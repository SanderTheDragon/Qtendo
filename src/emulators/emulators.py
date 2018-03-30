import logging

from . import fceux, zsnes, mupen64plus, dolphin, citra

def add_emulator(target, emulator):
    if len(emulator['path']) > 0:
        logging.info('Found ' + emulator['name'] + ' ' + emulator['version'])
    else:
        logging.warn('Failed to find ' + emulator['name'])

    target[emulator['name']] = emulator

def find_emulators():
    result = {}

    #Search for FCEUX
    add_emulator(result, fceux.find())

    #Search for ZSNES
    add_emulator(result, zsnes.find())

    #Search for Mupen64Plus
    add_emulator(result, mupen64plus.find())

    #Search for Dolphin Emulator
    add_emulator(result, dolphin.find())

    #Search for Citra
    add_emulator(result, citra.find())

    return result
