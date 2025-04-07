import unittest

from cbm_files.tokenset_basic_v7 import TokenSet_BASICv7


class TestBasicV7(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_BASICv7()
        self.assertEqual(tokenset.tokenize('SYS'), (b'\x9e', 'SYS'))
        self.assertEqual(tokenset.tokenize('SOUND'), (b'\xda', 'SOUND'))
        self.assertEqual(tokenset.tokenize('PEN'), (b'\xce\x04', 'PEN'))
        self.assertEqual(tokenset.tokenize('APPEND'), (b'\xfe\x0e', 'APPEND'))
        self.assertEqual(tokenset.tokenize('DIRECTORY'), (b'\xee', 'DIRECTORY'))

    def test_expand(self):
        tokenset = TokenSet_BASICv7()
        self.assertEqual(tokenset.expand(b'\x9e'), ('SYS', b'\x9e'))
        self.assertEqual(tokenset.expand(b'\xda'), ('SOUND', b'\xda'))
        self.assertEqual(tokenset.expand(b'\xce\x04'), ('PEN', b'\xce\x04'))
        self.assertEqual(tokenset.expand(b'\xfe\x0e'), ('APPEND', b'\xfe\x0e'))
        self.assertEqual(tokenset.expand(b'\xee'), ('DIRECTORY', b'\xee'))
