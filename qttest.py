#!/usr/bin/python
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Thing(QWidget):
    def __init__(self):
        super(Thing, self).__init__()
        self.setGeometry(300, 500, 350, 350)

        self.show()

    def keyPressEvent(self, event):
        QMessageBox.information(self, "You hit something!",
                "event #{}".format(event.key()), QMessageBox.Yes)

def main():
    app = QApplication(sys.argv)
    t = Thing()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
