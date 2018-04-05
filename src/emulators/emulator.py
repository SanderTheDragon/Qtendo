import subprocess
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem
from threading import Thread

from .. import utils
from ..roms import rom
from ui import ui_emulator

class Emulator(QWidget, ui_emulator.Ui_Emulator):
    game_found = QtCore.pyqtSignal(int, dict, str, int)
    games_loaded = QtCore.pyqtSignal()

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
        self.gameList.insertColumn(1)
        self.gameList.insertColumn(2)
        self.gameList.insertColumn(3)
        self.gameList.insertColumn(4)
        self.gameList.setHorizontalHeaderLabels([ 'Platform', 'ID', 'Title', 'Region', 'Path' ])

        self.game_found.connect(self.add_game)
        self.games_loaded.connect(self.done_loading)
        Thread(target=self.find_games).start()

        self.gameList.cellDoubleClicked.connect(lambda row, column: self.launch_game(self.gameList.item(row, 4).text()))

    def find_games(self):
        file_types = [ ]
        for platform in self.data['platforms'].keys():
            file_types += self.data['platforms'][platform]

        possible_games = utils.find_files('/', file_types)
        games_length = len(possible_games)
        for game in possible_games:
            index = self.gameList.rowCount()

            rom_ = rom.Rom(game, self.data['platforms'])
            if rom_.is_rom:
                self.roms.append(rom_)
                info = rom_.module.get_info(game)
                self.game_found.emit(index, info, game, games_length)
            else:
                games_length -= 1

        self.games_loaded.emit()

    def add_game(self, index, info, path, count):
        self.gameList.insertRow(index)

        if len(info.keys()) > 0:
            self.gameList.setItem(index, 0, QTableWidgetItem(info['platform']))
            self.gameList.setItem(index, 1, QTableWidgetItem(info['id']))
            self.gameList.setItem(index, 2, QTableWidgetItem(info['title']))
            self.gameList.setItem(index, 3, QTableWidgetItem(info['region'] + '(' + info['region_code'] + ')'))

        self.gameList.setItem(index, 4, QTableWidgetItem(path))
        self.gameList.resizeColumnsToContents()

        self.progressBar.setValue(int(100.0 / float(count) * float(index + 1)))

    def done_loading(self):
        self.gameList.sortItems(1)
        self.progressBar.setVisible(False)

    def launch_game(self, path):
        self.processes['path'] = subprocess.Popen([ self.data['path'] ] + self.data['arguments'] + [ path ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
