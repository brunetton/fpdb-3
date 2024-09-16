import sys
import pytest
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import Configuration
from Charset import *


class TestToUtf8:
    # Tests that an empty string is returned as is
    def test_empty_string(self):
        assert to_utf8('') == ''

    # Tests that an ASCII string is converted to UTF-8 encoding
    def test_ascii_string(self):
        assert to_utf8('hello') == 'hello'



    # Tests that an already encoded string is returned as is
    def test_already_encoded_string(self):
        assert to_utf8(b'hello') == b'hello'


