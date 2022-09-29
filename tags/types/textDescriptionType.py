from .type import TypeImplementation, registerType
from . import primitive


class TextDescriptionType(TypeImplementation):
    text = None
    signature = b'desc'

    def read(self):
        self.file.read(4)
        size = primitive.readU32(self.file)
        self.text = self.file.read(size).decode('ascii')

    def getDefault(self):
        return self.text


registerType(TextDescriptionType)
