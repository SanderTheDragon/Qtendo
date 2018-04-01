import collections
import struct

Header = collections.namedtuple('Header', 'constant manufacturer_code game_name game_type game_version side_number disk_number disk_type')
def get_header(path):
    with open(path, 'rb') as stream:
        return Header(*struct.unpack('>1x14sB3scBBBB', stream.read(24)))

def verify(path):
    return get_header(path).constant.decode('utf-8').startswith('*NINTENDO-HVC*')
