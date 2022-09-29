from .types.type import getTypeImplementation


class Tag:
    def __init__(self, inputFile=None, signature="", offset=0, size=0):
        self.file = inputFile
        self.signature = signature
        self.offset = offset
        self.size = size

    def read(self):
        self.file.seek(self.offset)
        signature = self.file.read(4)
        self.data = getTypeImplementation(self.file, signature, self.offset, self.size)
        self.data.read()

    def __str__(self):
        if not hasattr(self, 'data'):
            return f"<Tag {self.signature.decode('ascii')}>"
        return f"<Tag {self.signature.decode('ascii')} data={self.data}>"

