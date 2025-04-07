from .tokensets import _token_set_register
from .tokenset_basic_v2 import TokenSet_BASICv2


_basic_v4_tokens = (
    ("CONCAT", b'\xCC'),
    ("DOPEN", b'\xCD'),
    ("DCLOSE", b'\xCE'),
    ("RECORD", b'\xCF'),
    ("HEADER", b'\xD0'),
    ("COLLECT", b'\xD1'),
    ("BACKUP", b'\xD2'),
    ("COPY", b'\xD3'),
    ("APPEND", b'\xD4'),
    ("DSAVE", b'\xD5'),
    ("DLOAD", b'\xD6'),
    ("CATALOG", b'\xD7'),
    ("RENAME", b'\xD8'),
    ("SCRATCH", b'\xD9'),
    ("DIRECTORY", b'\xDA'),
    ("DCLEAR", b'\xDB'),
    ("BANK", b'\xDC'),
    ("BLOAD", b'\xDD'),
    ("BSAVE", b'\xDE')
    )


class TokenSet_BASICv4(TokenSet_BASICv2):
    """Tokens used by BASIC 4.0."""
    def __init__(self):
        super().__init__()
        self.add_tokens(_basic_v4_tokens)


_token_set_register['basic-v4'] = TokenSet_BASICv4()
