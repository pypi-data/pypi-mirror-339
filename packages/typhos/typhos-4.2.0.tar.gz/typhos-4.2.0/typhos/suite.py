"""
The high-level Typhos Suite, which bundles tools and panels.
"""
from __future__ import annotations

import logging
import os
import pathlib
import textwrap
from functools import partial
from typing import Optional, Union

import ophyd
import pcdsutils.qt
from ophyd import Device
from pyqtgraph import parametertree
from pyqtgraph.parametertree import parameterTypes as ptypes
from qtpy import QtCore, QtGui, QtWidgets

from . import utils, widgets
from .display import DisplayTypes, ScrollOptions, TyphosDeviceDisplay
from .tools import TyphosLogDisplay, TyphosTimePlot
from .utils import (TyphosBase, TyphosException, clean_attr, clean_name,
                    flatten_tree, save_suite)

logger = logging.getLogger(__name__)
# Use non-None sentinel value since None means no tools
DEFAULT_TOOLS = object()


class SidebarParameter(parametertree.Parameter):
    """
    Parameter to hold information for the sidebar.

    Attributes
    ----------
    itemClass : type
        The class to be used for the parameter.

    sigOpen : QtCore.Signal
        A signal indicating an open request for the parameter.

    sigHide : QtCore.Signal
        A signal indicating an hide request for the parameter.

    sigEmbed : QtCore.Signal
        A signal indicating an embed request for the parameter.
    """

    itemClass = widgets.TyphosSidebarItem
    sigOpen = QtCore.Signal(object)
    sigHide = QtCore.Signal(object)
    sigEmbed = QtCore.Signal(object)

    def __init__(self, devices=None, embeddable=None, **opts):
        super().__init__(**opts)
        self.embeddable = embeddable
        self.devices = list(devices) if devices else []

    def has_device(self, device: ophyd.Device):
        """
        Determine if this parameter contains the given device.

        Parameters
        ----------
        device : ophyd.OphydObj or str
            The device or its name.

        Returns
        -------
        has_device : bool
        """
        return any(
            (device in self.devices,
             device in getattr(self.value(), 'devices', []),
             self.name() == device,
             isinstance(device, str) and self.name() == clean_attr(device),
             )
        )


class TyphosDisplayNotCreatedError(TyphosException):
    """The given subdisplay has not yet been shown."""
    ...


class LazySubdisplay(QtWidgets.QWidget):
    """
    A lazy subdisplay which only is instantiated when shown in the suite.

    Supports devices by way of ``add_device``.

    Parameters
    ----------
    widget_cls : QtWidgets.QWidget subclass
        The widget class to instantiate.
    """

    widget_cls: type[QtWidgets.QWidget]
    widget: QtWidgets.QWidget | None
    devices: list[ophyd.Device]

    def __init__(self, widget_cls: type[QtWidgets.QWidget]):
        super().__init__()
        self.widget_cls = widget_cls
        self.widget = None

        self.setVisible(False)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.devices = []

    def add_device(self, device: ophyd.Device):
        """Hook for adding a device from the suite."""
        self.devices.append(device)

    def hideEvent(self, event: QtGui.QHideEvent):
        """Hook for when the tool is hidden."""
        return super().hideEvent(event)

    def _create_widget(self):
        """Make the widget no longer lazy."""
        if self.widget is not None:
            return

        self.widget = self.widget_cls()
        self.layout().addWidget(self.widget)
        self.setSizePolicy(self.widget.sizePolicy())

        if hasattr(self.widget, "add_device"):
            for device in self.devices:
                self.widget.add_device(device)

    def showEvent(self, event: QtGui.QShowEvent):
        """Hook for when the tool is shown in the suite."""
        if self.widget is None:
            self._create_widget()

        return super().showEvent(event)

    def minimumSizeHint(self):
        """Minimum size hint forwarder from the embedded widget."""
        if self.widget is not None:
            return self.widget.minimumSizeHint()
        return self.sizeHint()

    def sizeHint(self):
        """Size hint forwarder from the embedded widget."""
        if self.widget is not None:
            return self.widget.sizeHint()
        return QtCore.QSize(100, 100)


class DeviceParameter(SidebarParameter):
    """
    Parameter to hold information on an Ophyd Device.

    Parameters
    ----------
    device : ophyd.Device
        The device instance.

    subdevices : bool, optional
        Include child parameters for sub devices of ``device``.

    **opts
        Passed to super().__init__.
    """

    itemClass = widgets.TyphosSidebarItem

    def __init__(self, device, subdevices=True, **opts):
        # Set options for parameter
        opts['name'] = clean_name(device, strip_parent=device.root)
        self.device = device
        opts['expanded'] = False
        # Grab children from the given device
        children = list()
        if subdevices:
            for child in device._sub_devices:
                subdevice = getattr(device, child)
                if subdevice._sub_devices:
                    # If that device has children, make sure they are also
                    # displayed further in the tree
                    children.append(
                        DeviceParameter(subdevice, subdevices=False)
                    )
                else:
                    # Otherwise just make a regular parameter out of it
                    child_name = clean_name(subdevice,
                                            strip_parent=subdevice.root)
                    param = SidebarParameter(
                        value=partial(TyphosDeviceDisplay.from_device,
                                      subdevice),
                        name=child_name,
                        embeddable=True,
                        devices=[subdevice],
                    )
                    children.append(param)

        opts['children'] = children
        super().__init__(
            value=partial(TyphosDeviceDisplay.from_device, device),
            embeddable=opts.pop('embeddable', True),
            devices=[device],
            **opts
        )


class TyphosSuite(TyphosBase):
    """
    This suite combines tools and devices into a single widget.

    A :class:`ParameterTree` is contained in a :class:`~pcdsutils.qt.QPopBar`
    which shows tools and the hierarchy of a device along with options to
    show or hide them.

    Parameters
    ----------
    parent : QWidget, optional

    pin : bool, optional
        Pin the parameter tree on startup.

    content_layout : QLayout, optional
        Sets the layout for when we have multiple subdisplays
        open in the suite. This will have a horizontal layout by
        default but can be changed as needed for the use case.

    default_display_type : DisplayType, optional
        DisplayType enum that determines the type of display to open when we
        add a device to the suite. Defaults to DisplayType.detailed_screen.

    scroll_option : ScrollOptions, optional
        ScrollOptions enum that determines the behavior of scrollbars
        in the suite. Default is ScrollOptions.auto, which enables
        scrollbars for detailed and engineering screens but not for
        embedded displays.

    Attributes
    ----------
    default_tools : dict
        The default tools to use in the suite.  In the form of
        ``{'tool_name': ToolClass}``.
    """

    DEFAULT_TITLE = 'Typhos Suite'
    DEFAULT_TITLE_DEVICE = 'Typhos Suite - {device.name}'

    default_tools = {
        "Log": TyphosLogDisplay,
        "StripTool": TyphosTimePlot,
    }

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        *,
        pin: bool = False,
        content_layout: QtWidgets.QLayout | None = None,
        default_display_type: DisplayTypes = DisplayTypes.embedded_screen,
        scroll_option: ScrollOptions = ScrollOptions.auto,
    ):
        super().__init__(parent=parent)

        self._update_title()

        self._tree = parametertree.ParameterTree(parent=self, showHeader=False)
        self._tree.setAlternatingRowColors(False)
        self._save_action = ptypes.ActionParameter(name='Save Suite')
        self._tree.addParameters(self._save_action)
        self._save_action.sigActivated.connect(self.save)

        self._bar = pcdsutils.qt.QPopBar(title='Suite', parent=self,
                                         widget=self._tree, pin=pin)

        self._tree.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        self._tree.setMinimumSize(250, 150)

        self._content_frame = QtWidgets.QFrame(self)
        self._content_frame.setObjectName("content")
        self._content_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)

        # Content frame layout: configurable
        # Defaults to [content] [content] [content] ... in one line
        if content_layout is None:
            content_layout = QtWidgets.QHBoxLayout()
        self._content_frame.setLayout(content_layout)

        # Horizontal box layout: [PopBar] [Content Frame]
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._bar)
        layout.addWidget(self._content_frame)

        self.embedded_dock = None
        self.default_display_type = default_display_type
        self.scroll_option = scroll_option

    def add_subdisplay(self, name, display, category):
        """
        Add an arbitrary widget to the tree of available widgets and tools.

        Parameters
        ----------
        name : str
            Name to be displayed in the tree

        display : QWidget
            QWidget to show in the dock when expanded.

        category : str
            The top level group to place the controls under in the tree. If the
            category does not exist, a new one will be made
        """
        logger.debug("Adding widget %r with %r to %r ...",
                     name, display, category)
        # Create our parameter
        parameter = SidebarParameter(value=display, name=name)
        self._add_to_sidebar(parameter, category)

    def add_lazy_subdisplay(
        self, name: str, display_class: type[QtWidgets.QWidget], category: str
    ):
        """
        Add an arbitrary widget to the tree of available widgets and tools.

        Parameters
        ----------
        name : str
            Name to be displayed in the tree

        display_class : subclass of QWidget
            QWidget class to show in the dock when expanded.

        category : str
            The top level group to place the controls under in the tree. If the
            category does not exist, a new one will be made
        """
        logger.debug("Adding lazy subdisplay %r with %r to %r ...",
                     name, display_class, category)
        # Create our parameter
        parameter = SidebarParameter(
            value=LazySubdisplay(display_class),
            name=name
        )
        self._add_to_sidebar(parameter, category)

    @property
    def top_level_groups(self):
        """
        Get top-level groups.

        This is of the form:

        .. code:: python

            {'name': QGroupParameterItem}
        """
        root = self._tree.invisibleRootItem()
        return {root.child(idx).param.name():
                root.child(idx).param
                for idx in range(root.childCount())}

    def add_tool(self, name: str, tool: type[QtWidgets.QWidget]):
        """
        Add a widget to the toolbar.

        Shortcut for:

        .. code:: python

           suite.add_subdisplay(name, tool, category='Tools')

        Parameters
        ----------
        name : str
            Name of tool to be displayed in sidebar

        tool : QWidget
            Widget to be added to ``.ui.subdisplay``
        """
        self.add_lazy_subdisplay(name, tool, "Tools")

    def get_subdisplay(self, display: Union[Device, str], instantiate: bool = True):
        """
        Get a subdisplay by name or contained device.

        Parameters
        ----------
        display : str or Device
            Name of screen or device
        instantiate : bool, optional
            Instantiate lazy sub-displays if they do not already exist.
            Raise otherwise.

        Returns
        -------
        widget : QWidget or partial
            Widget that is a member of the :attr:`.ui.subdisplay`

        Example
        -------
        .. code:: python

            suite.get_subdisplay(my_device.x)
            suite.get_subdisplay('My Tool')
        """
        if not isinstance(display, SidebarParameter):
            for group in self.top_level_groups.values():
                tree = flatten_tree(group)
                matches = [
                    param for param in tree
                    if hasattr(param, 'has_device') and
                    param.has_device(display)
                ]

                if matches:
                    display = matches[0]
                    break

        if not isinstance(display, SidebarParameter):
            # If we got here we can't find the subdisplay
            raise ValueError(f"Unable to find subdisplay {display}")

        subdisplay = display.value()
        if isinstance(subdisplay, partial):
            if not instantiate:
                raise TyphosDisplayNotCreatedError(
                    f"Subdisplay {display} has not been created yet"
                )

            subdisplay = subdisplay()
            display.setValue(subdisplay)
        return subdisplay

    @QtCore.Slot(str)
    @QtCore.Slot(object)
    def show_subdisplay(
        self,
        widget: Union[QtWidgets.QWidget, SidebarParameter, str],
    ) -> QtWidgets.QWidget:
        """
        Open a display in the dock system.

        Parameters
        ----------
        widget : QWidget, SidebarParameter or str
            If given a ``SidebarParameter`` from the tree, the widget will be
            shown and the sidebar item update. Otherwise, the information is
            passed to :meth:`.get_subdisplay`

        Returns
        -------
        widget : QWidget
            The subdisplay that was shown.
        """
        # Grab true widget
        if not isinstance(widget, QtWidgets.QWidget):
            widget = self.get_subdisplay(widget)

        # Setup the dock
        dock = widgets.SubDisplay(self)
        # Set sidebar properly
        self._show_sidebar(widget, dock)
        # Add the widget to the dock
        logger.debug("Showing widget %r ...", widget)
        if hasattr(widget, 'scroll_option'):
            widget.scroll_option = self.scroll_option
        if hasattr(widget, "display_type"):
            # Setting a display_type implicitly loads the best template.
            widget.display_type = self.default_display_type
        dock.setWidget(widget)

        # Add to layout
        content_layout = self._content_frame.layout()
        content_layout.addWidget(dock)
        if isinstance(content_layout, QtWidgets.QGridLayout):
            self._content_frame.layout().setAlignment(
                dock, QtCore.Qt.AlignHCenter
            )
            self._content_frame.layout().setAlignment(
                dock, QtCore.Qt.AlignTop
            )

        self._new_template()
        if isinstance(widget, TyphosDeviceDisplay):
            widget.template_changed.connect(self._new_template)
        return widget

    def _new_template(self, template: Optional[pathlib.Path] = None) -> None:
        """Hook for when a new template is selected in a sub-display."""
        if self.parent() is not None:
            return

        new_width = self.minimumSizeHint().width()
        if self.width() < new_width:
            self.resize(new_width, self.height())

    @QtCore.Slot(str)
    @QtCore.Slot(object)
    def embed_subdisplay(self, widget):
        """Embed a display in the dock system."""
        # Grab the relevant display
        if not self.embedded_dock:
            self.embedded_dock = widgets.SubDisplay()
            self.embedded_dock.setWidget(QtWidgets.QWidget())
            self.embedded_dock.widget().setLayout(QtWidgets.QVBoxLayout())
            self.embedded_dock.widget().layout().addStretch(1)
            self._content_frame.layout().addWidget(self.embedded_dock)

        if not isinstance(widget, QtWidgets.QWidget):
            widget = self.get_subdisplay(widget)
        # Set sidebar properly
        self._show_sidebar(widget, self.embedded_dock)
        # Set our widget to be embedded
        widget.setVisible(True)
        widget.display_type = widget.embedded_screen
        widget_count = self.embedded_dock.widget().layout().count()
        self.embedded_dock.widget().layout().insertWidget(widget_count - 1,
                                                          widget)

    @QtCore.Slot()
    @QtCore.Slot(object)
    def hide_subdisplay(self, widget):
        """
        Hide a visible subdisplay.

        Parameters
        ----------
        widget: SidebarParameter or Subdisplay
            If you give a SidebarParameter, we will find the corresponding
            widget and hide it. If the widget provided to us is inside a
            DockWidget we will close that, otherwise the widget is just hidden.
        """
        if not isinstance(widget, QtWidgets.QWidget):
            try:
                widget = self.get_subdisplay(widget, instantiate=False)
            except TyphosDisplayNotCreatedError:
                logger.debug("Subdisplay was never shown; nothing to do: %s", widget)
                return

        sidebar = self._get_sidebar(widget)
        if sidebar:
            for item in sidebar.items:
                item._mark_hidden()
        else:
            logger.warning("Unable to find sidebar item for %r", widget)
        # Make sure the actual widget is hidden
        logger.debug("Hiding widget %r ...", widget)
        if isinstance(widget.parent(), QtWidgets.QDockWidget):
            logger.debug("Closing dock ...")
            widget.parent().close()
        # Hide the full dock if this is the last widget
        elif (self.embedded_dock
              and widget.parent() == self.embedded_dock.widget()):
            logger.debug("Removing %r from embedded widget layout ...",
                         widget)
            self.embedded_dock.widget().layout().removeWidget(widget)
            widget.hide()
            if self.embedded_dock.widget().layout().count() == 1:
                logger.debug("Closing embedded layout ...")
                self.embedded_dock.close()
                self.embedded_dock = None
        else:
            widget.hide()

    @QtCore.Slot()
    def hide_subdisplays(self):
        """Hide all open displays."""
        # Grab children from devices
        for group in self.top_level_groups.values():
            for param in flatten_tree(group)[1:]:
                self.hide_subdisplay(param)

    @property
    def tools(self):
        """Tools loaded into the suite."""
        if 'Tools' in self.top_level_groups:
            return [param.value()
                    for param in self.top_level_groups['Tools'].childs]
        return []

    def _update_title(self, device=None):
        """
        Update the window title, optionally with a device.

        Parameters
        ----------
        device : ophyd.Device, optional
            Device to indicate in the title.
        """
        title_fmt = (self.DEFAULT_TITLE if device is None
                     else self.DEFAULT_TITLE_DEVICE)

        self.setWindowTitle(title_fmt.format(self=self, device=device))

    def add_device(self, device, children=True, category='Devices'):
        """
        Add a device to the suite.

        Parameters
        ----------
        device: ophyd.Device
            The device to add.

        children: bool, optional
            Also add any ``subdevices`` of this device to the suite as well.

        category: str, optional
            Category of device. By default, all devices will just be added to
            the "Devices" group
        """

        super().add_device(device)
        self._update_title(device)
        # Create DeviceParameter and add to top level category
        dev_param = DeviceParameter(device, subdevices=children)
        self._add_to_sidebar(dev_param, category)
        # Grab children
        for child in flatten_tree(dev_param)[1:]:
            self._add_to_sidebar(child)
        # Add a device to all the tool displays
        for tool in self.tools:
            try:
                tool.add_device(device)
            except Exception:
                logger.exception("Unable to add %s to tool %s",
                                 device.name, type(tool))

    @classmethod
    def from_device(
        cls,
        device: Device,
        parent: QtWidgets.QWidget | None = None,
        tools: dict[str, type] | None | DEFAULT_TOOLS = DEFAULT_TOOLS,
        pin: bool = False,
        content_layout: QtWidgets.QLayout | None = None,
        default_display_type: DisplayTypes = DisplayTypes.detailed_screen,
        scroll_option: ScrollOptions = ScrollOptions.auto,
        show_displays: bool = True,
        **kwargs,
    ) -> TyphosSuite:
        """
        Create a new :class:`TyphosSuite` from an :class:`ophyd.Device`.

        Parameters
        ----------
        device : ophyd.Device
            The device to use.

        children : bool, optional
            Choice to include child Device components

        parent : QWidget

        tools : dict, optional
            Tools to load for the object. ``dict`` should be name, class pairs.
            By default these will be ``.default_tools``, but ``None`` can be
            passed to avoid tool loading completely.

        pin : bool, optional
            Pin the parameter tree on startup.

        content_layout : QLayout, optional
            Sets the layout for when we have multiple subdisplays
            open in the suite. This will have a horizontal layout by
            default but can be changed as needed for the use case.

        default_display_type : DisplayTypes, optional
            DisplayTypes enum that determines the type of display to open when
            we add a device to the suite. Defaults to
            DisplayTypes.detailed_screen.

        scroll_option : ScrollOptions, optional
            ScrollOptions enum that determines the behavior of scrollbars
            in the suite. Default is ScrollOptions.auto, which enables
            scrollbars for detailed and engineering screens but not for
            embedded displays.

        show_displays : bool, optional
            If True (default), open all the included device displays.
            If False, do not open any of the displays.

        **kwargs :
            Passed to :meth:`TyphosSuite.add_device`
        """
        return cls.from_devices([device], parent=parent, tools=tools, pin=pin,
                                content_layout=content_layout,
                                default_display_type=default_display_type,
                                scroll_option=scroll_option,
                                show_displays=show_displays,
                                **kwargs)

    @classmethod
    def from_devices(
        cls,
        devices: list[Device],
        parent: QtWidgets.QWidget | None = None,
        tools: dict[str, type] | None | DEFAULT_TOOLS = DEFAULT_TOOLS,
        pin: bool = False,
        content_layout: QtWidgets.QLayout | None = None,
        default_display_type: DisplayTypes = DisplayTypes.detailed_screen,
        scroll_option: ScrollOptions = ScrollOptions.auto,
        show_displays: bool = True,
        **kwargs,
    ) -> TyphosSuite:
        """
        Create a new TyphosSuite from an iterator of :class:`ophyd.Device`

        Parameters
        ----------
        device : ophyd.Device

        children : bool, optional
            Choice to include child Device components

        parent : QWidget

        tools : dict, optional
            Tools to load for the object. ``dict`` should be name, class pairs.
            By default these will be ``.default_tools``, but ``None`` can be
            passed to avoid tool loading completely.

        pin : bool, optional
            Pin the parameter tree on startup.

        content_layout : QLayout, optional
            Sets the layout for when we have multiple subdisplays
            open in the suite. This will have a horizontal layout by
            default but can be changed as needed for the use case.

        default_display_type : DisplayTypes, optional
            DisplayTypes enum that determines the type of display to open when
            we add a device to the suite. Defaults to
            DisplayTypes.detailed_screen.

        scroll_option : ScrollOptions, optional
            ScrollOptions enum that determines the behavior of scrollbars
            in the suite. Default is ScrollOptions.auto, which enables
            scrollbars for detailed and engineering screens but not for
            embedded displays.

        show_displays : bool, optional
            If True (default), open all the included device displays.
            If False, do not open any of the displays.

        **kwargs :
            Passed to :meth:`TyphosSuite.add_device`
        """
        suite = cls(
            parent=parent,
            pin=pin,
            content_layout=content_layout,
            default_display_type=default_display_type,
            scroll_option=scroll_option,
        )
        if tools is not None:
            logger.info("Loading Tools ...")
            if tools is DEFAULT_TOOLS:
                logger.debug("Using default TyphosSuite tools ...")
                tools = cls.default_tools
            for name, tool in tools.items():
                try:
                    suite.add_tool(name, tool)
                except Exception:
                    logger.exception("Unable to load %s", type(tool))

        logger.info("Adding devices ...")
        for device in devices:
            try:
                suite.add_device(device, **kwargs)
                if show_displays:
                    suite.show_subdisplay(device)
            except Exception:
                logger.exception("Unable to add %r to TyphosSuite",
                                 device.name)
        return suite

    def save(self):
        """
        Save suite settings to a file using :meth:`typhos.utils.save_suite`.

        A ``QFileDialog`` will be used to query the user for the desired
        location of the created Python file

        The template will be of the form:

        .. code::
        """
        # Note: the above docstring is appended below

        logger.debug("Requesting file location for saved TyphosSuite")
        root_dir = os.getcwd()
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save TyphosSuite', root_dir, "Python (*.py)")
        if filename:
            try:
                with open(filename[0], 'w+') as handle:
                    save_suite(self, handle)
            except Exception as exc:
                logger.exception("Failed to save TyphosSuite")
                utils.raise_to_operator(exc)
        else:
            logger.debug("No filename chosen")

    # Add the template to the docstring
    save.__doc__ += textwrap.indent('\n' + utils.saved_template, '\t\t')

    def save_screenshot(
        self,
        filename: str,
    ) -> bool:
        """Save a screenshot of this widget to ``filename``."""

        image = utils.take_widget_screenshot(self)
        if image is None:
            logger.warning("Failed to take screenshot")
            return False

        logger.info(
            "Saving screenshot of suite titled '%s' to '%s'",
            self.windowTitle(), filename,
        )
        image.save(filename)
        return True

    def save_device_screenshots(
        self,
        filename_format: str,
    ) -> dict[str, str]:
        """Save screenshot(s) of devices to ``filename_format``."""

        filenames = {}
        for device in self.devices:
            display = self.get_subdisplay(device)

            if hasattr(display, "to_image"):
                image = display.to_image()
            else:
                # This is a fallback for if/when we don't have a TyphosDisplay
                image = utils.take_widget_screenshot(display)

            suite_title = self.windowTitle()
            widget_title = display.windowTitle()
            if image is None:
                logger.warning(
                    "Failed to take screenshot of device: %s in %s",
                    device.name, suite_title,
                )
                continue

            filename = filename_format.format(
                suite_title=suite_title,
                widget_title=widget_title,
                device=device,
                name=device.name,
            )
            logger.info(
                "Saving screenshot of '%s': '%s' to '%s'",
                suite_title, widget_title, filename,
            )
            image.save(filename)
            filenames[device.name] = filename
        return filenames

    def _get_sidebar(self, widget):
        items = {}
        for group in self.top_level_groups.values():
            for item in flatten_tree(group):
                items[item.value()] = item
        return items.get(widget)

    def _show_sidebar(self, widget, dock):
        sidebar = self._get_sidebar(widget)
        if sidebar:
            for item in sidebar.items:
                item._mark_shown()
            # Make sure we react if the dock is closed outside of our menu
            self._connect_partial_weakly(
                dock, dock.closing, self.hide_subdisplay, sidebar
            )
        else:
            logger.warning("Unable to find sidebar item for %r", widget)

    def _add_to_sidebar(self, parameter, category=None):
        """Add an item to the sidebar, connecting necessary signals."""
        if category:
            # Create or grab our category
            if category in self.top_level_groups:
                group = self.top_level_groups[category]
            else:
                logger.debug("Creating new category %r ...", category)
                group = ptypes.GroupParameter(name=category)
                self._tree.addParameters(group)
                self._tree.sortItems(0, QtCore.Qt.AscendingOrder)
            logger.debug("Adding %r to category %r ...",
                         parameter.name(), group.name())
            group.addChild(parameter)

        widget = parameter.value()
        if isinstance(widget, QtWidgets.QWidget):
            # Setup window to have a parent
            widget.setParent(self)
            widget.setHidden(True)

        logger.debug("Connecting parameter signals ...")
        self._connect_partial_weakly(
            parameter, parameter.sigOpen, self.show_subdisplay, parameter
        )
        self._connect_partial_weakly(
            parameter, parameter.sigHide, self.hide_subdisplay, parameter
        )
        if parameter.embeddable:
            self._connect_partial_weakly(
                parameter, parameter.sigEmbed, self.embed_subdisplay, parameter
            )
        return parameter
