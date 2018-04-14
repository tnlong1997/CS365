import datetime
import struct


def as_signed_le(bs):
    if len(bs) <= 0 or len(bs) > 8:
        raise ValueError()

    signed_format = {1: 'b', 2: 'h', 4: 'l', 8: 'q'}

    fill = b'\xFF' if ((bs[-1] & 0x80) >> 7) == 1 else b'\x00'

    while len(bs) not in signed_format:
        bs = bs + fill

    return struct.unpack('<' + signed_format[len(bs)], bs)[0]


def to_size(s):
    if (s < 0):
        return 1 << abs(s)
    return s


def istat_ntfs(f, address, sector_size=512, offset=0):
    run_list = []
    res = []
    f.seek(sector_size * offset + 11)
    bytes_per_sector = f.read(2)
    bytes_per_sector = struct.unpack('<H', bytes_per_sector)[0]

    sector_per_cluster = f.read(1)
    sector_per_cluster = struct.unpack('<B', sector_per_cluster)[0]

    f.seek(sector_size * offset + 48)
    MFT_cluster_address = f.read(8)
    MFT_cluster_address = struct.unpack('<Q', MFT_cluster_address)[0]

    f.seek(sector_size * offset + 64)
    file_record_size = f.read(1)
    file_record_size = to_size(as_signed_le(file_record_size))

    f.seek(sector_size * offset + 68)
    index_record_size = f.read(1)
    index_record_size = to_size(as_signed_le(index_record_size))

    MFT_entry_index = offset * sector_size + (MFT_cluster_address
                                              * sector_per_cluster
                                              * bytes_per_sector) + (address
                                                                     * 1024)

    f.seek(MFT_entry_index)

    f.read(8)
    lsn_sequence_number = f.read(8)
    lsn_sequence_number = struct.unpack('<Q', lsn_sequence_number)[0]

    sequence_value = f.read(2)
    sequence_value = struct.unpack('<H', sequence_value)[0]

    link_count = f.read(2)
    link_count = struct.unpack('<H', link_count)[0]

    offset_to_first_att = f.read(2)
    offset_to_first_att = struct.unpack('<H', offset_to_first_att)[0]

    log_flag = f.read(2)
    log_flag = struct.unpack('<H', log_flag)[0]

    res.append('MFT Entry Header Values:')
    res.append('Entry: %d        Sequence: %d' % (address, sequence_value))
    res.append('$LogFile Sequence Number: %d' % lsn_sequence_number)
    res.append('Allocated File')
    res.append('Links: %d' % link_count)
    res.append('')

    attributes = ['Attributes:']

    att_index = offset_to_first_att + MFT_entry_index
    while (True):
        temp = 'Type: '
        f.seek(att_index)
        att_type = f.read(4)
        att_type = struct.unpack('<L', att_type)[0]

        att_size = f.read(4)
        att_size = struct.unpack('<L', att_size)[0]

        if (att_size == 0 or att_type == 4294967295):
            break

        non_president_flag = f.read(1)
        non_president_flag = struct.unpack('<B', non_president_flag)[0]

        length_of_name = f.read(1)
        length_of_name = struct.unpack('<B', length_of_name)[0]
        # print(length_of_name)

        offset_to_name = f.read(2)
        offset_to_name = struct.unpack('<H', offset_to_name)[0]

        f.seek(att_index + 12)
        name = ''
        if (length_of_name == 0):
            name = 'N/A'

        flags = f.read(2)
        flags = struct.unpack('<H', flags)[0]

        att_identifier = f.read(2)
        att_identifier = struct.unpack('<H', att_identifier)[0]

        if (att_type == 128):
            temp = temp + '$DATA '
            temp = temp + '(%d-%d)   ' % (att_type, att_identifier)
            temp = temp + 'Name: %s   ' % name
            if (non_president_flag == 0):
                temp = temp + 'Resident   '
                size_of_content = f.read(4)
                size_of_content = struct.unpack('<L', size_of_content)[0]
                temp = temp + 'size: %d' % size_of_content
            else:
                temp = temp + 'Non-Resident   '
                start_vcn = f.read(8)
                start_vcn = struct.unpack('<Q', start_vcn)[0]

                end_vcn = f.read(8)
                end_vcn = struct.unpack('<Q', end_vcn)[0]

                run_offset = f.read(2)
                run_offset = struct.unpack('<H', run_offset)[0]

                f.seek(att_index + 48)
                actual_size = f.read(8)
                actual_size = struct.unpack('<Q', actual_size)[0]

                init_size = f.read(8)
                init_size = struct.unpack('<Q', init_size)[0]
                temp = temp + 'size: %d  ' % actual_size
                temp = temp + 'init_size: %d' % init_size

                f.seek(att_index + run_offset)
                byte = f.read(1)
                byte = struct.unpack('<B', byte)[0]

                run_index = 0

                while (byte != 0):
                    run_start = byte >> 4
                    run_len = byte & 15

                    length = f.read(run_len)
                    length = as_signed_le(length)

                    start = f.read(run_start)
                    start = as_signed_le(start) + run_index
                    run_index = start

                    byte = f.read(1)
                    byte = struct.unpack('<B', byte)[0]

                    for i in range(start, start + length):
                        run_list.append(i)

            attributes.append(temp)

        elif (att_type == 16):
            res.append('$STANDARD_INFORMATION Attribute Values:')

            temp = temp + '$STANDARD_INFORMATION '
            temp = temp + '(%d-%d)   ' % (att_type, att_identifier)
            temp = temp + 'Name: %s   ' % name
            if (non_president_flag == 0):
                temp = temp + 'Resident   '
                size_of_content = f.read(4)
                size_of_content = struct.unpack('<L', size_of_content)[0]
                temp = temp + 'size: %d' % size_of_content
                res = res + president_implementation(f, att_type, att_index,
                                                     att_size, size_of_content)
            attributes.append(temp)

        elif (att_type == 48):
            res.append('$FILE_NAME Attribute Values:')

            temp = temp + '$FILE_NAME '
            temp = temp + '(%d-%d)   ' % (att_type, att_identifier)
            temp = temp + 'Name: %s   ' % name
            if (non_president_flag == 0):
                temp = temp + 'Resident   '
                size_of_content = f.read(4)
                size_of_content = struct.unpack('<L', size_of_content)[0]
                temp = temp + 'size: %d' % size_of_content
                res = res + president_implementation(f, att_type, att_index,
                                                     att_size, size_of_content)
            attributes.append(temp)
        att_index += att_size

    # for r in res:
    #     print(r)
    res = res + attributes
    count = 0
    t = ''
    for i in run_list:
        count += 1
        t = t + '%d ' % i
        if (count == 8):
            res.append(t)
            t = ''
            count = 0

    if (count != 0):
        res.append(t)

    return res


def president_implementation(f, att_type, att_index,
                             att_size, size_of_content):
    offset_to_content = f.read(2)
    offset_to_content = struct.unpack('<H', offset_to_content)[0]

    f.seek(att_index + offset_to_content)
    res = []
    if (att_type == 128):
        pass

    elif (att_type == 16):
        creation_date = f.read(8)
        creation_date = struct.unpack('<Q', creation_date)[0]
        creation_date = into_localtime_string(creation_date)

        file_modified_date = f.read(8)
        file_modified_date = struct.unpack('<Q', file_modified_date)[0]
        file_modified_date = into_localtime_string(file_modified_date)

        mft_modified_date = f.read(8)
        mft_modified_date = struct.unpack('<Q', mft_modified_date)[0]
        mft_modified_date = into_localtime_string(mft_modified_date)

        file_accessed_date = f.read(8)
        file_accessed_date = struct.unpack('<Q', file_accessed_date)[0]
        file_accessed_date = into_localtime_string(file_accessed_date)

        flags = f.read(4)
        flags = struct.unpack('<L', flags)[0]

        f.read(12)
        owner_id = f.read(4)
        owner_id = struct.unpack('<L', owner_id)[0]

        res.append('Flags: %s' % to_flags(flags))
        res.append('Owner ID: %d' % (owner_id - 48))
        res.append('Created:\t%s' % creation_date)
        res.append('File Modified:\t%s' % file_modified_date)
        res.append('MFT Modified:\t%s' % mft_modified_date)
        res.append('Accessed:\t%s' % file_accessed_date)
        res.append('')

    elif (att_type == 48):
        ref_of_parent_dir = f.read(6)
        ref_of_parent_dir = as_signed_le(ref_of_parent_dir)

        sequence_number = f.read(2)
        sequence_number = struct.unpack('<H', sequence_number)[0]

        creation_date = f.read(8)
        creation_date = struct.unpack('<Q', creation_date)[0]
        creation_date = into_localtime_string(creation_date)

        file_modified_date = f.read(8)
        file_modified_date = struct.unpack('<Q', file_modified_date)[0]
        file_modified_date = into_localtime_string(file_modified_date)

        mft_modified_date = f.read(8)
        mft_modified_date = struct.unpack('<Q', mft_modified_date)[0]
        mft_modified_date = into_localtime_string(mft_modified_date)

        file_accessed_date = f.read(8)
        file_accessed_date = struct.unpack('<Q', file_accessed_date)[0]
        file_accessed_date = into_localtime_string(file_accessed_date)

        allocated_size = f.read(8)
        allocated_size = struct.unpack('<Q', allocated_size)[0]

        actual_size = f.read(8)
        actual_size = struct.unpack('<Q', actual_size)[0]

        flags = f.read(4)
        flags = struct.unpack('<L', flags)[0]

        f.read(4)
        name_length = f.read(1)
        name_length = struct.unpack('<B', name_length)[0]

        f.read(1)

        name = f.read(name_length * 2)
        name = name.decode('utf-16-le')
        name = name.strip(' ')

        res.append('Flags: %s' % to_flags(flags))
        res.append('Name: %s' % name)
        res.append('Parent MFT Entry: %d \tSequence: %d' % (ref_of_parent_dir,
                                                            sequence_number))
        res.append('Allocated Size: %d   \tActual Size: %d' % (allocated_size,
                                                               actual_size))
        res.append('Created:\t%s' % creation_date)
        res.append('File Modified:\t%s' % file_modified_date)
        res.append('MFT Modified:\t%s' % mft_modified_date)
        res.append('Accessed:\t%s' % file_accessed_date)
        res.append('')

    return res


def to_flags(flags):
    if (flags == 1):
        return 'Read Only'
    if (flags == 2):
        return 'Hidden'
    if (flags == 4):
        return 'System'
    if (flags == 32):
        return 'Archive'


def into_localtime_string(windows_timestamp):
    """
    Convert a windows timestamp into istat-compatible output.

    Assumes your local host is in the EDT timezone.

    :param windows_timestamp: the struct.decoded 8-byte windows timestamp
    :return: an istat-compatible string representation of this time in EDT
    """
    dt = datetime.datetime.fromtimestamp((windows_timestamp
                                         - 116444736000000000) / 10000000)
    hms = dt.strftime('%Y-%m-%d %H:%M:%S')
    fraction = windows_timestamp % 10000000
    return hms + '.' + str(fraction) + '00 (EDT)'


# if __name__ == '__main__':
#     istat_ntfs(open('image.ntfs', 'rb'), 65)
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Display details of a meta-data structure (i.e. inode).')
    parser.add_argument('-o', type=int, default=0, metavar='imgoffset',
                        help='The offset of the file system in the image (in sectors)')
    parser.add_argument('-b', type=int, default=512, metavar='dev_sector_size',
                        help='The size (in bytes) of the device sectors')
    parser.add_argument('image', help='Path to an NTFS raw (dd) image')
    parser.add_argument('address', type=int,
                        help='Meta-data number to display stats on')
    args = parser.parse_args()
    with open(args.image, 'rb') as f:
        result = istat_ntfs(f, args.address, args.b, args.o)
        for line in result:
            print(line.strip())
