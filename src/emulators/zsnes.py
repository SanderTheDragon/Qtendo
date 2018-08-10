import os
from PyQt5.QtWidgets import QWidget

from src import utils
from src.emulators import emulator

class EmulatorZsnes(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)


    def create_settings_ui(self, ui):
        ui.fileSelect.addItems(self.get_config_files())
        ui.change_file(ui.fileSelect.currentText())



    def get_config_files(self):
        if os.name == 'nt': #Windows
            config_dir = os.path.dirname(self.data['path']) + '\\'
        else:
            config_dir = os.path.expanduser("~") + '/.zsnes/'

        return [ config_dir + 'zinput.cfg', config_dir + 'zmovie.cfg', config_dir + ('zsnesw.cfg' if os.name == 'nt' else 'zsnesl.cfg') ]


    def get_config_format(self):
        return 'ini' #Not actual INI, but good enough for formatting



def find(path_hint=None):
    path = path_hint

    if path is None or not os.path.isfile(path):
        path = utils.find_executable('zsnes')

    data = {
        'name': 'ZSNES',
        'icon': '/icons/zsnes.png',
        'widget': EmulatorZsnes,
        'platforms': { 'Super Nintendo Entertainment System': [ '.sfc', '.smc' ] },
        'site': 'http://zsnes.com/',
        'arguments': [ '-m' ],
        'get_version': get_version
    }

    if len(path) > 0:
        data['path'] = path
        data['version'] = get_version(path)
    else:
        data['path'] = ''
        data['version'] = 'Not Found'

    return data


def get_version(path):
    #Not the best way to get the version
    version = utils.execute(path, '-m')
    return version.split(' ')[1][:-1]
