from PyQt5.QtWidgets import QWidget

from .. import utils
from . import emulator

class EmulatorZsnes(emulator.Emulator):
    def __init__(self, data):
        emulator.Emulator.__init__(self, data)



def find():
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
