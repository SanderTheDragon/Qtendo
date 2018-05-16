import collections
import struct

Header = collections.namedtuple('Header', 'image_name media_format cartridge_id country_code version')

def get_header(path):
    with open(path, 'rb') as stream:
        stream.seek(0x20)
        return Header(*struct.unpack('>20s4x4s2sBB', stream.read(32)))


def verify(path):
    #Media format and country are probably good enough
    header = get_header(path)
    if any(format in header.media_format.decode('utf-8') for format in [ 'N', 'D', 'C', 'E', 'Z' ]):
        country_code = header.country_code
        if country_code in [ 0x37, 0x4E, 0x50, 0x53, 0x55 ] or (country_code > 0x41 and country_code < 0x4C) or (country_code > 0x57 and country_code < 0x59):
            return True

    return False


def get_region_name(region):
    return { '7': 'Beta', 'A': 'Asia', 'B': 'Brazil', 'C': 'China', 'D': 'Germany', 'E': 'United States', 'F': 'France', 'G': 'Gateway 64', 'H': 'The Netherlands', 'I': 'Italy', 'J': 'Japan', 'K': 'Korea', 'L': 'Gateway 64', 'N': 'Canada', 'P': 'Europe', 'S': 'Spain', 'U': 'Australia', 'W': 'Scandinavia', 'Y': 'Europe', 'Y': 'Europe' }[region.decode('utf-8')]


def get_info(path):
    header = get_header(path)

    return {
        'platform': 'N64',
        'id': header.cartridge_id.decode('utf-8'),
        'title': header.image_name.decode('utf-8'),
        'region_code': bytes([ header.country_code ]).decode('utf-8'),
        'region': get_region_name(bytes([ header.country_code ]))
    }
