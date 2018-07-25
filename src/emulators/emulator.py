import logging
import os
import shlex
import subprocess
import traceback
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QSettings, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QLabel, QMenu, QTableWidgetItem, QWidget
from threading import Thread

from .. import utils
from ..dialogs import emulator_settings
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

        self.settings = QSettings('SanderTheDragon', 'Qtendo')
        self.settings_prefix = 'emulation/emulator/' + self.data['name'].lower().replace(' ', '_')

        self.config_files = self.get_config_files()

        self.settings_dialog = emulator_settings.EmulatorSettingsDialog(parent=self, data=self.data)
        self.settings_dialog.accepted.connect(lambda: self.reload_settings())
        self.settings_dialog.setWindowTitle(self.data['name'] + ' Settings')

        self.ui_create()
        self.ui_connect()

        Thread(target=self.find_games, daemon=True).start()



    def ui_create(self):
        self.pathLabel.setText(self.settings.value(self.settings_prefix + '/path', self.data['path'], type=str))

        name = self.nameLabel.text()
        name = name.replace('{NAME}', self.data['name'])
        name = name.replace('{URL}', self.data['site'])

        version = self.data['version']
        if version == 'Not Found' and len(self.pathLabel.text()) > 0:
            version_ = self.data['get_version'](self.pathLabel.text())
            if len(version) > 0:
                version = version_
        self.version_pos = name.find('{VERSION}')
        name = name[:self.version_pos] + version

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

        self.gameList.setContextMenuPolicy(Qt.CustomContextMenu)


    def ui_connect(self):
        self.game_found.connect(self.add_game)
        self.games_loaded.connect(self.done_loading)

        self.gameList.customContextMenuRequested.connect(lambda position: self.game_list_context_menu(position))
        self.gameList.cellDoubleClicked.connect(lambda row, column: self.launch_game(self.gameList.item(row, 4).text()))
        self.refreshButton.pressed.connect(lambda: ( self.reset_list(), Thread(target=self.find_games, daemon=True).start() ))
        self.settingsButton.pressed.connect(lambda: ( self.settings_dialog.exec_() ))



    def find_games(self):
        file_types = [ ]
        for platform in self.data['platforms'].keys():
            file_types += self.data['platforms'][platform]

        logging.debug('[' + self.data['name'] + '] Searching for ( ' + ', '.join(file_types) + ' ) files')

        paths = self.settings.value('emulation/roms/paths', [ QDir.homePath() ], type=str)
        for path in paths:
            if not os.path.isdir(path):
                continue

            possible_games = utils.find_files(path, file_types)
            games_length = len(possible_games)
            logging.debug('[' + self.data['name'] + '] Found ' + str(games_length) + ' possible ROM' + ('s' if games_length != 1 else ''))
            for game in possible_games:
                index = self.gameList.rowCount()

                try:
                    rom_ = rom.Rom(game, self.data['platforms'])
                    if rom_.is_rom:
                        logging.debug('[' + self.data['name'] + '] \'' + game + '\' is a valid ROM')
                        self.roms.append(rom_)
                        info = rom_.module.get_info(game)
                        self.game_found.emit(index, info, game, games_length)
                    else:
                        logging.debug('[' + self.data['name'] + '] \'' + game + '\' is not a valid ROM')
                        games_length -= 1
                except:
                    traceback.print_exc()

        logging.debug('[' + self.data['name'] + '] Found ' + str(games_length) + ' ROM' + ('s' if games_length != 1 else ''))
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


    def reset_list(self):
        self.refreshButton.setEnabled(False)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)
        self.gameList.setSortingEnabled(False)
        self.gameList.setRowCount(0)
        self.roms.clear()


    def done_loading(self):
        self.gameList.setSortingEnabled(True)
        self.gameList.sortItems(1)
        self.progressBar.setVisible(False)
        self.refreshButton.setEnabled(True)


    def launch_game(self, path):
        command = self.settings.value(self.settings_prefix + '/command', '{EXEC} {ARGS} {ROM}', type=str)
        command = command.replace('{EXEC}', self.settings.value(self.settings_prefix + '/path', self.data['path'], type=str))
        command = command.replace('{ARGS}', ' '.join(self.data['arguments']))
        command = command.replace('{ROM}', shlex.quote(path))
        logging.info('[' + self.data['name'] + '] Launching: `' + command + '`')

        self.processes['path'] = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def reload_settings(self):
        self.pathLabel.setText(self.settings.value(self.settings_prefix + '/path', self.data['path'], type=str))

        name = self.nameLabel.text()
        version = self.data['get_version'](self.pathLabel.text())
        if len(version) > 0:
            name = name[:self.version_pos] + version
        self.nameLabel.setText(name)

        self.data['reload_settings']()


    def game_list_context_menu(self, position):
        menu = QMenu()
        launchAction = menu.addAction("Launch")
        menu.addSeparator()

        action = menu.exec_(self.gameList.mapToGlobal(position))

        if action == launchAction:
             self.launch_game(self.gameList.item(self.gameList.selectionModel().selectedRows()[0].row(), 4).text())
