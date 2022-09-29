import pytest
from .type import getTypeImplementation
from io import BytesIO


fixture = b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x0cenUS\x00\x00\x00$\x00\x00\x00\x1c\x00T\x00h\x00i\x00s\x00 \x00i\x00s\x00 \x00a\x00n\x00 \x00e\x00x\x00a\x00m\x00p\x00l\x00e'  # noqa


class TestMultiLocalizedUnicodeType(object):
    def setup_method(self):
        self.obj = getTypeImplementation(BytesIO(fixture), b'mluc', 0, 0)
        self.obj.read()

    def test_read(self):
        assert self.obj.getDefault() == "This is an example"

    def test_str(self):
        assert str(self.obj) == "<Type mluc: This is an example>"
