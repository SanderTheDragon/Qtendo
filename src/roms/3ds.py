import binascii
import collections
import struct

Type = collections.namedtuple('Type', 'magic_id')
NCCHHeader = collections.namedtuple('NCCHHeader', 'magic_id content_size partition_id maker_code version program_id product_code extended_header_size flags region_offset region_size exefs_offset exefs_size exefs_hash_size romfs_offset romfs_size romfs_hash_size')
NCSDHeader = collections.namedtuple('NCSDHeader', 'magic_id content_size media_id fs_type crypt_type offset')

def get_header(path):
    with open(path, 'rb') as stream:
        stream.seek(0x0100)
        rom_type = Type(*struct.unpack('>4s', stream.read(4)))

        stream.seek(0x0100)
        if rom_type.magic_id.decode('utf-8') == 'NCCH':
            return NCCHHeader(*struct.unpack('>4sIq2sH4xq48x16s32xI4x8pII8xIII4xIII', stream.read(188)))
        elif rom_type.magic_id.decode('utf-8') == 'NCSD':
            return NCSDHeader(*struct.unpack('>4sIqqqq', stream.read(40)))
        else:
            return rom_type


def verify(path):
    return get_header(path).magic_id.decode('utf-8').startswith('NC')


def get_info(path):
    header = get_header(path)

    if header.magic_id.decode('utf-8') == 'NCCH':
        return {
            'platform': '3DS(NCCH)',
            'id': header.product_code.decode('utf-8'),
            'title': '.'.join(path.split('/')[-1].split('.')[:-1]),
            'region_code': '?',
            'region': '?'
        }
    elif header.magic_id.decode('utf-8') == 'NCSD':
        return {
            'platform': '3DS(NCSD)',
            'id': '?',
            'title': '.'.join(path.split('/')[-1].split('.')[:-1]),
            'region_code': '?',
            'region': '?'
        }

    return {}
