import os
from PyQt5.QtWidgets import QWidget

from .. import utils
from . import emulator

class EmulatorDolphin(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)


    def create_settings_ui(self, ui):
        ui.fileSelect.addItems(self.get_config_files())
        ui.change_file(ui.fileSelect.currentText())



    def get_config_files(self):
        config_dir = ''
        if os.name == 'nt': #Windows
            import winreg
            hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Dolphin Emulator')

            if os.path.isdir(os.path.dirname(self.data['path']) + '\\User\\Config'):
                config_dir = os.path.dirname(self.data['path']) + '\\User\\Config\\'
            elif os.path.isdir(os.path.expanduser('~\\Documents') + '\\Dolphin Emulator\\Config'):
                config_dir = os.path.expanduser('~\\Documents') + '\\Dolphin Emulator\\Config\\'
            elif not _winreg.QueryValueEx(hkey, 'UserConfigPath')[0] is None: #Could not find what happens if this fails
                config_dir = _winreg.QueryValueEx(hkey, 'UserConfigPath')[0]
            else:
                config_dir = os.path.dirname(self.data['path']) + '\\User\\Config\\'

            winreg.CloseKey(hkey)
        else:
            if os.path.isdir(os.path.dirname(self.data['path']) + '/user/Config'):
                config_dir = os.path.dirname(self.data['path']) + '/user/Config/'
            else:
                if not os.getenv('XDG_CONFIG_HOME') is None and len(os.getenv('XDG_CONFIG_HOME')) > 0:
                    config_dir = os.getenv('XDG_CONFIG_HOME') + '/dolphin-emu/'
                else:
                    config_dir = os.path.expanduser("~") + '/.config/dolphin-emu/'

        return [ config_dir + 'Debugger.ini', config_dir + 'Dolphin.ini', config_dir + 'GCPadNew.ini', config_dir + 'GFX.ini', config_dir + 'Hotkeys.ini', config_dir + 'Logger.ini', config_dir + 'WiimoteNew.ini' ]


    def get_config_format(self):
        return 'ini'



def find():
    path = utils.find_executable('dolphin-emu-nogui')

    data = {
        'name': 'Dolphin Emulator',
        'icon': '/icons/dolphin-emu.svg',
        'widget': EmulatorDolphin,
        'platforms': { 'Gamecube': [ '.gcm', '.iso', '.gcz' ], 'Wii': [ '.iso', '.gcz', '.ciso', '.wbfs' ] },
        'site': 'https://dolphin-emu.org/',
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
    return ' '.join(version.split(' ')[1:])
