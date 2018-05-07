from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

class Tutorial(QWidget):
    def __init__(self, parent = None):
        super(Tutorial, self).__init__(parent)
        self.ui = uic.loadUi("Tutorial.ui")
        f = open("tutorial.txt", "r")
        s = f.read()
        if "False" in s:
            self.flag = False
        else:
            self.flag = True
        self.ui.dontShowBox.stateChanged.connect(self.setBox)
        self.ui.pushButton.clicked.connect(self.checkState)
        
    def setBox(self, index):
        if index == 2:
            self.flag = False
        else:
            self.flag = True
        
    def checkState(self):
        if self.flag == False:
            f = open("tutorial.txt", "w")
            f.write("False")
            f.flush()
            f.close()
        self.ui.hide()
