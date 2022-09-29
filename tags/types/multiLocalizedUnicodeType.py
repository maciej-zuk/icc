from .type import TypeImplementation, registerType
from . import primitive


class MultiLocalizedUnicodeType(TypeImplementation):
    signature = b'mluc'

    def read(self):
        self.file.read(4)
        self.recordCount = primitive.readU32(self.file)
        self.recordSize = primitive.readU32(self.file)
        self.records = []
        self.langs = []
        self.langToRecord = {}
        for r in range(self.recordCount):
            langCode = self.file.read(2)
            langCode2 = self.file.read(2)
            size = primitive.readU32(self.file)
            offset = primitive.readU32(self.file)
            self.langs.append(langCode)
            self.langToRecord[langCode] = r
            self.records.append({
                "lang": langCode,
                "lang2": langCode2,
                "offset": offset,
                "size": size,
            })
        for r in range(self.recordCount):
            self.records[r]["data"] = self.file.read(self.records[r]["size"])

    def get(self, lang):
        rc = self.langToRecord.get(lang, 0)
        try:
            return self.records[rc]["data"].decode('utf-16be')
        except UnicodeDecodeError:
            return self.records[rc]["data"]

    def getDefault(self):
        return self.get(None)


registerType(MultiLocalizedUnicodeType)
