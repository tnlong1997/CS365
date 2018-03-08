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
    res = []
    gpt_file.read(sector_size)
    header = gpt_file.read(sector_size)
    partion_index = struct.unpack('<Q', header[72:80])[0]
    numberOfEntries = struct.unpack('<I', header[80:84])[0]
    entrySize = struct.unpack('<I', header[84:88])[0]
    for i in range(2, partion_index):
        gpt_file.read(sector_size)
    for i in range(0, numberOfEntries):
        entry = gpt_file.read(entrySize)
        entry_dict = {}
        if (entry != (entrySize * b'\x00')):
            t = entry[0:16]
            start = struct.unpack('<Q', entry[32:40])[0]
            end = struct.unpack('<Q', entry[40:48])[0]
            entry_dict['start'] = start
            entry_dict['end'] = end
            entry_dict['type'] = uuid.UUID(bytes_le=t)
            entry_dict['number'] = i
            name = ''
            for i in range(56, 128, 2):
                if (entry[i] != 0):
                    name = name + chr(entry[i])
                else:
                    break
            entry_dict['name'] = name
            res = res + [entry_dict]
    return res


with open('disk-image.dd', 'rb') as f:
    parse_gpt(f, 512)
