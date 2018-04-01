import collections
import struct

Header = collections.namedtuple('Header', 'constant prg_rom_size chr_rom_size flags_6 flags_7 prg_ram_size flags_9 flags_10')
def get_header(path):
    with open(path, 'rb') as stream:
        return Header(*struct.unpack('>4sBBBBBBB5x', stream.read(16)))

def verify(path):
    return get_header(path).constant.decode('utf-8').startswith('NES')
