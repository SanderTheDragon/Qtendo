from PyQt5.QtWidgets import QWidget

from .. import utils
from . import emulator

class EmulatorCitra(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)



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
