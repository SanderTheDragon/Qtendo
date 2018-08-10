import os
from PyQt5.QtWidgets import QWidget

from src import utils
from src.emulators import emulator

class EmulatorFceux(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)


    def create_settings_ui(self, ui):
        ui.fileSelect.addItems(self.get_config_files())
        ui.change_file(ui.fileSelect.currentText())



    def get_config_files(self):
        config_dir = ''
        if os.name == 'nt': #Windows
            config_dir = os.path.dirname(self.data['path']) + '\\'
        else:
            config_dir = os.path.expanduser("~") + '/.fceux/'

        return [ config_dir + 'fceux.cfg' ]


    def get_config_format(self):
        return 'ini' #Not actual INI, but good enough for formatting



def find(path_hint=None):
    path = path_hint

    if path is None or not os.path.isfile(path):
        path = utils.find_executable('fceux')

    data = {
        'name': 'FCEUX',
        'icon': '/icons/fceux.png',
        'widget': EmulatorFceux,
        'platforms': { 'Nintendo Entertainment System': [ '.nes', '.unf', '.unif' ], 'Famicom Disk System': [ '.fds', '.unf', '.unif' ] },
        'site': 'http://www.fceux.com/web/home.html',
        'arguments': [ '--nogui', '1', '--noframe', '0' ],
        'get_version': get_version
    }

    if not path is None and len(path) > 0:
        data['path'] = path
        data['version'] = get_version(path)
    else:
        data['path'] = ''
        data['version'] = 'Not Found'

    return data


def get_version(path):
    #No way to get version without opening a window
    return ''
