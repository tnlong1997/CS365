import struct


UTF_8_BASE = 6


def count_number_of_bits(dec):
    count = 0
    while dec > 0:
        count += 1
        dec = dec // 2
    return count


def encode(codepoint):
    if codepoint < 128:
        return bytes([codepoint])

    numberOfBits = count_number_of_bits(codepoint)

    if (numberOfBits > 16):
        numberOfBytes = 4
    elif (numberOfBits > 11):
        numberOfBytes = 3
    else:
        numberOfBytes = 2

    res = None
    baseByte = 63
    numberOfRightBits = 0
    for i in range(0, numberOfBytes - 1):
        bits = (codepoint & baseByte) >> numberOfRightBits
        bits = (2 << UTF_8_BASE) | bits
        codepoint = codepoint >> UTF_8_BASE
        if res is None:
            res = struct.pack('>B', bits)
        else:
            res = struct.pack('>B', bits) + res

    if (numberOfBits > 16):
        res = struct.pack('>B', (30 << 3) | codepoint) + res
    elif (numberOfBits > 11):
        res = struct.pack('>B', (14 << 4) | codepoint) + res
    else:
        res = struct.pack('>B', (6 << 5) | codepoint) + res

    return res


def decode(bytes_object):
    if len(bytes_object) == 1:
        return bytes_object[0]

    temp = 0
    res = 0
    base = 0
    for i in range(len(bytes_object) - 1, 0, -1):
        temp = bytes_object[i] & 63
        res = res | (temp << (base * 6))
        base += 1

    if len(bytes_object) == 4:
        res = res | ((bytes_object[0] & 7) << 18)
    elif len(bytes_object) == 3:
        res = res | ((bytes_object[0] & 15) << 12)
    else:
        res = res | ((bytes_object[0] & 31) << 6)

    return res


def main():
    pass


if __name__ == '__main__':
    main()
