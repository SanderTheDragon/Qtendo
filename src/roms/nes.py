import binascii
import collections
import os
import struct

Header = collections.namedtuple('Header', 'constant prg_rom_size chr_rom_size flags_6 flags_7 prg_ram_size flags_9 flags_10 flags_11 flags_12 flags_13 flags_14 flags_15')

def get_header(path):
    with open(path, 'rb') as stream:
        return Header(*struct.unpack('>4sBBBBBBBBBBBB', stream.read(16)))


def verify(path):
    return get_header(path).constant.decode('utf-8').startswith('NES')


def get_variant(path):
    byte_7 = get_header(path).flags_7

    if byte_7 & 0x0C == 0x00:
        return 1 #iNes
    if byte_7 & 0x0C == 0x08:
        return 2 #NES 2.0

    return 0 #Archaic iNES


def get_region_code(header, variant):
    if variant == 0:
        return '-'
    elif variant == 1:
        if header.flags_9 & 0b00000001 == 0:
            return 'NTSC'

        return 'PAL'
    elif variant == 2:
        if header.flags_12 & 0b00000010 == 1:
            return 'UE'

        if header.flags_12 & 0b00000001 == 0:
            return 'NTSC'

        return 'PAL'


def get_id(path):
    with open(path, 'rb') as stream:
        stream.seek(16)
        crc = 0
        while True:
            data = stream.read(65536)
            if len(data) == 0:
                break

            crc = binascii.crc32(data, crc)

        return '%08X' % ( crc & 0xffffffff, )


def get_title(path):
    #Sometimes the title can be found at 03fff0
    if os.path.getsize(path) > 0x03fff0:
        with open(path, 'rb') as stream:
            stream.seek(0x03fff0)
            name = stream.read(16)
            return name[name.count(0xff):].decode('utf-8')

    return '.'.join(path.split('/')[-1].split('.')[:-1])


def get_info(path):
    header = get_header(path)
    variant = get_variant(path)
    region_code = get_region_code(header, variant)

    return {
        'platform': 'NES(' + [ 'Archaic iNES', 'iNes', 'NES 2.0' ][variant] + ')',
        'id': get_id(path),
        'title': get_title(path),
        'region_code': region_code,
        'region': { 'NTSC': 'United States', 'PAL': 'Europe', 'UE': 'Any' }[region_code]
    }
