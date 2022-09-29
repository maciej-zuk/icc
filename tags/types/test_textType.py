import pytest
from .type import getTypeImplementation
from io import BytesIO


class TestTextType(object):
    def setup_method(self):
        self.obj = getTypeImplementation(BytesIO(b"texttest"), b'text', 0, 8+4)
        self.obj.read()

    def test_read(self):
        assert self.obj.getDefault() == "test"

    def test_str(self):
        assert str(self.obj) == "<Type text: test>"
