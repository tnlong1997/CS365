import tags
import struct


class ExifParseError(Exception):
    def init(__self__):
        pass


def carve(f, start, end):
    # return the bytes

    # here is an example that just returns the entire range of bytes:
    f.seek(start)
    return f.read(end - start + 1)


def find_jfif(f, max_length=None):
    # do some stuff

    # then return a possibly-empty sequence of pairs

    # here's an example that just returns the start and end of the file
    # without parsing
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
    if fmat == 1:
        return struct.unpack('>B', data[0:1])[0]
    elif fmat == 2:
        return bytes.decode(data[0:len(data) - 1])
    elif fmat == 3:
        return struct.unpack('>H', data[0:len(data)])[0]
    elif fmat == 4:
        return struct.unpack('>L', data[0:4])[0]
    elif fmat == 5:
        (numerator, denominator) = struct.unpack('>LL', data[0:8])
        return '%s/%s' % (numerator, denominator)
    elif fmat == 7:
        value = struct.unpack('>%dB' % len(data), data[0:len(data)])
        return "".join("%.2x" % x for x in value)


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
            tag = f.read(2)
            index += 2
            name = tags.TAGS[struct.unpack('>H', tag)[0]]
            fmat = f.read(2)
            index += 2
            fmat = struct.unpack('>H', fmat)[0]
            nComponents = f.read(4)
            index += 4
            nComponents = struct.unpack('>I', nComponents)[0]
            lData = nComponents * BYTE_PER_COMPONENTS[fmat]
            data = None
            # print(name)
            if (lData < 4):
                data = f.read(lData)
                f.read(4 - lData)
                index += 4
                # print(fmat, data)
                data = get_data_big_endian(data, fmat)
            elif (lData == 4):
                data = f.read(4)
                index += 4
                # print(fmat, data)
                data = get_data_big_endian(data, fmat)
            else:
                data = f.read(4)
                index += 4
                f.seek(endian_index + struct.unpack('>I', data)[0])
                data = f.read(lData)
                # print(fmat, data)
                data = get_data_big_endian(data, fmat)
            if name in res:
                res[name].append(data)
            else:
                res[name] = [data]
            f.seek(index)
        ifd_offsets = f.read(4)
        ifd_offsets = struct.unpack('>I', ifd_offsets)[0]
    return res, f


def get_data_little_endian(data, fmat):
    return data


def get_exif_little_endian(res, f, endian_index):
    ifd_offsets = f.read(4)
    print(ifd_offsets)
    ifd_offsets = struct.unpack('<I', ifd_offsets)[0]
    while (ifd_offsets != 0):
        f.seek(endian_index + ifd_offsets)
        index = endian_index + ifd_offsets
        numberOfEntries = f.read(2)
        print(numberOfEntries)
        index += 2
        numberOfEntries = struct.unpack('<H', numberOfEntries)[0]
        for entry in range(0, numberOfEntries):
            tag = f.read(2)
            index += 2
            # print(tag)
            name = tags.TAGS[struct.unpack('<H', tag)[0]]
            fmat = f.read(2)
            index += 2
            fmat = struct.unpack('<H', fmat)[0]
            nComponents = f.read(4)
            index += 4
            nComponents = struct.unpack('<I', nComponents)[0]
            lData = nComponents * BYTE_PER_COMPONENTS[fmat]
            data = None
            # print(name)
            if (lData < 4):
                data = f.read(lData)
                f.read(4 - lData)
                index += 4
                # print(fmat, data)
                # print(data)
                data = get_data_little_endian(data, fmat)
            elif (lData == 4):
                data = f.read(4)
                index += 4
                # print(fmat, data)
                # print(data)
                data = get_data_little_endian(data, fmat)
            else:
                data = f.read(4)
                index += 4
                f.seek(endian_index + struct.unpack('>I', data)[0])
                # print(data)
                data = f.read(lData)
                # print(fmat, data)
                data = get_data_little_endian(data, fmat)
            if name in res:
                res[name].append(data)
            else:
                res[name] = [data]
            f.seek(index)
        ifd_offsets = f.read(4)
        ifd_offsets = struct.unpack('>I', ifd_offsets)[0]
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
                # print(exif_tag)
                if (exif_tag != b'Exif\x00\x00'):
                    byte = f.read(1)
                    index += 1
                else:
                    endian = f.read(2)
                    # print(endian)
                    index += 2
                    endian_index = index - 1
                    f.read(2)
                    if (endian == b'MM'):
                        res, f = get_exif_big_endian(res, f, endian_index)
                    else:
                        res, f = get_exif_little_endian(res, f, endian_index)
                    byte = f.read(1)
        else:
            byte = f.read(1)
            index += 1
    if res == {}:
        raise ExifParseError()
    return res


parse_exif(open('leaves.jpg', 'rb'))
