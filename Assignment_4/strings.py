import argparse


def print_strings(file_obj, encoding, min_len):
    # Right now all this function does is print its arguments.
    # You'll need to replace that code with code that actually finds and prints the strings!
    if encoding == 's':
        currentString = ''
        count = 0
        byte = file_obj.read(1)
        while (len(byte) != 0):
            temp = ord(byte)
            if temp > 31 and temp < 127:
                count += 1
                currentString = currentString + chr(temp)
            else:
                if (count >= min_len):
                    print(currentString)
                currentString = ''
                count = 0
            byte = file_obj.read(1)
        if (count >= min_len):
            print(currentString)
    else:
        currentString = ''
        count = 0
        byte = file_obj.read(2)
        while (len(byte) == 2):
            if (encoding == 'b'):
                byte1 = byte[0]
                byte2 = byte[1]
            else:
                byte1 = byte[1]
                byte2 = byte[0]
            if (byte1 == 0 and 31 < byte2 < 127):
                count += 1
                currentString = currentString + chr(byte2)
            else:
                if (count >= min_len):
                    print(currentString)
                currentString = ''
                count = 0
            byte = file_obj.read(2)
        if (count >= min_len):
            print(currentString)



def main():
    parser = argparse.ArgumentParser(description='Print the printable strings from a file.')
    parser.add_argument('filename')
    parser.add_argument('-n', metavar='min-len', type=int, default=4,
                        help='Print sequences of characters that are at least min-len characters long')
    parser.add_argument('-e', metavar='encoding', choices=('s', 'l', 'b'), default='s',
                        help='Select the character encoding of the strings that are to be found. ' +
                             'Possible values for encoding are: s = UTF-8, b = big-endian UTF-16, ' +
                             'l = little endian UTF-16.')
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        print_strings(f, args.e, args.n)

if __name__ == '__main__':
    main()
