from .tokensets import _token_set_register
from .tokenset_basic_v2 import TokenSet_BASICv2


_vic20_super_expander_jp_tokens = (
    ("HIRES", b'\xCC'),
    ("SOUND(", b'\0xCD'),
    ("TEXT", b'\xCE'),
    ("PLOT", b'\xCF'),
    ("BOX", b'\xD0'),
    ("CIRCLE", b'\xD1'),
    ("PAINT", b'\xD2'),
    ("SETC", b'\xD3'),
    ("TEMPO", b'\xD4'),
    ("MUSIC", b'\xD5'),
    ("KEY", b'\xD6'),
    ("PIANO", b'\xD7'),
    ("LOCATE", b'\xD8'),
    ("CHAR", b'\xD9'),
    ("RELEASE", b'\xDA'),
    ("PDL", b'\xDB'),
    ("JOY", b'\xDC'),
    ("LIGHTX", b'\xDD'),
    ("LIGHTY", b'\xDE'),
    ("POINT", b'\xDF'),
    ("FGC", b'\xE0'),
    ("BGC", b'\xE1'),
    ("BDC", b'\xE2')
    )


class TokenSet_VIC20_SuperExpander_JP(TokenSet_BASICv2):
    """Tokens used by Super Expander (VIC-1211/1211M)."""
    def __init__(self):
        super().__init__()
        self.add_tokens(_vic20_super_expander_jp_tokens)


_token_set_register['vic20-super-expander-jp'] = TokenSet_VIC20_SuperExpander_JP()
