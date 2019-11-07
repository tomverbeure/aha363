#! /usr/bin/env python3

import sys

import pprint

pp = pprint.PrettyPrinter(indent = 4)

CREATOR_ID = 1
DEVICE_NAME = 2
COMMENT = 3
RESERVED_4 = 4
SECURITY_BIT = 5
LOG_ADDR_DATA16 = 6
ELEC_ADDR_DATA16 = 7
TERMINATOR = 8
SYM_TABLE = 9
TEST_VECTORS = 10
ELEC_ADDR_CONST_DATA = 12
NUM_PROG_ELEMENTS = 14
LOG_ADDR_DATA32 = 17
FLASH_CHUNKS = 26

packet_tags = {
    CREATOR_ID 		: { "descr" : "Creator_ID", "type" : "string", },
    DEVICE_NAME 	: { "descr" : "Device_Name", "type" : "string", },
    COMMENT 		: { "descr" : "Comment_Text", "type" : "string", },
    RESERVED_4 		: { "descr" : "Tag_Reserved", },
    SECURITY_BIT 	: { "descr" : "Security_Bit", },
    LOG_ADDR_DATA16 	: { "descr" : "Logical_Address_and_Data_16", },
    ELEC_ADDR_DATA16	: { "descr" : "Electrical_Address_and_Data_16", },
    TERMINATOR		: { "descr" : "Terminator", },
    SYM_TABLE 		: { "descr" : "Symbol table", },
    TEST_VECTORS 	: { "descr" : "Test Vectors", },
    ELEC_ADDR_CONST_DATA: { "descr" : "Electrical_Address_and_Constant_Data", },
    NUM_PROG_ELEMENTS 	: { "descr" : "Number of programmable elements", },
    LOG_ADDR_DATA32 	: { "descr" : "Logical_Address_and_Data_32", },
    FLASH_CHUNKS 	: { "descr" : "Flash Chunks <unofficial>", },
}

def hexdump(data, length):

    str = ""
    for offset in range(0,min(length, len(data))):
        if (offset % 16) == 0:
            print("{:08x}: ".format(offset), end="")
        print("{:02x} ".format(data[offset]), end="")

        if data[offset] < 32:
            char = "."
        else:
            char = chr(data[offset])
        str += char

        if (offset % 16) == 7:
            print(" ", end="")

        if (offset % 16) == 15:
            print(": {:s}".format(str))
            str = ""
    pass
    print()
    
def parse_packet(data):
    offset = 0
    packet_tag = data[offset] + (data[offset+1] << 8)
    offset = offset + 2
    packet_len = data[offset] + (data[offset+1] << 8) + (data[offset+2] << 16) + (data[offset+3] << 24)
    offset = offset + 4

    packet_tag_info = packet_tags.get(packet_tag, { "descr" : "<Unknown>" })

    print("Tag: {:d} ({:s})".format(packet_tag, packet_tag_info["descr"]))
    print("Length: {:d} (0x{:08x})".format(packet_len, packet_len))

    info = {
        "tag"		: packet_tag,
        "length"	: packet_len,
        "data"		: data[offset:offset+packet_len],
        "all_decoded"	: False,
        }

    if "type" in packet_tag_info and packet_tag_info["type"] == "string":
        str = "".join(map(chr,data[offset:offset+packet_len]))
        info["string"] = str
        info["all_decoded"] = True

        print("Content: '{:s}'".format(str))
        print()

    if packet_tag == TERMINATOR:
        crc16 = int.from_bytes(data[offset:offset+2], byteorder='little')
        info["crc16"] = crc16
        info["all_decoded"] = True

        print("CRC16: 0x{:02x}".format(crc16))
        print()

    if packet_tag == LOG_ADDR_DATA32:
        field0 = int.from_bytes(data[offset  :offset+4], byteorder='little')
        field1 = int.from_bytes(data[offset+4:offset+8], byteorder='little')
        field2 = int.from_bytes(data[offset+8:offset+12], byteorder='little')

        info["field0"] = field0
        info["field1"] = field1
        info["field2"] = field2
        info["all_decoded"] = True

        print("Field 0: 0x{:08x} ({:d})".format(field0, field0))
        print("Field 1: 0x{:08x} ({:d})".format(field1, field1))
        print("Field 2: 0x{:08x} ({:d})".format(field2, field2))
        print("Binary Content:")
        hexdump(data[offset+12:offset+packet_len], 256)
        print()

        with open("dump.bin", mode="wb") as dump:
            dump.write(data[offset+12:offset+packet_len])

    if packet_tag == FLASH_CHUNKS:
        field0 = int.from_bytes(data[offset  :offset+4], byteorder='little')
        field1 = int.from_bytes(data[offset+4:offset+8], byteorder='little')
        field2 = int.from_bytes(data[offset+8:offset+12], byteorder='little')

        info["field0"] = field0
        info["field1"] = field1
        info["field2"] = field2
        info["all_decoded"] = True

        print("Field 0: 0x{:08x} ({:d})".format(field0, field0))
        print("Field 1: 0x{:08x} ({:d})".format(field1, field1))
        print("Field 2: 0x{:08x} ({:d})".format(field2, field2))
        str = "".join(map(chr,data[offset+12:offset+packet_len]))
        print("Content:")
        print("\n".join(str.split(";")))
        print()

    if packet_tag == 30:
        field0 = int.from_bytes(data[offset  :offset+4], byteorder='little')
        field1 = int.from_bytes(data[offset+4:offset+8], byteorder='little')

        info["field0"] = field0
        info["field1"] = field1
        info["all_decoded"] = True

        print("Field 0: 0x{:08x} ({:d})".format(field0, field0))
        print("Field 1: 0x{:08x} ({:d})".format(field1, field1))
        print()

     
    return info


all_packets = []

with open(sys.argv[1], mode="rb") as file:
    data = file.read()

    header = "".join(map(chr,data[0:3]))
    print(header)

    if header != "POF":
        print("Missing POF header.")
        sys.exit(-1);

    offset = 12
    

    while offset < len(data):
        print("==============================")
        #print("0x{:08x}:".format(offset))
        #hexdump(data[offset:], 128)
        info = parse_packet(data[offset:])

        if not(info["all_decoded"]):
            hexdump(info["data"], 128)

        all_packets.append(info)
        offset += 2 + 4 + info["length"]

    print()
    hexdump(data, 256)


