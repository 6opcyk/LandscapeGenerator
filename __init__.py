# -*- coding: utf-8-*-
from PyQt5.QtCore import *
from MainWindow import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec())
