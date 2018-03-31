import struct


def as_unsigned(bs, endian='<'):
    unsigned_format = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
    if len(bs) <= 0 or len(bs) > 8:
        raise ValueError()
    fill = '\x00'
    while len(bs) not in unsigned_format:
        bs = bs + fill
    result = struct.unpack(endian + unsigned_format[len(bs)], bs)[0]
    return result


def decode_fat_time(time_bytes, tenths=0, tz='EDT'):
    v = as_unsigned(time_bytes)
    second = int(int(0x1F & v) * 2)
    if tenths > 100:
        second += 1
    minute = (0x7E0 & v) >> 5
    hour = (0xF800 & v) >> 11
    return '{:02}:{:02}:{:02} ({})'.format(hour, minute, second, tz)


def decode_fat_day(date_bytes):
    v = as_unsigned(date_bytes)
    day = 0x1F & v
    month = (0x1E0 & v) >> 5
    year = ((0xFE00 & v) >> 9) + 1980
    return '{}-{:02}-{:02}'.format(year, month, day)


def istat_fat16(f, address, sector_size=512, offset=0):
    fat16_file = f
    fat16_file.seek(offset * sector_size)
    fat16_file.read(3)
    OEM = fat16_file.read(8)
    OEM = OEM.decode('utf-8')
    bytesPerSector = fat16_file.read(2)
    bytesPerSector = struct.unpack('<H', bytesPerSector)[0]
    sectorsPerCluster = fat16_file.read(1)
    sectorsPerCluster = struct.unpack('<B', sectorsPerCluster)[0]
    bytesPerCluster = sectorsPerCluster * sector_size
    fat16_file.seek(offset*sector_size + 14)
    reserved = fat16_file.read(2)
    reserved = struct.unpack('<H', reserved)[0]
    numberOfFAT = fat16_file.read(1)
    numberOfFAT = struct.unpack('<B', numberOfFAT)[0]
    root = fat16_file.read(2)
    root = struct.unpack('<H', root)[0]
    rootSize = int(root * 32 / bytesPerSector)
    numberOfSectors = fat16_file.read(2)
    numberOfSectors = struct.unpack('<H', numberOfSectors)[0]
    leftover = (numberOfSectors + 1) % sectorsPerCluster
    fat16_file.seek(offset*sector_size + 22)
    sectorPerFAT = fat16_file.read(2)
    sectorPerFAT = struct.unpack('<H', sectorPerFAT)[0]
    beginData = sectorPerFAT*numberOfFAT + reserved
    fat16_file.seek(offset*sector_size + 39)
    volumeId = fat16_file.read(4)
    volumeId = hex(struct.unpack('<L', volumeId)[0])
    label = fat16_file.read(11)
    label = label.decode('utf-8')

    f.seek(offset * sector_size + sector_size * beginData)
    f.read((address - 2 - 1) * 32)
    first_byte = f.read(1)
    name = f.read(7)
    if (first_byte[0] == 0 or first_byte[0] == 229):
        allocated = False
        name = '_' + name.decode('utf-8')
    else:
        allocated = True
        name = first_byte.decode('utf-8') + name.decode('utf-8')
    name = name.strip(' ')
    extensions = f.read(3)
    if (extensions != b'   '):
        name = name + '.' + extensions.decode('utf-8').strip(' ')
    attributes = f.read(1)
    reserved = f.read(1)
    tenths = f.read(1)[0]
    createdTime = f.read(2)
    createdDate = f.read(2)
    accessedDate = f.read(2)
    f.read(2)
    writtenTime = f.read(2)
    writtenDate = f.read(2)
    first_cluster = struct.unpack('<H', f.read(2))[0]

    file_size = f.read(4)
    file_size = struct.unpack('<L', file_size)[0]

    start = offset * sector_size + sector_size + 4
    index = (first_cluster - 2) * 2
    f.seek(start + index)
    byte = f.read(2)
    sectors = []
    sectors.append(index)
    sectors.append(index + 1)
    # print(index)
    # print(struct.unpack('<H', byte)[0])
    # f.seek(start + 3676)
    # byte = f.read(2)
    # print(struct.unpack('<H', byte)[0])
    while (True):
        if (byte == b'\xff\xff'):
            break
        index = struct.unpack('<H', byte)[0] * 2 - 4
        f.seek(start + index)
        byte = f.read(2)
        sectors.append(index)
        sectors.append(index + 1)

    res = []
    res.append('Directory Entry: %d' % address)
    if not allocated:
        res.append('Unallocated')
    else:
        res.append('Allocated')
    res.append('File Attributes: %s' % get_attributes(attributes))
    if (attributes[0] >> 4 == 1):
        res.append('Size: %d' % (len(sectors) * sector_size))
    else:
        res.append('Size: %d' % (file_size))
    res.append('Name: %s' % name)
    res.append('')
    res.append('Directory Entry Times:')
    res.append('Written:\t%s %s' % (decode_fat_day(writtenDate),
                                    decode_fat_time(writtenTime)))
    res.append('Accessed:\t%s %s' % (decode_fat_day(accessedDate),
                                     decode_fat_time(b'\x00')))
    res.append('Created:\t%s %s' % (decode_fat_day(createdDate),
                                    decode_fat_time(createdTime,
                                                    tenths=tenths)))
    res.append('')
    res.append('Sectors:')

    count = 0
    temp = ''
    for sector in sectors:
        temp = temp + '%d ' % (sector + rootSize + beginData)
        count += 1
        if (count == 8):
            res.append(temp)
            temp = ''
            count = 0
    if (count > 0):
        res.append(temp)

    # for r in res:
    #     print(r)

    return res


def get_attributes(att):
    if (att == b'\x10'):
        return 'Directory'
    if (att == b'\x22'):
        return 'File, Hidden, Archive'
    if (att == b'\x20'):
        return 'File, Archive'
    if (att == b'\x12'):
        return 'Directory, Hidden'


istat_fat16(open('adams.dd', 'rb'), 7)

# if __name__ == '__main__':
    # The code below just exercises the time/date decoder
    # and need not be included
    # in your final submission!
    #
    # values below are from the directory entry in adams.dd that
    # corresponds to the
    # creation date/time of the `IMAGES` directory in the root directory, at
    # metadata address 5;it starts at offset 0x5240 from the start of the image
    # print(decode_fat_day(bytes.fromhex('E138')),
          # decode_fat_time(bytes.fromhex('C479'), 0))
