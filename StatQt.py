#!/usr/bin/python
from __future__ import print_function, division
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class StatWidget(QWidget):
    def __init__(self, app):
        super(StatWidget, self).__init__()
        self.app = app
