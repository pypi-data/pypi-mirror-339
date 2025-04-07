from .tokensets import _token_set_register
from .tokenset_basic_v2 import TokenSet_BASICv2


_basic_ycxb_tokens = (
    ("MODE", b'\xCC'),
    ("CLB", b'\xCD'),
    ("CLS", b'\xCE'),
    ("CLG", b'\xCF'),
    ("AT", b'\xD0'),
    ("INK", b'\xD1'),
    ("AUX", b'\xD2'),
    ("VDU", b'\xD3'),
    ("VOL", b'\xD4'),
    ("CHAN", b'\xD5'),
    ("SOUND", b'\xD6'),
    ("SET", b'\xD7'),
    ("RSET", b'\xD8'),
    ("GCOL", b'\xD9'),
    ("HALT", b'\xDA'),
    ("UDG", b'\xDB'),
    ("CHAIN", b'\xDC'),
    ("PUT", b'\xDD'),
    ("RPT", b'\xDE'),
    ("INV", b'\xDF'),
    ("UPS", b'\xE0'),
    ("DNS", b'\xE1'),
    ("PLACE", b'\xE2'),
    ("CHAR", b'\xE3'),
    ("KEY", b'\xE4')
    )


class TokenSet_BASIC_ycxb(TokenSet_BASICv2):
    """Tokens used by Your Computer Extended Basic."""
    def __init__(self):
        super().__init__()
        self.add_tokens(_basic_ycxb_tokens)


_token_set_register['basic-ycxb'] = TokenSet_BASIC_ycxb()
