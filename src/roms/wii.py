import collections
import struct

IsoHeader = collections.namedtuple('IsoHeader', 'disc_id game_code region_code maker_code disc_number disc_version audio_streaming stream_buffer_size wii_magicword gamecube_magicword game_title')
CisoHeader = collections.namedtuple('CisoHeader', 'magic disc_id game_code region_code maker_code game_title')
BackupHeader = collections.namedtuple('BackupHeader', 'magic disc_id game_code region_code maker_code game_title')

def get_header(path):
    with open(path, 'rb') as stream:
        if path.endswith('.iso'):
            return IsoHeader(*struct.unpack('>c2sc2sBBBB14xLL64s', stream.read(96)))
        elif path.endswith('.ciso'):
            return CisoHeader(*struct.unpack('>4s32764xc2sc2s26x64s', stream.read(32864)))
        elif path.endswith('.wbfs'):
            return BackupHeader(*struct.unpack('>4s508xc2sc2s26x64s', stream.read(608)))


def verify(path):
    if path.endswith('.iso'):
        return get_header(path).wii_magicword == 0x5D1C9EA3
    elif path.endswith('.ciso'):
        return get_header(path).magic.decode('utf-8').startswith('CISO')
    elif path.endswith('.wbfs'):
        return get_header(path).magic.decode('utf-8').startswith('WBFS')



def get_region_name(region):
    return { 'D': 'Germany', 'E': 'United States', 'F': 'France', 'I': 'Italy', 'J': 'Japan', 'K': 'Korea', 'P': 'Europe', 'R': 'Russia', 'S': 'Spain', 'T': 'Taiwan', 'U': 'Australia' }[region.decode('utf-8')]


def get_id(header):
    return header.disc_id.decode('utf-8') + header.game_code.decode('utf-8') + header.region_code.decode('utf-8') + header.maker_code.decode('utf-8')


def get_info(path):
    header = get_header(path)

    return {
        'platform': 'WII(' + { 'IsoHeader': 'ISO', 'CisoHeader': 'CISO', 'BackupHeader': 'WBFS' }[type(header).__name__] + ')',
        'id': get_id(header),
        'title': header.game_title.decode('utf-8'),
        'region_code': header.region_code.decode('utf-8'),
        'region': get_region_name(header.region_code)
    }
