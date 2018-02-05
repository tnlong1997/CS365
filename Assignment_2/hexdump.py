import sys
import binascii


def dump():
    line = f.read(16)
    count = 0
    while len(line) != 0:
        res_string = ""
        res_byte = ""
        content = binascii.hexlify(line)
        for i in range(0, 16):
            if (i * 2 < len(content)):
                hchar = content[(i*2):(i*2+2)]
                res_byte = res_byte + str(hchar, 'utf-8') + str(' ')
                val = int(hchar, 16)
                if (val >= 32 and val < 127):
                    res_string = res_string + str(chr(val))
                else:
                    res_string = res_string + str('.')
            else:
                res_byte = res_byte + '   '
            if (i == 7):
                res_byte = res_byte + str(' ')
        print('%08x  %s |%s|' % (count, res_byte, res_string))
        count += len(content) // 2
        line = f.read(16)
    print('%08x' % count)


filename = str(sys.argv[1])
f = open(filename, "rb")
dump()
