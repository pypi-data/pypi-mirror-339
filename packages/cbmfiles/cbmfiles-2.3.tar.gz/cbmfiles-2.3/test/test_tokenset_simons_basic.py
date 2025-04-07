import unittest

from cbm_files.tokenset_simons_basic import TokenSet_Simons_BASIC


class TestBasicV2(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_Simons_BASIC()
        self.assertEqual(tokenset.tokenize('SYS'), (b'\x9e', 'SYS'))
        self.assertEqual(tokenset.tokenize('COPY'), (b'\x64\x77', 'COPY'))
        self.assertEqual(tokenset.tokenize('LOW COL'), (b'\x64\x76', 'LOW COL'))

    def test_expand(self):
        tokenset = TokenSet_Simons_BASIC()
        self.assertEqual(tokenset.expand(b'\x9e'), ('SYS', b'\x9e'))
        self.assertEqual(tokenset.expand(b'\x64\x19'), ('MULTI', b'\x64\x19'))
