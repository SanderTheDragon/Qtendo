import binascii
import collections
import math
import struct

Type = collections.namedtuple('Type', 'magic_id')
NCCHHeader = collections.namedtuple('NCCHHeader', 'magic_id content_size partition_id maker_code version program_id product_code extended_header_size flags region_offset region_size exefs_offset exefs_size exefs_hash_size romfs_offset romfs_size romfs_hash_size')
NCSDHeader = collections.namedtuple('NCSDHeader', 'magic_id content_size media_id fs_type crypt_type offset_1 length_1 offset_2 length_2 offset_3 length_3 offset_4 length_4 offset_5 length_5 offset_6 length_6 offset_7 length_7 offset_8 length_8 add_header_size zero_offset flags_1 flags_2 flags_3 flags_4 flags_5 flags_6 flags_7 flags_8 id_1 id_2 id_3 id_4 id_5 id_6 id_7 id_8 address bitmask title_version card_revision ncch_header')

def get_header(path):
    with open(path, 'rb') as stream:
        stream.seek(0x0100)
        rom_type = Type(*struct.unpack('>4s', stream.read(4)))

        stream.seek(0x0)
        if rom_type.magic_id.decode('utf-8') == 'NCCH':
            return NCCHHeader(*struct.unpack('>256x4sIq2sH4xq48x16s32xI4x8pII8xIII4xIII68x', stream.read(0x200)))
        elif rom_type.magic_id.decode('utf-8') == 'NCSD':
            return NCSDHeader(*struct.unpack('>256x4sIqqq16I32xII8B8q48xII264xHH3564x256s', stream.read(0x1200)))
        else:
            return rom_type


def verify(path):
    return get_header(path).magic_id.decode('utf-8').startswith('NC')


def get_info(path):
    header = get_header(path)

    if header.magic_id.decode('utf-8') == 'NCCH':
        prod_code = header.product_code.decode('utf-8')
        return {
            'platform': '3DS(NCCH)',
            'id': prod_code,
            'title': '.'.join(path.split('/')[-1].split('.')[:-1]),
            'region_code': prod_code[9],
            'region': { 'E': 'United States', 'P': 'Europe', 'J': 'Japan', 'A': 'Any' }[prod_code[9]]
        }
    elif header.magic_id.decode('utf-8') == 'NCSD':
        ncch = NCCHHeader(*struct.unpack('>4sIq2sH4xq48x16s32xI4x8pII8xIII4xIII68x', header.ncch_header))
        prod_code = ncch.product_code.decode('utf-8')
        return {
            'platform': '3DS(NCSD)',
            'id': prod_code,
            'title': '.'.join(path.split('/')[-1].split('.')[:-1]),
            'region_code': prod_code[9],
            'region': { 'E': 'United States', 'P': 'Europe', 'J': 'Japan', 'A': 'Any' }[prod_code[9]]
        }

    return {}
