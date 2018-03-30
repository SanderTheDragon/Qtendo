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
        'widget': EmulatorCitra
    }

    if not path is None and len(path) > 0:
        data['path'] = path

        version = utils.execute(path, '--version')
        data['version'] = ' '.join(version.split('\n')[-1].split(' ')[1:])
    else:
        data['version'] = 'Not Found'

    return data
