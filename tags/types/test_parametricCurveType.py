import pytest
from .type import getTypeImplementation
from io import BytesIO


fixture_type0 = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00'  # noqa
fixture_type1 = b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00'  # noqa
fixture_type2 = b'\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00'  # noqa
fixture_type3 = b'\x00\x00\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00\x06\x00\x00'  # noqa
fixture_type4 = b'\x00\x00\x00\x00\x00\x04\x00\x00\x00\x05\x80\x00\x00\x03\x40\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00'  # noqa


class TestParametricCurveType(object):
    def test_type0(self):
        self.obj = getTypeImplementation(BytesIO(fixture_type0), b'para', 0, 0)
        self.obj.read()
        assert self.obj.g == 2.0
        assert self.obj.get(2.0) == 4.0
        assert str(self.obj) == '<Type para: curve type 0>'

    def test_type1(self):
        self.obj = getTypeImplementation(BytesIO(fixture_type1), b'para', 0, 0)
        self.obj.read()
        assert self.obj.g == 2.0
        assert self.obj.a == 3.0
        assert self.obj.b == 4.0
        assert self.obj.get(2.0) == 100.0
        assert str(self.obj) == '<Type para: curve type 1>'

    def test_type2(self):
        self.obj = getTypeImplementation(BytesIO(fixture_type2), b'para', 0, 0)
        self.obj.read()
        assert self.obj.g == 2.0
        assert self.obj.a == 3.0
        assert self.obj.b == 4.0
        assert self.obj.c == 5.0
        assert self.obj.get(2.0) == 105.0
        assert str(self.obj) == '<Type para: curve type 2>'

    def test_type3(self):
        self.obj = getTypeImplementation(BytesIO(fixture_type3), b'para', 0, 0)
        self.obj.read()
        assert self.obj.g == 2.0
        assert self.obj.a == 3.0
        assert self.obj.b == 4.0
        assert self.obj.c == 5.0
        assert self.obj.d == 6.0
        assert self.obj.get(2.0) == 10.0
        assert str(self.obj) == '<Type para: curve type 3>'

    def test_type4(self):
        self.obj = getTypeImplementation(BytesIO(fixture_type4), b'para', 0, 0)
        self.obj.read()
        assert self.obj.g == 5.5
        assert self.obj.a == 3.25
        assert self.obj.b == 0.0
        assert self.obj.c == 1.0
        assert self.obj.d == 3.0
        assert self.obj.e == 3.0
        assert self.obj.f == 4.0
        assert self.obj.get(2.0) == 6.0
        assert str(self.obj) == '<Type para: curve type 4>'
