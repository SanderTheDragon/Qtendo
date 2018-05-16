import collections
import struct
from titlecase import titlecase

Header = collections.namedtuple('Header', 'disc_id game_code region_code maker_code disc_number disc_version audio_streaming stream_buffer_size wii_magicword gamecube_magicword game_title')

def get_header(path):
    with open(path, 'rb') as stream:
        return Header(*struct.unpack('>c2sc2sBBBB14xLL64s', stream.read(96)))


def verify(path):
    return get_header(path).wii_magicword == 0x5D1C9EA3


def get_region_name(region):
    return { 'D': 'Germany', 'E': 'United States', 'F': 'France', 'I': 'Italy', 'J': 'Japan', 'K': 'Korea', 'P': 'Europe', 'R': 'Russia', 'S': 'Spain', 'T': 'Taiwan', 'U': 'Australia' }[region.decode('utf-8')]


def get_id(header):
    return header.disc_id.decode('utf-8') + header.game_code.decode('utf-8') + header.region_code.decode('utf-8') + header.maker_code.decode('utf-8')


def get_info(path):
    header = get_header(path)

    return {
        'platform': 'WII',
        'id': get_id(header),
        'title': header.game_title.decode('utf-8'),
        'region_code': header.region_code.decode('utf-8'),
        'region': get_region_name(header.region_code)
    }
