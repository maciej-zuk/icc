import math
from .type import TypeImplementation, registerType
from . import primitive


def paramCurve(params):
    def fn(x):
        lp = len(params) - 1
        a = math.floor(x * lp)
        period = 1/lp
        if a >= lp:
            return params[-1]
        if a < 0:
            return params[0]
        b = a + 1
        c = (x - a*period) / period
        return params[a] * (1 - c) + params[b] * c
    return fn


class CurveType(TypeImplementation):
    signature = b'curv'

    def read(self):
        self.file.read(4)
        self.entries = primitive.readU32(self.file)
        if self.entries == 0:
            self.fn = lambda x: x
        elif self.entries == 1:
            self.value = primitive.readU8Fixed8Number(self.file)
            self.fn = lambda x: math.pow(x, self.value)
        else:
            self.values = []
            for n in range(self.entries):
                self.values.append(primitive.readU16(self.file) / 65535.0)
            self.fn = paramCurve(self.values)

    def get(self, x):
        return self.fn(x)

    def getDefault(self):
        return self.fn


registerType(CurveType)
