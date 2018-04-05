import binascii
import collections
import os
import struct

Header = collections.namedtuple('Header', 'game_title rom_makeup rom_type rom_size ram_size country_code creator_license_id version_number checksum_complement checksum')
def get_header(path):
    #Because smc
    file_size = os.path.getsize(path)
    diff = file_size % 1024

    #LoROM/HiROM
    starts = [ 0x7fc0, 0xffc0 ]
    with open(path, 'rb') as stream:
        for start in starts:
            stream.seek(diff + start)
            header = Header(*struct.unpack('>21sBBBBBBB2s2s', stream.read(32)))

            if (start == 0x7fc0 and header.rom_makeup & 0b00000001 == 0) or (start == 0xffc0 and header.rom_makeup & 0b00000001 == 1):
                fast = header.rom_makeup & 0b00110000 == 0b00110000
                ex = False
                if fast and (header.rom_makeup & 0b00000111 == 0b00000101 or header.rom_makeup & 0b00000111 == 0b00000010):
                    fast = False
                    ex = True

                type = 'Ex' if ex else ''
                type += { 0x7fc0: 'LoROM', 0xffc0: 'HiROM' }[start]
                type += ' + FastROM' if fast else ''
                return ( type, header )

    return None

def verify(path):
    return not get_header(path) is None

def get_id(path):
    with open(path, 'rb') as stream:
        stream.seek(32)
        crc = 0
        while True:
            data = stream.read(65536)
            if len(data) == 0:
                break

            crc = binascii.crc32(data, crc)

        return '%08X' % ( crc & 0xffffffff, )

def get_region(header):
    countries = [ 'Japan', 'United States', 'Europe', 'Sweden', 'Finland', 'Denmark', 'France', 'The Netherlands', 'Spain', 'Germany', 'Italy', 'China', 'Korea' ]
    if header.country_code >= len(countries):
        return ( '-', '-' )

    country = countries[header.country_code]
    video = 'PAL'
    if header.country_code in [ 0x00, 0x01, 0x0d ]:
        video = 'NTSC'

    return ( video, country )

def get_info(path):
    ( type, header ) = get_header(path)
    ( region, region_name ) = get_region(header)

    return {
        'platform': 'SNES(' + type + ')',
        'id': get_id(path),
        'title': header.game_title.decode('utf-8'),
        'region_code': region,
        'region': region_name
    }
