import os
from PyQt5.QtWidgets import QWidget

from .. import utils
from . import emulator

class EmulatorCitra(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)


    def create_settings_ui(self, ui):
        ui.fileSelect.addItems(self.get_config_files())
        ui.change_file(ui.fileSelect.currentText())



    def get_config_files(self):
        config_dir = ''
        if os.name == 'nt': #Windows
            if os.path.isdir(os.path.dirname(self.data['path']) + '\\user\\config'):
                config_dir = os.path.dirname(self.data['path']) + '\\user\\config\\'
            else:
                config_dir = os.getenv('APPDATA') + '\\Citra\\config\\'
        else:
            if os.path.isdir(os.path.dirname(self.data['path']) + '/user/config'):
                config_dir = os.path.dirname(self.data['path']) + '/user/config/'
            else:
                if not os.getenv('XDG_CONFIG_HOME') is None and len(os.getenv('XDG_CONFIG_HOME')) > 0:
                    config_dir = os.getenv('XDG_CONFIG_HOME') + '/citra-emu/'
                else:
                    config_dir = os.path.expanduser("~") + '/.config/citra-emu/'

        return [ config_dir + 'qt-config.ini', config_dir + 'sdl2-config.ini' ]


    def get_config_format(self):
        return 'ini'



def find():
    path = utils.find_executable('citra')

    data = {
        'name': 'Citra',
        'icon': '/icons/citra.svg',
        'widget': EmulatorCitra,
        'platforms': { '3DS': [ '.3ds' ] },
        'site': 'https://citra-emu.org/',
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
    return ' '.join(version.split('\n')[-1].split(' ')[1:])
