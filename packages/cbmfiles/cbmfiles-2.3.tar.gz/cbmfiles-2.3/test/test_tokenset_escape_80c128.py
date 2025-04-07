import unittest

from cbm_files.tokenset_escape_80c128 import TokenSet_Escape80C128


class TestEscape80C128(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_Escape80C128()
        self.assertEqual(tokenset.tokenize('{red}'), (b'\x1c', '{red}'))
        self.assertEqual(tokenset.tokenize('{lred}'), (b'\x96', '{lred}'))
        self.assertEqual(tokenset.tokenize('{tab}'), (b'\x09', '{tab}'))
        self.assertEqual(tokenset.tokenize('{ensh}'), (b'\x0b', '{ensh}'))
        self.assertEqual(tokenset.tokenize('{ulon}'), (b'\x02', '{ulon}'))
        self.assertEqual(tokenset.tokenize('{dpur}'), (b'\x81', '{dpur}'))
        self.assertEqual(tokenset.tokenize('{dyel}'), (b'\x95', '{dyel}'))
        self.assertEqual(tokenset.tokenize('{dcyn}'), (b'\x97', '{dcyn}'))
        self.assertEqual(tokenset.tokenize('{orng}'), (None, None))
        self.assertEqual(tokenset.tokenize('{brn}'), (None, None))
        self.assertEqual(tokenset.tokenize('{gry1}'), (None, None))

    def test_expand(self):
        tokenset = TokenSet_Escape80C128()
        self.assertEqual(tokenset.expand(b'\x1c'), ('{red}', b'\x1c'))
        self.assertEqual(tokenset.expand(b'\x96'), ('{lred}', b'\x96'))
        self.assertEqual(tokenset.expand(b'\x09'), ('{tab}', b'\x09'))
        self.assertEqual(tokenset.expand(b'\x0b'), ('{ensh}', b'\x0b'))
        self.assertEqual(tokenset.expand(b'\x02'), ('{ulon}', b'\x02'))
        self.assertEqual(tokenset.expand(b'\x81'), ('{dpur}', b'\x81'))
        self.assertEqual(tokenset.expand(b'\x95'), ('{dyel}', b'\x95'))
        self.assertEqual(tokenset.expand(b'\x97'), ('{dcyn}', b'\x97'))
