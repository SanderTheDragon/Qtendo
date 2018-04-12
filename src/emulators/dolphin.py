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
