import pytest
from .type import getTypeImplementation
from io import BytesIO


class TestTextDescriptionType(object):
    def setup_method(self):
        self.obj = getTypeImplementation(BytesIO(b"\x00\x00\x00\x00\x00\x00\x00\x0ctest"), b'desc', 0, 8+4)
        self.obj.read()

    def test_read(self):
        assert self.obj.getDefault() == "test"

    def test_str(self):
        assert str(self.obj) == "<Type desc: test>"
