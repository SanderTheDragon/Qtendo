from PyQt5.QtCore import QSize
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QDialog

from src import system
from ui import ui_about

class AboutDialog(QDialog, ui_about.Ui_About):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)

        self.nameLabel.setText(self.nameLabel.text().replace('{VERSION}', system.get_version_string()))

        self.mupen64plusLogo = QSvgWidget()
        self.mupen64plusLogo.load(':/icons/mupen64plus.svg')
        self.mupen64plusLogo.setMaximumSize(QSize(32, 32))
        self.gridLayout_7.addWidget(self.mupen64plusLogo, 0, 0, 2, 1)

        self.dolphinLogo = QSvgWidget()
        self.dolphinLogo.load(':/icons/dolphin-emu.svg')
        self.dolphinLogo.setMaximumSize(QSize(32, 32))
        self.gridLayout_4.addWidget(self.dolphinLogo, 0, 0, 2, 1)

        self.citraLogo = QSvgWidget()
        self.citraLogo.load(':/icons/citra.svg')
        self.citraLogo.setMaximumSize(QSize(32, 32))
        self.gridLayout_8.addWidget(self.citraLogo, 0, 0, 2, 1)
