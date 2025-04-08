# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6 import QtWidgets, QtGui
from GridCalEngine.Devices.Injections.battery import Battery
from GridCal.Gui.Diagrams.generic_graphics import ACTIVE, DEACTIVATED, OTHER, Square
from GridCal.Gui.Diagrams.SchematicWidget.Injections.injections_template_graphics import InjectionTemplateGraphicItem
from GridCal.Gui.messages import yes_no_question

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from GridCal.Gui.Diagrams.SchematicWidget.schematic_widget import SchematicWidget


class BatteryGraphicItem(InjectionTemplateGraphicItem):

    def __init__(self, parent, api_obj: Battery, editor: SchematicWidget):
        """

        :param parent:
        :param api_obj:
        :param editor:
        """
        InjectionTemplateGraphicItem.__init__(self,
                                              parent=parent,
                                              api_obj=api_obj,
                                              editor=editor,
                                              device_type_name='generator',
                                              w=40,
                                              h=40)

        pen = QtGui.QPen(self.color, self.width, self.style)

        self.glyph = Square(self)
        self.glyph.setRect(0, 0, self.h, self.w)
        self.glyph.setPen(pen)
        self.addToGroup(self.glyph)

        self.label = QtWidgets.QGraphicsTextItem('B', parent=self.glyph)
        self.label.setDefaultTextColor(self.color)
        self.label.setPos(self.h / 4, self.w / 5)

        self.setPos(self.parent.x(), self.parent.y() + 100)
        self.update_nexus(self.pos())

    def recolour_mode(self):
        """
        Change the colour according to the system theme
        """
        if self.api_object is not None:
            if self.api_object.active:
                self.color = ACTIVE['color']
                self.style = ACTIVE['style']
            else:
                self.color = DEACTIVATED['color']
                self.style = DEACTIVATED['style']
        else:
            self.color = ACTIVE['color']
            self.style = ACTIVE['style']

        pen = QtGui.QPen(self.color, self.width, self.style)
        self.glyph.setPen(pen)
        self.nexus.setPen(pen)
        self.label.setDefaultTextColor(self.color)

    def contextMenuEvent(self, event):
        """
        Display context menu
        @param event:
        @return:
        """
        menu = QtWidgets.QMenu()
        menu.addSection("Battery")

        pe = menu.addAction('Active')
        pe.setCheckable(True)
        pe.setChecked(self.api_object.active)
        pe.triggered.connect(self.enable_disable_toggle)

        pa = menu.addAction('Plot profiles')
        plot_icon = QtGui.QIcon()
        plot_icon.addPixmap(QtGui.QPixmap(":/Icons/icons/plot.svg"))
        pa.setIcon(plot_icon)
        pa.triggered.connect(self.plot)

        da = menu.addAction('Delete')
        del_icon = QtGui.QIcon()
        del_icon.addPixmap(QtGui.QPixmap(":/Icons/icons/delete3.svg"))
        da.setIcon(del_icon)
        da.triggered.connect(self.remove)

        rabf = menu.addAction('Change bus')
        move_bus_icon = QtGui.QIcon()
        move_bus_icon.addPixmap(QtGui.QPixmap(":/Icons/icons/move_bus.svg"))
        rabf.setIcon(move_bus_icon)
        rabf.triggered.connect(self.change_bus)

        menu.exec_(event.screenPos())

    def enable_disable_toggle(self):
        """

        @return:
        """
        if self.api_object is not None:
            if self.api_object.active:
                self.set_enable(False)
            else:
                self.set_enable(True)

            if self.editor.circuit.has_time_series:
                ok = yes_no_question('Do you want to update the time series active status accordingly?',
                                     'Update time series active status')

                if ok:
                    # change the bus state (time series)
                    self.editor.set_active_status_to_profile(self.api_object, override_question=True)

    def set_enable(self, val=True):
        """
        Set the enable value, graphically and in the API
        @param val:
        @return:
        """
        self.api_object.active = val
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']
        self.glyph.setPen(QtGui.QPen(self.color, self.width, self.style))
        self.label.setDefaultTextColor(self.color)

    def plot(self):
        """
        Plot API objects profiles
        """
        # time series object from the last simulation
        ts = self.editor.circuit.time_profile

        # plot the profiles
        self.api_object.plot_profiles(time=ts)
