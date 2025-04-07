import unittest

from cbm_files.tokenset_basic_v2 import TokenSet_BASICv2


class TestBasicV2(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_BASICv2()
        self.assertEqual(tokenset.tokenize('SYS'), (b'\x9e', 'SYS'))
        self.assertEqual(tokenset.tokenize('XZY'), (None, None))

    def test_expand(self):
        tokenset = TokenSet_BASICv2()
        self.assertEqual(tokenset.expand(b'\x9e'), ('SYS', b'\x9e'))
        self.assertEqual(tokenset.expand(b'\x00\x01'), (None, None))

    def test_renumber_split(self):
        tokenset = TokenSet_BASICv2()
        # 'GOTO10:PRINT20'
        self.assertEqual(list(tokenset.renumber_split(b'\x8910:\x9920')), [b'\x89', 10, b':\x9920'])
        # 'ONAGOTO10,20'
        self.assertEqual(list(tokenset.renumber_split(b'\x91A\x8910,20')), [b'\x91A\x89', 10, b',', 20])
        # 'PRINT"<$8D>5"'
        self.assertEqual(list(tokenset.renumber_split(b'\x99"\x8D5"')), [b'\x99"\x8D5"'])
        # 'GO TO 30'
        self.assertEqual(list(tokenset.renumber_split(b'\xCB \xA4 30')), [b'\xCB \xA4 ', 30])
        # 'LIST40-50'
        self.assertEqual(list(tokenset.renumber_split(b'\x9B40\xAB50')), [b'\x9B', 40, b'\xAB', 50])
