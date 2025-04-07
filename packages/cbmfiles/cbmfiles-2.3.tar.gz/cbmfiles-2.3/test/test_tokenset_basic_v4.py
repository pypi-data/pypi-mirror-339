import unittest

from cbm_files.tokenset_basic_v4 import TokenSet_BASICv4


class TestBasicV4(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_BASICv4()
        self.assertEqual(tokenset.tokenize('SYS'), (b'\x9e', 'SYS'))
        self.assertEqual(tokenset.tokenize('DIRECTORY'), (b'\xda', 'DIRECTORY'))

    def test_expand(self):
        tokenset = TokenSet_BASICv4()
        self.assertEqual(tokenset.expand(b'\x9e'), ('SYS', b'\x9e'))
        self.assertEqual(tokenset.expand(b'\xda'), ('DIRECTORY', b'\xda'))
