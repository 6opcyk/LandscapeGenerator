# -*- coding: utf-8-*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from direct.task import Task  
from WorldGen import *
from Settings import *
from Tutorial import *
import sys
import random


class MainWindow(QMainWindow):
    maxSize = None
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.settings = Settings()
        self.tutorial = Tutorial()
        self.mapsUi = uic.loadUi("Maps.ui")
        WorldGenerator.initPanda()
        
        self.ui = uic.loadUi("MainMenu.ui")
        self.ui.setWindowTitle("LandscapeGenerator")
        self.ui.setDockOptions(self.dockOptions() | QMainWindow.ForceTabbedDocks)
        
        self.ui.actionNew.triggered.connect(self.showSettings)
        self.ui.actionClose.triggered.connect(self.closeTab)
        self.ui.actionImport_maps.triggered.connect(self.showMaps)
        self.ui.actionNormal_map.triggered.connect(self.changeNormalState)
        self.ui.actionHigh_map.triggered.connect(self.changeHighState)
        self.ui.actionInformation.triggered.connect(self.changeInfoState)
        
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.ui.tabWidget.currentChanged.connect(self.curChanged)
        self.ui.tabWidget.keyPressEvent = self.keyPressEvent
        self.ui.tabWidget.keyReleaseEvent = self.keyReleaseEvent
        
        self.settings.ui.generateButton.clicked.connect(self.addTab)
        self.settings.ui.cancelBut.clicked.connect(self.settings.ui.hide)

        self.mapsUi.butSaveHigh.clicked.connect(self.saveHigh)
        self.mapsUi.butSaveNormal.clicked.connect(self.saveNormal)
        
        self.dir = [0,0,0,0]
        self.mouseHpr = [0,0]
        self.oldMousePos = QCursor.pos()
        self.pressed_keys = []

        self.timer =  QTimer()
        self.timer.timeout.connect(taskMgr.step)
        self.timer.timeout.connect(self.keyHandler)
        self.timer.timeout.connect(self.updateInfo)
        self.timer.timeout.connect(self.mouseObserving)
        self.saveDialog = QFileDialog(self)
        
        self.changeAllState("hide")
        
        self.ui.showMaximized()
        self.settings.ui.show()
        
        MainWindow.maxSize = (QApplication.primaryScreen().size())
        
    def showSettings(self):
        self.settings.update_ui()
        self.settings.ui.show()
        
    def curChanged(self, index):
        if self.ui.tabWidget.currentWidget() != None:
            self.ui.hightMapLabel.setPixmap(self.ui.tabWidget.currentWidget().highMapPixmap)
            self.ui.normalMapLabel.setPixmap(self.ui.tabWidget.currentWidget().normalMapPixmap)
        else:
            self.ui.hightMapLabel.clear()
            self.ui.normalMapLabel.clear()
            self.ui.seedLabel.clear()
            self.ui.posLabel.clear()
            self.ui.angleLabel.clear()
            
    def showMaps(self):
        self.mapsUi.show()
        if self.ui.tabWidget.currentWidget() != None:
            tab = self.ui.tabWidget.currentWidget()
            self.mapsUi.normalLabel.setPixmap(self.ui.tabWidget.currentWidget().normalMapPixmap)
            self.mapsUi.highLabel.setPixmap(self.ui.tabWidget.currentWidget().highMapPixmap)
            
    def saveNormal(self):
        if self.ui.tabWidget.currentWidget() != None:
            tab = self.ui.tabWidget.currentWidget()
            filename = self.saveDialog.getSaveFileName(self, "Save file", "/home","Images (*.png)")
            tab.world.highMap.normalMap.save(filename[0])
        
    def saveHigh(self):
        if self.ui.tabWidget.currentWidget() != None:
            tab = self.ui.tabWidget.currentWidget()
            filename = self.saveDialog.getSaveFileName(self, "Save file", "/home","Images (*.png)")
            tab.world.highMap.hightMap.save(filename[0])
        
    def addTab(self):
        self.settings.ui.hide()
        pandaContainer = Tab(name = self.settings.ui.nameEdit.text(),
                             seed = self.settings.ui.seedEdit.text(),
                             rough = self.settings.rough,
                             size = self.settings.size)
        
        if self.ui.tabWidget.currentWidget() == None:
            self.ui.stackedWidget.setCurrentIndex(1)
            self.timer.start(0)
            self.changeAllState("show")
            if self.tutorial.flag == True:
                self.tutorial.ui.show()     
        self.ui.tabWidget.addTab(pandaContainer, self.settings.ui.nameEdit.text())
        self.ui.tabWidget.activateWindow()
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count()-1)
        self.tutorial.ui.raise_()
          
    def closeTab(self, index):
        self.ui.tabWidget.removeTab(index)
        if self.ui.tabWidget.currentWidget() == None:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.changeAllState("hide")
            self.timer.stop()
                
    def keyPressEvent(self, KeyEvent):
        self.pressed_keys.append(KeyEvent.key())
   
    def keyReleaseEvent(self, KeyEvent):
        self.pressed_keys.remove(KeyEvent.key())

    def mouseObserving(self):
        radHpr = ((self.mouseHpr[0]*3.14)/180, ((self.mouseHpr[0]-90)*3.14)/180)
        self.dir[0]=math.cos(radHpr[0])
        self.dir[1]=math.sin(radHpr[0])
        self.dir[2]=math.cos(radHpr[1])
        self.dir[3]=math.sin(radHpr[1])
        
    def keyHandler(self):
        for key in self.pressed_keys:
            print(self.dir)
            if key == Qt.Key_W:
                self.move((10*self.dir[1], 10*self.dir[0], 0))
            if key == Qt.Key_S:
                self.move((-10*self.dir[1], -10*self.dir[0], 0))
            if key == Qt.Key_D:
                self.move((-10*self.dir[3], -10*self.dir[2], 0))
            if key == Qt.Key_A:
                self.move((10*self.dir[3], 10*self.dir[2], 0))
                
            if key == Qt.Key_Space:
                self.move((0, 0, 2))
            if key == Qt.Key_Shift:
                self.move((0, 0, -2))
                
            if key == Qt.Key_J:
                self.rotate((0.5, 0, 0))
            if key == Qt.Key_L:
                self.rotate((-0.5, 0, 0))    
            if key == Qt.Key_I:
                self.rotate((0, 0.5, 0))
            if key == Qt.Key_K:
                self.rotate((0, -0.5, 0))
                
    def updateInfo(self):
        if self.ui.tabWidget.currentWidget() != None:
            tab = self.ui.tabWidget.currentWidget()
            pos = tab.world.cam.getPos()
            hpr = tab.world.cam.getHpr()
            seed = tab.world.highMap.seed
            
            self.ui.posLabel.setText('x: %.2f\ny: %.2f\nz: %.2f\n' % (pos.x, pos.y, pos.z))

            sides = ["north", "east", "south", "west"]
            nHpr = [hpr.x,hpr.y]
            if hpr.x > 360:
                nHpr[0] = hpr.x - (360 * (hpr.x//360))
            if hpr.x < 0:
                nHpr[0] = (-360 * (hpr.x//360)) + hpr.x
            if hpr.y > 360:
                nHpr[1] = hpr.y - (360 * (hpr.y//360))
            if hpr.y < 0:
                nHpr[1] = (-360 * (hpr.y//360)) + hpr.y
            nHpr[0] = 360 - nHpr[0]
            side = sides[int(nHpr[0]//90)]
            self.mouseHpr = nHpr
            self.ui.angleLabel.setText('x: %.2f\ny: %.2f\n (%s)\n' % (nHpr[0], nHpr[1], side))
         
            self.ui.seedLabel.setText('seed: %d' % seed)
            
    def move(self, step):
        if self.ui.tabWidget.currentWidget() != None:
            cam = self.ui.tabWidget.currentWidget().world.cam
            pos = cam.getPos()
            cam.setPos(pos[0]+step[0],pos[1]+step[1],pos[2]+step[2])
            
    def rotate(self, step):
        if self.ui.tabWidget.currentWidget() != None:
            cam = self.ui.tabWidget.currentWidget().world.cam
            hpr = cam.getHpr()
            cam.setHpr(hpr[0]+step[0],hpr[1]+step[1],hpr[2]+step[2])
            
    def changeNormalState(self):
        if self.ui.normalDock.isVisible() == True:
            self.ui.normalDock.hide()
        else:
            self.ui.normalDock.show()
            
    def changeHighState(self):
        if self.ui.highDock.isVisible() == True:
            self.ui.highDock.hide()
        else:
            self.ui.highDock.show()
    
    def changeInfoState(self):
        if self.ui.infoDock.isVisible() == True:
            self.ui.infoDock.hide()
        else:
            self.ui.infoDock.show()
            
    def changeAllState(self, t):
        if t == "show":
            self.ui.highDock.show()
            self.ui.infoDock.show()
            self.ui.normalDock.show()
        else:
            self.ui.highDock.hide()
            self.ui.infoDock.hide()
            self.ui.normalDock.hide()
            
class Tab(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Tab, self).__init__(parent)
        worldId = self.getId()
        myRender = NodePath(worldId)
        self.name = kwargs["name"]
        self.seed = kwargs["seed"]
        self.rough = kwargs["rough"]
        self.size = kwargs["size"]
        self.world = WorldGenerator(myRender, self.seed, self.rough, self.size)
 
        highImage = QImage(self.size, self.size, QImage.Format_RGB32)
        normalImage = QImage(self.size, self.size, QImage.Format_RGB32)
        for i in range(0,self.size):
            for j in range(0, self.size):
                h = self.world.highMap.hightPixels[i,j][0]
                n = self.world.highMap.normalPixels[i,j]
                highImage.setPixel(i, j, qRgb(h,h,h))
                normalImage.setPixel(i, j, qRgb(n[0],n[1],n[2]))
                
        self.highMapPixmap = QPixmap.fromImage(highImage)
        self.normalMapPixmap = QPixmap.fromImage(normalImage)
        
        self.world.bindToWindow(int(self.winId()), MainWindow.maxSize)
        
    def getId(self):
        s = "abcdefjhigklmnopqrstuvwxyz0123456789"
        k = ""
        for i in range(10):
            k+=str(s[random.randint(0,26)])
        return "W"+k

