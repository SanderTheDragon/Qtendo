from PyQt5.QtWidgets import QWidget

from .. import utils
from . import emulator

class EmulatorFceux(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)



def find():
    path = utils.find_executable('fceux')

    data = {
        'name': 'FCEUX',
        'icon': '/icons/fceux.png',
        'widget': EmulatorFceux,
        'platforms': { 'Nintendo Entertainment System': [ '.nes', '.unf', '.unif' ], 'Famicom Disk System': [ '.fds', '.unf', '.unif' ] },
        'site': 'http://www.fceux.com/web/home.html'
    }

    if not path is None and len(path) > 0:
        data['path'] = path

        #No way to get version without opening a window
        data['version'] = ''
    else:
        data['path'] = ''
        data['version'] = 'Not Found'

    return data
