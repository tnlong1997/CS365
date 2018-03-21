import struct


def fsstat_fat16(fat16_file, sector_size=512, offset=0):
    result = ['FILE SYSTEM INFORMATION',
              '--------------------------------------------',
              'File System Type: FAT16',
              '']

    # then do a few things, .append()ing to result as needed
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

    result.append("OEM Name: %s" % OEM)
    result.append("Volume ID: %s" % volumeId)
    result.append("Volume Label (Boot Sector): %s" % label)
    result.append("File System Type Label: FAT16")
    result.append("")
    result.append("Sectors before file system: %d" % offset)
    result.append("")
    result.append("File System Layout (in sectors)")
    result.append("Total Range: 0 - %d" % (numberOfSectors - 1))
    result.append("* Reserved: 0 - %d" % (reserved - 1))
    result.append("** Boot Sector: %d" % int(offset / bytesPerSector))
    for x in range(0, numberOfFAT):
        result.append("* FAT %d" % x + ": %d" % (reserved + sectorPerFAT * x)
                      + " - %d" % (sectorPerFAT * (x + 1) + reserved - 1))
    result.append("* Data Area: %d" % beginData
                  + " - %d" % (numberOfSectors - 1))
    result.append("** Root Directory: %d" % beginData
                  + " - %d" % (beginData + rootSize - 1))
    result.append("** Cluster Area: %d" % (rootSize + beginData)
                  + " - %d" % (numberOfSectors - leftover - 1))
    result.append("")
    result.append("CONTENT INFORMATION")
    result.append("--------------------------------------------")
    result.append("Sector Size: %d" % bytesPerSector)
    result.append("Cluster Size: %d" % bytesPerCluster)
    result.append("Total Cluster Range: %d" % sectorsPerCluster
                  + " - %d" % int(sectorsPerCluster + (numberOfSectors
                                                       - rootSize
                                                       - beginData
                                                       - leftover) / sectorsPerCluster - 1))
    result.append("")
    result.append("FAT CONTENTS (in sectors)")
    result.append("--------------------------------------------")
    # for x in range(0, numberOfFAT):
    # for res in result:
    #     print(res)
    return result


# fsstat_fat16(open('adams.dd', 'rb'), offset=0)
