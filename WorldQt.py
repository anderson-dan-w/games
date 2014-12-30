#!/usr/bin/python
from __future__ import print_function, division
from PyQt4.QtCore import *
from PyQt4.QtGui import *

MONOSPACE = QFont('Courier MONOSPACE') ## don't think the text matters...
MONOSPACE.setStyleHint(MONOSPACE.TypeWriter, MONOSPACE.PreferDefault)

class MoveCounter(QLabel):
    def __init__(self):
        super(MoveCounter, self).__init__()
        self.setFont(MONOSPACE)
        self.moves = -1
        self.increment()

    def increment(self):
        self.moves += 1
        width = len(str(self.moves)) ## math.log(self.moves, 10)
        ## 6=len('move: '); 9=pixel width of letter (experimentally determined)
        self.setFixedWidth((width + 6) * 9)
        self.setText('Move: {}'.format(self.moves))


class WorldWidget(QWidget):
    def __init__(self, rows=10, cols=15, app=None):
        super(WorldWidget, self).__init__()
        self.app = app
        self.rows = rows
        self.cols = cols

        layout = QGridLayout()
        self.setLayout(layout)
        ## set up the world
        self.world = World(self.rows, self.cols)

        ## now make it into a PyQt-usable object
        self.worldview = QTextEdit(self.world.get_view())
        self.worldview.setReadOnly(True)
        self.worldview.setFont(MONOSPACE)
        layout.addWidget(self.worldview, 0, 0,
                            self.world.MAX_X, self.world.MAX_Y)

        ## set up keys to navigate the world
        self.KEY_PRESS = {
                Qt.Key_J: lambda: self.move( 0, -1),
                Qt.Key_K: lambda: self.move( 0,  1),
                Qt.Key_H: lambda: self.move(-1,  0),
                Qt.Key_L: lambda: self.move( 1,  0)
        }

        self.moveCounter = MoveCounter()
        layout.addWidget(self.moveCounter, 0, self.world.MAX_X)

    def move(self, xmove, ymove):
        ## make the move on the underlying object...
        self.world.move(xmove, ymove)
        ## ...and actually show the change
        self.moveCounter.increment()
        self.worldview.setText(self.world.get_view())

    def keyPressEvent(self, event):
        key = event.key()
        if key in self.KEY_PRESS:
            self.KEY_PRESS[key]()
            if self.world.grid[self.world.ME.y][self.world.ME.x].text == 'T':
                reply = QMessageBox.question(self, 'Town', 'Shall we enter?',
                        QMessageBox.Yes|QMessageBox.No)
                if reply == QMessageBox.Yes:
                    print("heyyy")

        else:
            event.ignore()

class Cell(object):
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.color = "green"
        self.background_color = "yellow"
        self.text = '.'
        self.visible = False

    def __sub__(self, other):
        """ Return shortest (wrappable) Manhattan distance """
        xdiff = min((self.x - other.x) % self.world.MAX_X,
                    (other.x - self.x) % self.world.MAX_X)
        ydiff = min((self.y - other.y) % self.world.MAX_Y,
                    (other.y - self.y) % self.world.MAX_Y)
        return xdiff + ydiff

    def __str__(self):
        return ('<span style="color:{}; background-color:{};">{}</span>'
                .format(self.color, self.background_color, self.text))

    def render(self):
        if self - self.world.ME == 0:
            return str(self.world.ME)
        if self.world.isnight and (self - self.world.ME) > self.world.nsight:
            return '<span style="background-color:black">&nbsp;</span>'
        if not self.visible:
            return '&nbsp;'
        return self.__str__()

class TownCell(Cell):
    def __init__(self, x, y, world):
        super(TownCell, self).__init__(x, y, world)
        self.color = "red"
        self.text = "T"

class World(object):
    DAY_LENGTH = 20  ## arbitrary
    def __init__(self, rows=10, cols=10):
        self.MAX_X = cols
        self.MAX_Y = rows
        self.nsight = 2 ## default visibility length
        ## initialize empty cell grid
        ##@TODO: eventually need some more variety in here...
        self.grid = [[Cell(x, y, self) for x in range(self.MAX_X)]
                        for y in range(self.MAX_Y)]
        ## deal with ME
        self.ME = Cell(int(self.MAX_X/2), int(self.MAX_Y/2), self)
        self.ME.text = 'i'

        ## other details about the world
        self.isnight = False
        self.nmove = 0

        ## add a random town
        town = TownCell(self.ME.x + 1, self.ME.y - 1, self)
        self.grid[town.y][town.x] = town

        ## initialize view and show it:
        ## *after* re-setting things, so their .visible's are set properly
        self.grid[self.ME.y][self.ME.x].visible = True
        self._add_visible() ## fill in initial view

    def _add_visible(self):
        """ POST-move, add new visibility. redundant, but oh well """
        ## if arriving in new areas with nsight > 2,
        for dist in range(self.nsight):
            for dir_x, dir_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                edge_x = self.ME.x + (dir_x * dist)
                edge_y = self.ME.y + (dir_y * dist)
                for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx = (edge_x + x) % self.MAX_X
                    ny = (edge_y + y) % self.MAX_Y
                    self.grid[ny][nx].visible = True

    def move(self, x, y):
        self.ME.x = (self.ME.x + x) % self.MAX_X
        self.ME.y = (self.ME.y + y) % self.MAX_Y
        self._add_visible()
        self.nmove += 1
        if (self.nmove % self.DAY_LENGTH) >= int(self.DAY_LENGTH/4):
            self.isnight = False
        else:
            self.isnight = True

    def get_view(self):
        s = ""
        for y in range(self.MAX_Y):
            for x in range(self.MAX_X):
                s += self.grid[y][x].render()
            s += '<br>'
        return s

