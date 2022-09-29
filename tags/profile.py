from .tag import Tag
from .types import primitive


def getProfileClassVerbose(profileClass):
    return {
        b'scnr': 'Input',
        b'mntr': 'Display',
        b'prtr': 'Output',
        b'link': 'Device link',
        b'spac': 'Color space conversion',
        b'abst': 'Abstract',
        b'nmcl': 'Named color',
    }.get(profileClass, 'Unknown')

class ProfileHeader:
    def __init__(self, inputFile):
        self.file = inputFile

    def read(self):
        self.file.seek(0)
        self.fileSize = primitive.readU32(self.file)
        self.cmmType = self.file.read(4)
        profileVersion = self.file.read(4)
        self.profileVersion = f"{profileVersion[0]}.{(profileVersion[1]&0xf0) >> 4}.{(profileVersion[1]&0x0f)}"
        self.profileClass = getProfileClassVerbose(self.file.read(4))
        self.colorSpace = self.file.read(4)
        self.pcs = self.file.read(4)
        self.dateTime = primitive.readDateTime(self.file)
        self.signature = self.file.read(4)
        self.platform = self.file.read(4)
        self.flags = self.file.read(4)
        self.devManufacturer = self.file.read(4)
        self.devModel = self.file.read(4)
        self.devAttr = self.file.read(8)
        self.intent = self.file.read(4)
        self.pcsIlluminant = self.file.read(12)
        self.creator = self.file.read(4)
        self.profileId = self.file.read(16)
        self.file.read(28)
        assert(self.file.tell() == 128)
        assert(self.signature == b'acsp')

    def __str__(self):
        result = []
        for k in [
            "profileVersion",
            "profileClass",
            "dateTime",
            "colorSpace",
            "pcs",
            "cmmType",
            "platform",
            "flags",
            "devManufacturer",
            "devModel",
            "devAttr",
            "intent",
            "pcsIlluminant",
            "creator",
            "profileId",
        ]:
            result.append(f"{k}={getattr(self, k)}")
        return f"<ProfileHeader {', '.join(result)}>"


class ProfileTag:
    def __init__(self, inputFile):
        self.file = inputFile

    def readHeader(self):
        self.signature = self.file.read(4)
        self.offset = primitive.readU32(self.file)
        self.size = primitive.readU32(self.file)
        self.implementation = Tag(self.file, self.signature, self.offset, self.size)

    def __str__(self):
        return f"<ProfileTag {self.implementation}>"


class ProfileTagTable:
    def __init__(self, inputFile):
        self.file = inputFile

    def read(self):
        self.file.seek(128)
        self.tagCount = primitive.readU32(self.file)
        self.tags = []
        self.bySignature = {}
        for tagN in range(self.tagCount):
            tag = ProfileTag(self.file)
            tag.readHeader()
            self.tags.append(tag)
            self.bySignature[tag.signature] = tag
        for tag in self.tags:
            tag.implementation.read()

    def getTag(self, signature):
        return self.bySignature[signature].implementation.data

    def __str__(self):
        return f"<ProfileTableTag TagCount={self.tagCount}>"


class Profile:
    def __init__(self, inputFile):
        self.file = inputFile
        self.header = ProfileHeader(inputFile)
        self.header.read()
        self.table = ProfileTagTable(inputFile)
        self.table.read()

    def __str__(self):
        return f"\
<Profile \
v{self.header.profileVersion} \
{self.header.profileClass} \
{self.header.colorSpace.decode('ascii').strip()} -> {self.header.pcs.decode('ascii').strip()}\
>"
