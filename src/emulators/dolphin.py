from PyQt5.QtWidgets import QWidget

from .. import utils
from . import emulator

class EmulatorDolphin(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)



def find():
    path = utils.find_executable('dolphin-emu-nogui')

    data = {
        'name': 'Dolphin Emulator',
        'icon': '/icons/dolphin-emu.svg',
        'widget': EmulatorDolphin,
        'platforms': { 'Gamecube': [ '.gcm', '.iso', '.gcz' ], 'Wii': [ '.iso', '.gcz', '.ciso', '.wbfs' ] },
        'site': 'https://dolphin-emu.org/'
    }

    if not path is None and len(path) > 0:
        data['path'] = path

        version = utils.execute(path, '--version')
        data['version'] = ' '.join(version.split(' ')[1:])
    else:
        data['path'] = ''
        data['version'] = 'Not Found'

    return data
