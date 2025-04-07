from .tokensets import _token_set_register
from .tokenset_basic_v2 import TokenSet_BASICv2


_vic20_super_expander_tokens = (
    ("KEY", b'\xCC'),
    ("GRAPHIC", b'\xCD'),
    ("SCNCLR", b'\xCE'),
    ("CIRCLE", b'\xCF'),
    ("DRAW", b'\xD0'),
    ("REGION", b'\xD1'),
    ("COLOR", b'\xD2'),
    ("POINT", b'\xD3'),
    ("SOUND", b'\xD4'),
    ("CHAR", b'\xD5'),
    ("PAINT", b'\xD6'),
    ("RPOT", b'\xD7'),
    ("RPEN", b'\xD8'),
    ("RSND", b'\xD9'),
    ("RCOLR", b'\xDA'),
    ("RGR", b'\xDB'),
    ("RJOY", b'\xDC'),
    ("RDOT", b'\xDD')
    )


class TokenSet_VIC20_SuperExpander(TokenSet_BASICv2):
    """Tokens used by Super Expander (VIC-1211A)."""
    def __init__(self):
        super().__init__()
        self.add_tokens(_vic20_super_expander_tokens)


_token_set_register['vic20-super-expander'] = TokenSet_VIC20_SuperExpander()
