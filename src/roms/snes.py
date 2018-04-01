import collections
import os
import struct

Header = collections.namedtuple('Header', 'game_title rom_makeup rom_type rom_size sram_size creator_license_id version_number checksum_complement checksum')
def get_header(path):
    #Because smc
    file_size = os.path.getsize(path)
    diff = file_size % 1024

    #LoROM/HiROM
    starts = [ 0x7fc0, 0xffc0 ]
    with open(path, 'rb') as stream:
        for start in starts:
            stream.seek(diff + start)
            header = Header(*struct.unpack('>21sBBBB2sB2s2s', stream.read(32)))

            if (start == 0x7fc0 and header.rom_makeup & 0x00000001 == 0) or (start == 0xffc0 and header.rom_makeup & 0x00000001 == 1):
                return header

    return None

def verify(path):
    return not get_header(path) is None
