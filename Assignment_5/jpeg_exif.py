# import tags

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


def parse_exif(f):
    # do it!

    # ...

    # Don't hardcode the answer! Return your computed dictionary.
    return {'Make':['Apple']}

# print(find_jfif(open('minimal.jpg', 'rb')))
