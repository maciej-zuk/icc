import math
from .type import TypeImplementation, registerType
from . import primitive


class ParametricCurveType(TypeImplementation):
    signature = b'para'

    def read(self):
        self.file.read(4)
        self.fType = primitive.readU16(self.file)
        self.file.read(2)
        if self.fType == 0:
            self.g = primitive.readS15Fixed16Number(self.file)
            self.fn = lambda x: math.pow(x, self.g)
        if self.fType == 1:
            self.g = primitive.readS15Fixed16Number(self.file)
            self.a = primitive.readS15Fixed16Number(self.file)
            self.b = primitive.readS15Fixed16Number(self.file)
            self.ba = -self.b / self.a
            self.fn = lambda x: x >= self.ba and math.pow(self.a*x+self.b, self.g) or 0
        if self.fType == 2:
            self.g = primitive.readS15Fixed16Number(self.file)
            self.a = primitive.readS15Fixed16Number(self.file)
            self.b = primitive.readS15Fixed16Number(self.file)
            self.c = primitive.readS15Fixed16Number(self.file)
            self.ba = -self.b / self.a
            self.fn = lambda x: x >= self.ba and math.pow(self.a*x+self.b, self.g) + self.c or self.c
        if self.fType == 3:
            self.g = primitive.readS15Fixed16Number(self.file)
            self.a = primitive.readS15Fixed16Number(self.file)
            self.b = primitive.readS15Fixed16Number(self.file)
            self.c = primitive.readS15Fixed16Number(self.file)
            self.d = primitive.readS15Fixed16Number(self.file)
            self.fn = lambda x: x >= self.d and math.pow(self.a*x+self.b, self.g) or self.c*x
        if self.fType == 4:
            self.g = primitive.readS15Fixed16Number(self.file)
            self.a = primitive.readS15Fixed16Number(self.file)
            self.b = primitive.readS15Fixed16Number(self.file)
            self.c = primitive.readS15Fixed16Number(self.file)
            self.d = primitive.readS15Fixed16Number(self.file)
            self.e = primitive.readS15Fixed16Number(self.file)
            self.f = primitive.readS15Fixed16Number(self.file)
            self.fn = lambda x: x >= self.d and math.pow(self.a*x+self.b, self.g)+self.e or self.c*x+self.f

    def get(self, x):
        return self.fn(x)

    def getDefault(self):
        return f'curve type {self.fType}'


registerType(ParametricCurveType)
