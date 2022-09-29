import functools
import math
from .type import TypeImplementation, registerType, getTypeImplementation
from . import primitive


@functools.lru_cache(maxsize=10000000)
def interpolate1Dim(x, lp):
    a = math.floor(x * lp)
    period = 1/lp
    c = (x - a*period) / period
    return a, c


class lutAToBType(TypeImplementation):
    signature = b'mAB '

    def read(self):
        self.file.read(4)
        self.inputChannelCount = primitive.readU8(self.file)
        self.outputChannelCount = primitive.readU8(self.file)
        self.file.read(2)
        self.bcOffset = primitive.readU32(self.file)
        self.matrixOffset = primitive.readU32(self.file)
        self.mcOffset = primitive.readU32(self.file)
        self.clutOffset = primitive.readU32(self.file)
        self.acOffset = primitive.readU32(self.file)
        if self.bcOffset:
            self.bc = []
            for n in range(self.outputChannelCount):
                curve = self.readTypeFromOffset(self.bcOffset)
                while self.file.tell() % 4 != 0:
                    self.file.read()
                self.bc.append(curve)
        if self.mcOffset:
            self.mc = []
            for n in range(self.outputChannelCount):
                curve = self.readTypeFromOffset(self.mcOffset)
                while self.file.tell() % 4 != 0:
                    self.file.read()
                self.mc.append(curve)
        if self.acOffset:
            self.ac = []
            for n in range(self.inputChannelCount):
                curve = self.readTypeFromOffset(self.acOffset)
                while self.file.tell() % 4 != 0:
                    self.file.read()
                self.ac.append(curve)
        if self.clutOffset:
            self.readCLUT()

    def readTypeFromOffset(self, offset):
        self.file.seek(self.parentOffset + offset)
        signature = self.file.read(4)
        data = getTypeImplementation(self.file, signature, self.parentOffset + offset, self.parentSize)
        data.read()
        return data

    def readCLUTData(self, dimNo=0):
        result = []
        if dimNo == self.inputChannelCount:
            for p in range(self.outputChannelCount):
                if self.precision == 1:
                    result.append(primitive.readU8(self.file))
                if self.precision == 2:
                    result.append(primitive.readU16(self.file))
        else:
            for gp in range(self.gridPoints[dimNo]):
                result.append(self.readCLUTData(dimNo + 1))
        return tuple(result)

    def readCLUT(self):
        self.file.seek(self.parentOffset + self.clutOffset)
        self.gridPoints = []
        for n in range(self.inputChannelCount):
            self.gridPoints.append(primitive.readU8(self.file))
        if self.inputChannelCount < 16:
            self.file.read(16-self.inputChannelCount)
        self.precision = primitive.readU8(self.file)
        self.maxGridValue = self.precision == 2 and 65535.0 or 255.0
        self.file.read(3)
        self.grid = self.readCLUTData()

    @functools.lru_cache(maxsize=10000000)
    def nLinearInterpoloation(self, coord, path=None, dimNo=0):
        if not path:
            path = ()
        out = [0]*self.outputChannelCount
        lp = self.gridPoints[dimNo] - 1
        a, t = interpolate1Dim(coord[dimNo], lp)
        sg0 = a
        sg1 = (a+1) < lp and a+1 or lp

        if dimNo == self.inputChannelCount - 1:
            p0 = self.getGrid(path + (sg0,))
            p1 = self.getGrid(path + (sg1,))
        else:
            p0 = self.nLinearInterpoloation(coord, path + (sg0,), dimNo+1)
            p1 = self.nLinearInterpoloation(coord, path + (sg1,), dimNo+1)

        for outDim in range(self.outputChannelCount):
            out[outDim] = p0[outDim] * (1-t) + p1[outDim] * t

        return tuple(out)

    @functools.lru_cache(maxsize=10000000)
    def nCubicInterpoloation(self, coord, path=None, dimNo=0):
        if not path:
            path = ()
        out = [0]*self.outputChannelCount
        lp = self.gridPoints[dimNo] - 1
        a, t = interpolate1Dim(coord[dimNo], lp)
        t2 = t*t
        t3 = t*t2
        sg0 = (a-1) >= 0 and a-1 or 0
        sg1 = a
        sg2 = (a+1) < lp and a+1 or lp
        sg3 = (a+2) < lp and a+2 or lp

        if dimNo == self.inputChannelCount - 1:
            p0 = self.getGrid(path + (sg0,))
            p1 = self.getGrid(path + (sg1,))
            p2 = self.getGrid(path + (sg2,))
            p3 = self.getGrid(path + (sg3,))
        else:
            p0 = self.nCubicInterpoloation(coord, path + (sg0,), dimNo+1)
            p1 = self.nCubicInterpoloation(coord, path + (sg1,), dimNo+1)
            p2 = self.nCubicInterpoloation(coord, path + (sg2,), dimNo+1)
            p3 = self.nCubicInterpoloation(coord, path + (sg3,), dimNo+1)

        for outDim in range(self.outputChannelCount):
            out[outDim] = 0.5 * ((2 * p1[outDim]) + (-p0[outDim] + p2[outDim]) * t + (2 * p0[outDim] - 5 * p1[outDim] + 4 *
                                 p2[outDim] - p3[outDim]) * t2 + (-p0[outDim] + 3 * p1[outDim] - 3 * p2[outDim] + p3[outDim]) * t3)
        return tuple(out)

    def getGrid(self, path):
        g = self.grid
        for p in path:
            g = g[p]
        return g

    def get(self, a):
        a = tuple(ac.get(p) for ac, p in zip(self.ac, a))
        b = self.nCubicInterpoloation(a)
        b = tuple(o/self.maxGridValue for o in b)
        b = tuple(bc.get(p) for bc, p in zip(self.bc, b))
        return b

    def getDefault(self):
        gcv = self.clutOffset and f"{'x'.join(map(str, self.gridPoints))} grid" or 'not present'
        return " ".join([
            f"AC={self.acOffset and f','.join(map(str, self.ac))  or 'not present'},",
            f"BC={self.bcOffset and f','.join(map(str, self.bc))  or 'not present'},",
            f"MC={self.mcOffset and f','.join(map(str, self.mc))  or 'not present'},",
            f"CLUT={gcv},",
            f"matrix={self.matrixOffset and 'present'  or 'not present'}",
        ])


registerType(lutAToBType)
