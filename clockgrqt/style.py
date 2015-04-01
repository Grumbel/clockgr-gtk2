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


from PyQt5.QtGui import QFont, QColor


class Style:

    def __init__(self):
        self.font = QFont("DejaVu Sans")

        self.background_color = QColor.fromRgbF(1.0, 1.0, 1.0)
        self.midcolor = QColor.fromRgbF(0.5, 0.5, 0.5)
        self.foreground_color = QColor.fromRgbF(0, 0, 0)


# EOF #