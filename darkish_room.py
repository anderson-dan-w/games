#!/usr/bin/python
from __future__ import print_function, division
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import WorldQt
import StatQt

class TabBar(QTabWidget):
    def __init__(self, rows, cols, app):
        super(TabBar, self).__init__()
        self.app = app

        ## add the world tab
        self.worldWidget = WorldQt.WorldWidget(rows, cols, self.app)
        self.addTab(self.worldWidget, "World")

        ## add a stat tab
        self.statWidget = StatQt.StatWidget(self.app)
        self.addTab(self.statWidget, "Stats")

class AppQt(QWidget):
    def __init__(self, rows=10, cols=15):
        ## first, super it
        super(AppQt, self).__init__()

        ## then do basic set up
        self.setGeometry(300, 500, 350, 350) ## (start_x, y; xlen, ylen)
        self.setWindowTitle('A Darkish Room')

        ## layout
        layout = QGridLayout()
        self.setLayout(layout)

        ## add a tab for the world
        self.tabBar = TabBar(rows, cols, self)
        layout.addWidget(self.tabBar, 0, 0)

        ## now show everything
        self.show()

## create our main window
def main():
    app = QApplication(sys.argv)
    appqt = AppQt()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

