import subprocess
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem

from .. import utils
from ..roms import rom
from ui import ui_emulator

class Emulator(QWidget, ui_emulator.Ui_Emulator):
    def __init__(self, data):
        super(Emulator, self).__init__()
        self.setupUi(self)
        self.data = data
        self.processes = {}
        self.roms = []

        name = self.nameLabel.text()
        name = name.replace('{NAME}', self.data['name'])
        name = name.replace('{VERSION}', self.data['version'])
        name = name.replace('{URL}', self.data['site'])
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

        platformText = ''
        for platform in self.data['platforms'].keys():
            platformText += '&nbsp;&nbsp;&nbsp;&nbsp;• ' + platform + ' (' + ', '.join(self.data['platforms'][platform]) + ')<br/>'

        self.platformLabel.setText(self.platformLabel.text().replace('{PLATFORMS}', platformText))

        self.gameList.insertColumn(0)

        file_types = [ ]
        for platform in self.data['platforms'].keys():
            file_types += self.data['platforms'][platform]

        for game in utils.find_files('/home/sander/Roms', file_types):
            index = self.gameList.rowCount()

            rom_ = rom.Rom(game, self.data['platforms'])

            if rom_.is_rom:
                self.roms.append(rom_)
                self.gameList.insertRow(index)
                self.gameList.setItem(index, 0, QTableWidgetItem(game))

        self.gameList.cellDoubleClicked.connect(lambda row, column: self.launch_game(self.gameList.item(row, 0).text()))

    def launch_game(self, path):
        self.processes['path'] = subprocess.Popen([ self.data['path'] ] + self.data['arguments'] + [ path ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
