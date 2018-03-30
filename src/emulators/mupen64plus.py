from PyQt5.QtWidgets import QWidget

from .. import utils
from . import emulator

class EmulatorMupen64Plus(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)



def find():
    path = utils.find_executable('mupen64plus')

    data = {
        'name': 'Mupen64Plus',
        'icon': '/icons/mupen64plus.svg',
        'widget': EmulatorMupen64Plus
    }

    if not path is None and len(path) > 0:
        data['path'] = path

        version = utils.execute(path, '--version')
        version_line = ''
        for line in version.split('\n'):
            if 'Version' in line:
                version_line = line
                break

        data['version'] = version_line.split(' ')[-1]
    else:
        data['version'] = 'Not Found'

    return data
