import tags
import struct


class ExifParseError(Exception):
    def init(__self__):
        pass


def carve(f, start, end):
    # return the bytes
    byte_list = f.read()
    return byte_list[start:end+1]


def find_jfif(f, max_length=None):
    # do some stuff
    # then return a possibly-empty sequence of pairs
    # here's an example that just returns the start and end of the file without parsing
    list = []
    b = f.read(2)
    count = 0
    while b:
        if b == b"\xFF\xD8":
            start = count
            temp_count = count + 2
            f.seek(temp_count)
            temp = f.read(2)
            while temp:
                if temp == b"\xFF\xD9":
                    end = temp_count + 1
                    if max_length is None:
                        list.append((start, end))
                    elif end - start + 1 <= max_length:
                        list.append((start, end))
                temp_count += 1
                f.seek(temp_count)
                temp = f.read(2)
        count += 1
        f.seek(count)
        b = f.read(2)

    return list


def parse_exif(f):
    res = {}
    count = 0
    b = f.read(2)
    if b == b"\xFF\xD8":
        count += 2
        b = f.read(2)
        while b:
            if b == b"\xFF\xE1":
                checkmark_e = count + 10
                print("checkmark endian :")
                print(checkmark_e)
                f.seek(checkmark_e)
                b = f.read(2)
                if b == b"\x4D\x4D":
                    print(b)
                    checkmark_num_of_fid = checkmark_e + 8
                    f.seek(checkmark_num_of_fid)
                    b = f.read(2)
                    num_of_fid = struct.unpack('>H', b)[0]
                    checkmark = checkmark_num_of_fid + 2
                    b = f.read(2)

                    while num_of_fid > 0 and b:
                        print("turn")
                        print(num_of_fid)
                        v = f.read(2)
                        value_type = struct.unpack('>H', v)[0]
                        print("value type ", end="")
                        print(value_type)
                        c = f.read(4)
                        component = struct.unpack('>I', c)[0]
                        print("num of component ", end="")
                        print(component)

                        b_as_hex = struct.unpack('>H', b)[0]
                        print("hex: ", end="")
                        print(b_as_hex)

                        if value_type == 1:
                            d = f.read(1)
                            while d:
                                if component*1 <= 4:
                                    data = struct.unpack('>B', d)[0]
                                else:
                                    length = component * 1
                                    position = checkmark_e + struct.unpack('>I', d)[0]
                                    f.seek(position)
                                    d_temp = f.read(length)
                                    data = struct.unpack('>B', d_temp)
                                d = f.read(1)
                            if b_as_hex in tags.TAGS:
                                if tags.TAGS[b_as_hex] in res:
                                    res[tags.TAGS[b_as_hex]].append(data)
                                else:
                                    res[tags.TAGS[b_as_hex]] = [data]
                            print(data)
                        elif value_type == 2:
                            d = f.read(4)
                            if component*1 <= 4:
                                length = component * 1
                                data = bytes.decode(d[0:length-1])
                                print(d[0:length])
                            else:
                                length = component * 1
                                position = checkmark_e + struct.unpack('>I', d)[0]
                                f.seek(position)
                                d_temp = f.read(length)
                                data = bytes.decode(d_temp[0:length-1])
                            if b_as_hex in tags.TAGS:
                                if tags.TAGS[b_as_hex] in res:
                                    res[tags.TAGS[b_as_hex]].append(data)
                                else:
                                    res[tags.TAGS[b_as_hex]] = [data]
                            print(data)
                        elif value_type == 3:
                            d = f.read(2)
                            if component*2 <= 4:
                                data = struct.unpack('>%dH' % component, d)[0]
                            else:
                                length = component * 2
                                position = checkmark_e + struct.unpack('>I', d)[0]
                                f.seek(position)
                                d_temp = f.read(length)
                                data = struct.unpack('>%dH' % component, d_temp)[0]
                            if b_as_hex in tags.TAGS:
                                if tags.TAGS[b_as_hex] in res:
                                    res[tags.TAGS[b_as_hex]].append(data)
                                else:
                                    res[tags.TAGS[b_as_hex]] = [data]
                            print(data)
                        elif value_type == 4:
                            d = f.read(4)
                            if component*4 <= 4:
                                data = struct.unpack('>L', d)[0]
                            else:
                                length = component * 4
                                position = checkmark_e + struct.unpack('>I', d)[0]
                                f.seek(position)
                                d_temp = f.read(length)
                                data = struct.unpack('>L', d_temp)[0]
                            if b_as_hex in tags.TAGS:
                                if tags.TAGS[b_as_hex] in res:
                                    res[tags.TAGS[b_as_hex]].append(data)
                                else:
                                    res[tags.TAGS[b_as_hex]] = [data]
                            print(data)
                        elif value_type == 5:
                            d = f.read(4)
                            length = component * 8
                            position = checkmark_e + struct.unpack('>I', d)[0]
                            f.seek(position)
                            d_temp = f.read(length)
                            (num, dem) = struct.unpack(">LL", d_temp)
                            data = "%s/%s"%(num,dem)
                            if b_as_hex in tags.TAGS:
                                if tags.TAGS[b_as_hex] in res:
                                    res[tags.TAGS[b_as_hex]].append(data)
                                else:
                                    res[tags.TAGS[b_as_hex]] = [data]
                            print(data)
                        elif value_type == 7:
                            d = f.read(4)
                            length = component * 1
                            if length <= 4:
                                value = struct.unpack(">%dB" % length, d[0:length])
                                data = "".join("%.2x" % x for x in value)
                            else:
                                position = checkmark_e + struct.unpack('>I', d)[0]
                                f.seek(position)
                                d_temp = f.read(length)
                                value = struct.unpack(">%dB" % length, d_temp[0:length])
                                data = "".join("%.2x" % x for x in value)
                            if b_as_hex in tags.TAGS:
                                if tags.TAGS[b_as_hex] in res:
                                    res[tags.TAGS[b_as_hex]].append(data)
                                else:
                                    res[tags.TAGS[b_as_hex]] = [data]
                            print(data)

                        num_of_fid -= 1
                        if num_of_fid == 0:
                            new_fid = f.read(4)

                            if new_fid != b"\x00\x00\x00\x00":
                                print("reset")
                                new_position = checkmark_e + struct.unpack('>I', new_fid)[0]
                                checkmark = new_position + 2
                                f.seek(new_position)
                                new_fid = f.read(2)
                                num_of_fid = struct.unpack('>H', new_fid)[0]
                                b = f.read(2)
                        else:
                            checkmark += 12
                            f.seek(checkmark)
                            b = f.read(2)
                            print("----------")

                elif b == b"\x49\x49":
                    print(b)
                else:
                    f.seek(count)
            count += 1
            f.seek(count)
            b = f.read(2)
    print(res)
    return res


parse_exif(open('palmtrees.jpg', 'rb'))
