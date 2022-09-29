from .type import TypeImplementation, registerType
from . import primitive


class TextType(TypeImplementation):
    text = None
    signature = b'text'

    def read(self):
        self.file.read(4)
        size = self.parentSize - 8
        self.text = self.file.read(size).decode('ascii')

    def getDefault(self):
        return self.text


registerType(TextType)
