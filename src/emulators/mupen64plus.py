import os
from PyQt5.QtWidgets import QWidget

from src import utils
from src.emulators import emulator

class EmulatorMupen64Plus(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)


    def create_settings_ui(self, ui):
        ui.fileSelect.addItems(self.get_config_files())
        ui.change_file(ui.fileSelect.currentText())



    def get_config_files(self):
        config_dir = ''
        if os.name == 'nt': #Windows
            config_dir = os.getenv('APPDATA') + '\\Mupen64Plus\\'
        else:
            if not os.getenv('XDG_CONFIG_HOME') is None and len(os.getenv('XDG_CONFIG_HOME')) > 0:
                config_dir = os.getenv('XDG_CONFIG_HOME') + '/mupen64plus/'
            else:
                config_dir = os.path.expanduser("~") + '/.config/mupen64plus/'

        return [ config_dir + 'mupen64plus.cfg' ]


    def get_config_format(self):
        return 'ini'



def find(path_hint=None):
    path = path_hint

    if path is None or not os.path.isfile(path):
        path = utils.find_executable('mupen64plus')

    data = {
        'name': 'Mupen64Plus',
        'icon': '/icons/mupen64plus.svg',
        'widget': EmulatorMupen64Plus,
        'platforms': { 'Nintendo 64': [ '.n64', '.z64', '.v64' ] },
        'site': 'http://mupen64plus.org/',
        'arguments': [ ],
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
    version = utils.execute(path, '--version')
    version_line = ''
    for line in version.split('\n'):
        if 'Version' in line:
            version_line = line
            break

    return version_line.split(' ')[-1]
