import struct
import datetime


def readDateTime(file):
    return datetime.datetime(*struct.unpack(">HHHHHH", file.read(12)))


def readU32(file):
    return struct.unpack(">I", file.read(4))[0]


def readU16(file):
    return struct.unpack(">H", file.read(2))[0]


def readU8(file):
    return file.read(1)[0]


def readS15Fixed16Number(file):
    integerPart, fractionPart = struct.unpack(">hH", file.read(4))
    return integerPart + fractionPart/65536.0


def readU8Fixed8Number(file):
    # file.read(1)
    return 0
