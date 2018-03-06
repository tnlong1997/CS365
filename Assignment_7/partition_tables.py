import struct
import uuid


NULL_HEX = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


def parse_mbr(mbr_bytes):
    res = []
    for i in range(0, 4):
        entry = mbr_bytes[446 + i*16:446 + i*16 + 16]
        entry_dict = {}
        if (entry != NULL_HEX):
            t = entry[4]
            start = struct.unpack('<I', entry[8:12])[0]
            end = start + struct.unpack('<I', entry[12:16])[0] - 1
            entry_dict['type'] = hex(t)
            entry_dict['start'] = start
            entry_dict['end'] = end
            entry_dict['number'] = i
            res = res + [entry_dict]
    return res


def parse_gpt(gpt_file, sector_size=512):
    return []


# with open('usb-mbr.dd', 'rb') as f:
#     data = f.read(512)
# parse_mbr(data)
