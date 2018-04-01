import collections
import struct

Header = collections.namedtuple('Header', 'disc_id game_code region_code maker_code disc_number disc_version audio_streaming stream_buffer_size wii_magicword gamecube_magicword game_title')
def get_header(path):
    with open(path, 'rb') as stream:
        return Header(*struct.unpack('>c2sc2sBBBB14xLL64s', stream.read(96)))

def verify(path):
    return get_header(path).gamecube_magicword == 0xC2339F3D
