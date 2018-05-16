import binascii
import collections
import struct

Header = collections.namedtuple('Header', 'constant manufacturer_code game_name game_type game_version side_number disk_number disk_type')

def get_header(path):
    with open(path, 'rb') as stream:
        return Header(*struct.unpack('>1x14sB3scBBBB', stream.read(24)))


def verify(path):
    return get_header(path).constant.decode('utf-8').startswith('*NINTENDO-HVC*')


def get_id(path):
    with open(path, 'rb') as stream:
        return '%08X' % ( binascii.crc32(stream.read()) & 0xffffffff, )


def get_info(path):
    header = get_header(path)

    return {
        'platform': 'FDS',
        'id': get_id(path),
        'title': '.'.join(path.split('/')[-1].split('.')[:-1]),
        'region_code': '-',
        'region': 'Japan'
    }
