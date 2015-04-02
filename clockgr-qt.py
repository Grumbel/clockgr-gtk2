#!/usr/bin/env python3

# clockgr - A fullscreen clock for Qt
# Copyright (C) 2015 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
from datetime import datetime
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QPixmap
from PyQt5.QtCore import QRectF, QTimer
from PyQt5.QtWidgets import (QGraphicsScene, QMainWindow, QWidget,
                             QVBoxLayout, QGraphicsView, QApplication,
                             QGraphicsItemGroup, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsLineItem)

from clockgrqt.analog_clock import AnalogClock
from clockgrqt.digital_clock import DigitalClock
from clockgrqt.calendar import CalendarDesklet
from clockgrqt.style import Style


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.inverted = False

        central = QWidget()

        self.graphics_view = QGraphicsView(central)
        self.graphics_view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        #self.graphics_view.centerOn(1200/2, 900/2)

        self.scene = QGraphicsScene()

        self.graphics_view.setScene(self.scene)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.graphics_view)
        central.setLayout(layout)

        self.setCentralWidget(central)
        self.show()

        style = Style()

        self.debug_rect = self.scene.addRect(QRectF(0, 0, 1199, 899))
        self.debug_rect.setPen(QPen(QColor(255, 0, 0)))

        world = self.scene.addPixmap(QPixmap("world_g.png"))
        world.setPos(1200 - 540 - 32, 900 - 276 - 32)

        self.analog_clock = AnalogClock()
        self.analog_clock.set_rect(QRectF(900 - 256, 32, 512, 512))
        self.analog_clock.set_style(style)
        self.analog_clock.set_time(datetime.now())
        self.scene.addItem(self.analog_clock.root)

        self.digital_clock = DigitalClock()
        self.digital_clock.set_rect(QRectF(32, 670, 640, 200))
        self.digital_clock.set_style(style)
        self.digital_clock.set_rect(QRectF(32, 670, 640, 200))
        self.digital_clock.update(datetime.now())
        self.scene.addItem(self.digital_clock.root)

        self.calendar = CalendarDesklet()
        self.calendar.update(datetime.now())
        self.calendar.set_style(style)
        self.calendar.set_rect(QRectF(32, 32, 512, 412))
        self.calendar.set_style(style)
        self.calendar.update(datetime.now())
        self.scene.addItem(self.calendar.root)

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.my_update)
        self.timer.start()

        # self.world = self.add_desklet(WorldDesklet(),    (1200 - 540 - 32, 900 - 276 - 32, 540, 276))
        # self.stopwatch = self.add_desklet(StopWatch(),       (32, 64, 500, 180))

        self.setMinimumSize(1200, 900)

    def invert(self):
        if self.inverted:
            style = Style()
        else:
            style = Style()
            (style.background_color,
             style.foreground_color) = \
             (style.foreground_color,
              style.background_color)

        self.scene.setBackgroundBrush(style.background_color)
        self.calendar.set_style(style)
        self.digital_clock.set_style(style)
        self.analog_clock.set_style(style)

        self.inverted = not self.inverted

    def my_update(self, *args):
        now = datetime.now()
        self.analog_clock.set_time(now)
        self.digital_clock.update(now)

    def closeEvent(self, event):
        event.accept()

    def keyPressEvent(self, ev):
        # cursor keys are eaten up by the QGraphicsView

        if ev.key() == Qt.Key_Escape:
            QApplication.instance().quit()
        elif ev.key() == Qt.Key_I:
            self.invert()
        elif ev.key() == Qt.Key_F or ev.key() == Qt.Key_F11:
            if self.windowState() & Qt.WindowFullScreen:
                self.showNormal()
            else:
                self.showFullScreen()
        elif ev.key() == Qt.Key_1:
            self.calendar.previous_month()
        elif ev.key() == Qt.Key_2:
            self.calendar.next_month()
        else:
            pass


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()

    # manually tear down the app, PyQt crashes otherwise
    del window
    del app


if __name__ == "__main__":
    main()


# EOF #
