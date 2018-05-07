from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

class Settings (QWidget):
    def __init__(self, parent = None):
        super(Settings, self).__init__(parent)
        self.ui = uic.loadUi("Settings.ui")
        self.rough = 500
        self.sizes = [128, 256, 512, 1024, 2048]
        self.size = self.sizes[0]
        self.text_fields = {self.ui.nameEdit:self.ui.nameValid,
                            self.ui.seedEdit:self.ui.seedValid}
  
        for field in self.text_fields:
            field.textEdited.connect(self.validator)
      
        name_r = QRegularExpression("\w{3,8}")
        name_v = QRegularExpressionValidator(name_r)
        self.ui.nameEdit.setValidator(name_v)
        
        seed_r = QRegularExpression("\d{5}|\d{0}")
        seed_v = QRegularExpressionValidator(seed_r)
        self.ui.seedEdit.setValidator(seed_v)

        self.ui.roughSlider.valueChanged.connect(self.set_rough)
        self.ui.sizeCombo.currentIndexChanged.connect(self.set_size)
        self.update_ui()
        
    def update_ui(self):
        for field in self.text_fields:
            field.setText("")
        self.ui.generateButton.setEnabled(False)
        self.ui.nameValid.hide()
        self.ui.seedValid.hide()
        
    def set_rough(self, value):
        self.rough = value
        self.ui.roughLabel.setText(str(self.rough))
        
    def set_size (self, index):
        self.size = self.sizes[index]
        print(self.size)
    def validator(self, text):
        is_valid = True
        for field in self.text_fields:
            if field.hasAcceptableInput() == False:
                self.text_fields[field].show()
                is_valid = False
            else:
                self.text_fields[field].hide()
        self.ui.generateButton.setEnabled(is_valid)
