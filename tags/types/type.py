class DataReplay:
    def __init__(self, file):
        self.file = file
        self.replay = []
        self.recording = False

    def start_replay(self):
        self.replay = []
        self.recording = True

    def stop_replay(self):
        self.recording = False
        return self.replay

    def read(self, *args, **kwargs):
        data = self.file.read(*args, **kwargs)
        if self.recording:
            self.replay.append({"type": "read", "args": args, "kwargs": kwargs, "data": data})
        return data

    def seek(self, *args, **kwargs):
        if self.recording:
            self.replay.append({"type": "seek", "args": args, "kwargs": kwargs})
        return self.file.seek(*args, **kwargs)

    def tell(self, *args, **kwargs):
        data = self.file.tell(*args, **kwargs)
        if self.recording:
            self.replay.append({"type": "tell", "args": args, "kwargs": kwargs, "data": data})
        return data

    def print_replay(self):
        return b"".join([x["data"] for x in self.stop_replay() if x["type"] == "read"])


class TypeImplementation:
    def __init__(self, inputFile=None, parentOffset=0, parentSize=0):
        self.file = DataReplay(inputFile)
        self.parentOffset = parentOffset
        self.parentSize = parentSize

    def read(self):
        pass

    def get(self):
        return self.getDefault()

    def getDefault(self):
        pass

    def __str__(self):
        return f"<Type {self.signature.decode('ascii')}: {self.getDefault()}>"


typeRegistry = {}


def registerType(klass):
    typeRegistry[klass.signature] = klass


def getTypeImplementation(file, signature, parentOffset=0, parentSize=0):
    klass = signature in typeRegistry and typeRegistry[signature] or TypeImplementation
    obj = klass(file, parentOffset, parentSize)
    obj.signature = signature
    return obj
