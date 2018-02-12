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
        codepoint = (30 << numberOfBits) | codepoint
        numberOfBytes = 4
    elif (numberOfBits > 11):
        codepoint = (14 << numberOfBits) | codepoint
        numberOfBytes = 3
    else:
        codepoint = (6 << numberOfBits) | codepoint
        numberOfBytes = 2

    res = 0
    baseByte = 0b111111
    numberOfRightBits = 0
    for i in range(0, numberOfBytes - 1):
        bits = (codepoint & baseByte) >> numberOfRightBits
        bits = (2 << UTF_8_BASE) | bits
        codepoint = codepoint >> UTF_8_BASE
        res = (res << (8 * i)) | bits

    if (numberOfBits > 16):
        codepoint = (30 << numberOfBits) | codepoint
        numberOfBytes = 4
    elif (numberOfBits > 11):
        codepoint = (14 << numberOfBits) | codepoint
        numberOfBytes = 3
    else:
        codepoint = (6 << numberOfBits) | codepoint
        numberOfBytes = 2
    print(res)
    return res




def decode(bytes_object):
    return ord(bytes_object.decode())


def main():
    pass

if __name__ == '__main__':
    main()
