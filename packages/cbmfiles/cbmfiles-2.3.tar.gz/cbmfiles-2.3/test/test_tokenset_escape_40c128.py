import unittest

from cbm_files.tokenset_escape_40c128 import TokenSet_Escape40C128


class TestEscape40C128(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_Escape40C128()
        self.assertEqual(tokenset.tokenize('{red}'), (b'\x1c', '{red}'))
        self.assertEqual(tokenset.tokenize('{lred}'), (b'\x96', '{lred}'))
        self.assertEqual(tokenset.tokenize('{tab}'), (b'\x09', '{tab}'))
        self.assertEqual(tokenset.tokenize('{ensh}'), (b'\x0b', '{ensh}'))

    def test_expand(self):
        tokenset = TokenSet_Escape40C128()
        self.assertEqual(tokenset.expand(b'\x1c'), ('{red}', b'\x1c'))
        self.assertEqual(tokenset.expand(b'\x96'), ('{lred}', b'\x96'))
        self.assertEqual(tokenset.expand(b'\x09'), ('{tab}', b'\x09'))
        self.assertEqual(tokenset.expand(b'\x0b'), ('{ensh}', b'\x0b'))
