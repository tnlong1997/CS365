import tags
import struct


class ExifParseError(Exception):
    def init(__self__):
        pass


def carve(f, start, end):
    f.seek(start)
    return f.read(end - start + 1)


def find_jfif(f, max_length=None):
    res = []
    index = 0
    soiList = []
    eoiList = []
    byte = f.read(1)
    while len(byte) != 0:
        if (byte == b'\xff'):
            byte = f.read(1)
            index += 1
            if byte == b'\xd8':
                soiList = soiList + [index - 1]
            elif byte == b'\xd9':
                eoiList = eoiList + [index]
        else:
            index += 1
            byte = f.read(1)

    for soi in soiList:
        for eoi in eoiList:
            if (max_length is not None):
                if (eoi - soi + 1 <= max_length) and (soi < eoi):
                    res = res + [(soi, eoi)]
            else:
                if (soi < eoi):
                    res = res + [(soi, eoi)]
    return res


BYTE_PER_COMPONENTS = [0, 1, 1, 2, 4, 8, 1, 1, 2, 4, 8, 4, 8]


def get_data_big_endian(data, fmat):
    res = []
    if fmat == 1:
        return struct.unpack('>B', data[0:1])[0]
    elif fmat == 2:
        return bytes.decode(data[0:len(data) - 1])
    elif fmat == 3:
        for i in range(0, len(data)//2, 2):
            val = struct.unpack('>H', data[i*2:i*2 + 2])[0]
            if (val != 0):
                res.append(val)
        return res
    elif fmat == 4:
        return struct.unpack('>L', data[0:4])[0]
    elif fmat == 5:
        (numerator, denominator) = struct.unpack('>LL', data[0:8])
        return '%s/%s' % (numerator, denominator)
    elif fmat == 7:
        value = struct.unpack('>%dB' % len(data), data[0:len(data)])
        return "".join("%.2x" % x for x in value)
    else:
        return None


def get_exif_big_endian(res, f, endian_index):
    ifd_offsets = f.read(4)
    ifd_offsets = struct.unpack('>I', ifd_offsets)[0]
    while (ifd_offsets != 0):
        f.seek(endian_index + ifd_offsets)
        index = endian_index + ifd_offsets
        numberOfEntries = f.read(2)
        index += 2
        numberOfEntries = struct.unpack('>H', numberOfEntries)[0]
        for entry in range(0, numberOfEntries):
            index += 12
            tag = f.read(2)
            tag = struct.unpack('>H', tag)[0]
            if (tag not in tags.TAGS):
                f.read(10)
                continue
            name = tags.TAGS[tag]
            fmat = f.read(2)
            fmat = struct.unpack('>H', fmat)[0]
            nComponents = f.read(4)
            nComponents = struct.unpack('>I', nComponents)[0]
            lData = nComponents * BYTE_PER_COMPONENTS[fmat]
            data = f.read(4)
            if (lData <= 4):
                data = get_data_big_endian(data, fmat)
            else:
                f.seek(endian_index + struct.unpack('>I', data)[0])
                data = f.read(lData)
                data = get_data_big_endian(data, fmat)
            if name in res:
                if (fmat == 3):
                    res[name] = res[name] + data
                else:
                    res[name].append(data)
            else:
                if (fmat == 3):
                    res[name] = data
                else:
                    res[name] = [data]
            f.seek(index)
        ifd_offsets = f.read(4)
        ifd_offsets = struct.unpack('>I', ifd_offsets)[0]
    return res, f


def get_data_little_endian(data, fmat):
    res = []
    if fmat == 1:
        return struct.unpack('<B', data[0:1])[0]
    elif fmat == 2:
        return bytes.decode(data[0:len(data) - 1])
    elif fmat == 3:
        for i in range(0, len(data)//2, 2):
            val = struct.unpack('<H', data[i*2:i*2 + 2])[0]
            if (val != 0):
                res.append(val)
        return res
    elif fmat == 4:
        return struct.unpack('<L', data[0:4])[0]
    elif fmat == 5:
        (numerator, denominator) = struct.unpack('<LL', data[0:8])
        return '%s/%s' % (numerator, denominator)
    elif fmat == 7:
        value = struct.unpack('<%dB' % len(data), data[0:len(data)])
        return "".join("%.2x" % x for x in value)
    else:
        return None


def get_exif_little_endian(res, f, endian_index):
    ifd_offsets = f.read(4)
    ifd_offsets = struct.unpack('<I', ifd_offsets)[0]
    while (ifd_offsets != 0):
        f.seek(endian_index + ifd_offsets)
        index = endian_index + ifd_offsets
        numberOfEntries = f.read(2)
        index += 2
        numberOfEntries = struct.unpack('<H', numberOfEntries)[0]
        for entry in range(0, numberOfEntries):
            index += 12
            tag = f.read(2)
            tag = struct.unpack('<H', tag)[0]
            if (tag not in tags.TAGS):
                f.read(10)
                continue
            name = tags.TAGS[tag]
            fmat = f.read(2)
            fmat = struct.unpack('<H', fmat)[0]
            nComponents = f.read(4)
            nComponents = struct.unpack('<I', nComponents)[0]
            lData = nComponents * BYTE_PER_COMPONENTS[fmat]
            data = f.read(4)
            if (lData <= 4):
                data = get_data_little_endian(data, fmat)
            else:
                f.seek(endian_index + struct.unpack('<I', data)[0])
                data = f.read(lData)
                data = get_data_little_endian(data, fmat)
            if name in res:
                if (fmat == 3):
                    res[name] = res[name] + data
                else:
                    res[name].append(data)
            else:
                if (fmat == 3):
                    res[name] = data
                else:
                    res[name] = [data]
            f.seek(index)
        ifd_offsets = f.read(4)
        ifd_offsets = struct.unpack('<I', ifd_offsets)[0]
    return res, f


def parse_exif(f):
    index = 0
    byte = f.read(1)
    res = {}
    while len(byte) != 0:
        if (byte == b'\xff'):
            byte = f.read(1)
            index += 1
            if (byte == b'\xe1'):
                size = f.read(2)
                index += 2
                size = struct.unpack('>H', size)[0]
                exif_tag = f.read(6)
                index += 6
                if (exif_tag != b'Exif\x00\x00'):
                    byte = f.read(1)
                    index += 1
                else:
                    endian = f.read(2)
                    index += 2
                    endian_index = index - 1
                    f.read(2)
                    if (endian == b'MM'):
                        res, f = get_exif_big_endian(res, f, endian_index)
                    else:
                        res, f = get_exif_little_endian(res, f, endian_index)
                    f.seek(endian_index + size - 6)
                    byte = f.read(1)
                    index += 1
        else:
            byte = f.read(1)
            index += 1
    if res == {}:
        raise ExifParseError()
    return res
