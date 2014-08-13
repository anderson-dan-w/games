#!/usr/bin/python
from __future__ import print_function, division
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import World

MONOSPACE = QFont('Courier MONOSPACE') ## don't think the text matters...
MONOSPACE.setStyleHint(MONOSPACE.TypeWriter, MONOSPACE.PreferDefault)

class Arrow(QPushButton):
    def __init__(self, text, xmove, ymove, world):
        super(Arrow, self).__init__(text)
        self.world = world
        self.xmove = xmove
        self.ymove = ymove
        self.setFixedWidth(18)
        self.clicked.connect(self.world.move)

class WorldQt(QWidget):
    def __init__(self, rows=10, cols=10):
        ## first, super it
        super(WorldQt, self).__init__()
        ## save input args?
        self.rows = rows
        self.cols = cols

        ## then do basic set up
        self.setGeometry(300, 500, 350, 350) ## (start_x, y; xlen, ylen)
        self.setWindowTitle('A Darkish Room')
        #self.setWindowIcon(QIcon('lighning.png')) ## not working here?

        ## layout
        layout = QGridLayout()
        self.setLayout(layout)

        ## movement
        self.UP    = Arrow('^',  0, -1, self)
        self.DOWN  = Arrow('v',  0,  1, self)
        self.LEFT  = Arrow('<', -1,  0, self)
        self.RIGHT = Arrow('>',  1,  0, self)
        layout.addWidget(self.UP   , 0, 1)
        layout.addWidget(self.DOWN , 2, 1)
        layout.addWidget(self.LEFT , 1, 0)
        layout.addWidget(self.RIGHT, 1, 2)

        ## set up the world
        self.world = World.World(self.rows, self.cols)

        ## now make it into a PyQt-usable object
        self.worldview = QTextEdit(self.world.get_view())
        self.worldview.setReadOnly(True)
        self.worldview.setFont(MONOSPACE)
        layout.addWidget(self.worldview, 3, 0,
                            self.world.MAX_X, self.world.MAX_Y)

        ## now show it
        self.show()

    def move(self):
        ## figure out where it's going...
        direction = self.sender()
        ## ...make the move on the underlying object...
        self.world.move(direction.xmove, direction.ymove)
        ## ...and actually show the change
        self.worldview.setText(self.world.get_view())

## create our main window
def main():
    app = QApplication(sys.argv)
    w = WorldQt()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
