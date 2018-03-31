from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QLabel

from ui import ui_emulator

class Emulator(QWidget, ui_emulator.Ui_Emulator):
    def __init__(self, data):
        super(Emulator, self).__init__()
        self.setupUi(self)
        self.data = data

        name = self.nameLabel.text()
        name = name.replace('{NAME}', self.data['name'])
        name = name.replace('{VERSION}', self.data['version'])
        self.nameLabel.setText(name)

        if self.data['icon'].endswith('.svg'):
            self.svgWidget = QSvgWidget()
            self.svgWidget.load(':' + self.data['icon'])
            self.svgWidget.setMaximumSize(QSize(24, 24))
            self.gridLayout.addWidget(self.svgWidget, 0, 0)
        else:
            self.iconLabel = QLabel()
            self.iconLabel.setPixmap(QPixmap(':' + self.data['icon']).scaled(24, 24))
            self.gridLayout.addWidget(self.iconLabel, 0, 0)

        self.pathLabel.setText(self.data['path'])
