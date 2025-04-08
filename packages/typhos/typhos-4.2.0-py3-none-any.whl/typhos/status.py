from __future__ import annotations

import dataclasses
import enum
import logging
import time
import traceback

from ophyd.status import Status
from ophyd.utils import (StatusTimeoutError, UnknownStatusFailure,
                         WaitTimeoutError)
from qtpy.QtCore import QObject, QThread, Signal

logger = logging.getLogger(__name__)


class TyphosStatusResult(enum.Enum):
    success = enum.auto()
    failure = enum.auto()
    timeout = enum.auto()


@dataclasses.dataclass
class TyphosStatusMessage:
    text: str
    tooltip: str


class TyphosStatusThread(QThread):
    """
    Thread which monitors an ophyd Status object and emits start/stop signals.

    The ``status_started`` signal may be emitted after ``start_delay`` seconds,
    unless the status has already completed, in which case it will not be
    emitted.

    The ``status_timeout`` signal will be emitted if the status starts and the
    timeout supplied to the ``TyphosStatusThread`` expires. This is distinct
    from an internal timeout from a status object, which is an error.
    The ``status_timeout`` is advisory rather than perscriptive and does not
    necessarily indicate a severe problem. If you want a status to be marked
    as failing after a timeout, pass the timeout to the status's constructor.

    The ``status_finished`` signal is guaranteed to be emitted after the status
    completes or fails, with a ``TyphosStatusResult`` enum set to
    ``success`` or to ``failure``.

    The ``error_message`` signal emits some information that could be useful
    for a GUI to display an error. This is a ``TyphosStatusMessage`` which
    contains a short error under ``.text`` and a longer message under
    ``.tooltip``, intended for e.g. a label and its mouseover tooltip text.
    This will not be emitted if the status succeeds.

    The ``status_exc`` signal emits the literal exception object from a
    status failure. This will not be emitted if the status succeeds.
    This can be useful for customizing what to do in the case of failure.

    Parameters
    ----------
    status : ophyd.status.StatusBase
        The status object.

    start_delay : float, optional
        Delay emitting ``status_started``. This avoids rapid flashes for
        statuses that complete quickly. Units of seconds.

    timeout : float, optional
        Timeout for considering status complete.

    Example
    ------

    .. code:: python

       thread = TyphosStatusThread(motor.set(...))
       thread.start()

    """
    status_started = Signal()
    status_timeout = Signal()
    status_finished = Signal(TyphosStatusResult)
    error_message = Signal(TyphosStatusMessage)
    status_exc = Signal(object)

    def __init__(
        self,
        status: Status,
        error_context: str = "Status",
        timeout_calc: str = "",
        start_delay: float = 0.,
        timeout: float = 10.0,
        parent: QObject | None = None,
    ):
        super().__init__(parent=parent)
        self.status = status
        self.error_context = error_context
        self.timeout_calc = timeout_calc
        self.start_delay = start_delay
        self.timeout = timeout

    def run(self) -> None:
        """Monitor status object status and emit signals."""
        # Don't do anything if we are handed a finished status
        if self.status.done:
            logger.debug("Status already completed.")
            self.wait_and_emit_finished()
            return

        # Wait to emit to avoid too much flashing
        time.sleep(self.start_delay)
        self.status_started.emit()
        self.wait_and_emit_finished()

    def wait_and_emit_finished(self) -> None:
        result = self.wait_and_get_result(use_timeout=True)
        if result == TyphosStatusResult.timeout:
            result = self.wait_and_get_result(use_timeout=False)
        logger.debug("Emitting finished: %r", result)
        self.status_finished.emit(result)

    def wait_and_get_result(self, use_timeout: bool) -> TyphosStatusResult:
        if use_timeout:
            timeout = self.timeout
        else:
            timeout = None
        try:
            self.status.wait(timeout=timeout)
        except WaitTimeoutError as ex:
            # Status doesn't have a timeout, but this thread does
            errmsg = f"{self.error_context} taking longer than expected, >{timeout}s"
            if self.timeout_calc:
                tooltip = f"Calculated as {self.timeout_calc}"
            else:
                tooltip = ""
            self.error_message.emit(
                TyphosStatusMessage(
                    text=errmsg,
                    tooltip=tooltip,
                )
            )
            logger.debug(f"{errmsg}, {tooltip}")
            self.status_timeout.emit()
            self.status_exc.emit(ex)
            return TyphosStatusResult.timeout
        except StatusTimeoutError as ex:
            # Status has an intrinsic timeout, and it's failing now
            errmsg = f"{self.error_context} failed with timeout, >{self.status.timeout:.2f}s"
            logger.debug(errmsg)
            self.error_message.emit(
                TyphosStatusMessage(
                    text=errmsg,
                    tooltip="",
                )
            )
            self.status_exc.emit(ex)
            return TyphosStatusResult.failure
        except UnknownStatusFailure as ex:
            # Status has failed, but no reason was given.
            errmsg = f"{self.error_context} failed with no reason given."
            logger.debug(errmsg)
            self.error_message.emit(
                TyphosStatusMessage(
                    text=errmsg,
                    tooltip="",
                )
            )
            self.status_exc.emit(ex)
            return TyphosStatusResult.failure
        except Exception as ex:
            # There is some other status failure, and it has a specific exception.
            logger.debug("Status failed", exc_info=True)
            self.error_message.emit(
                TyphosStatusMessage(
                    text=str(ex),
                    tooltip=traceback.format_exc(),
                )
            )
            self.status_exc.emit(ex)
            return TyphosStatusResult.failure
        else:
            # This is only reachable if the status wait succeeds
            return TyphosStatusResult.success
