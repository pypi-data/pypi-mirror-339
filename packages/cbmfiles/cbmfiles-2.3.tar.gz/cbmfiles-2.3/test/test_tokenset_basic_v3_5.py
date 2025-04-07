import unittest

from cbm_files.tokenset_basic_v3_5 import TokenSet_BASICv3_5


class TestBasicV3_5(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_BASICv3_5()
        self.assertEqual(tokenset.tokenize('SYS'), (b'\x9e', 'SYS'))
        self.assertEqual(tokenset.tokenize('DIRECTORY'), (b'\xee', 'DIRECTORY'))

    def test_expand(self):
        tokenset = TokenSet_BASICv3_5()
        self.assertEqual(tokenset.expand(b'\x9e'), ('SYS', b'\x9e'))
        self.assertEqual(tokenset.expand(b'\xee'), ('DIRECTORY', b'\xee'))
