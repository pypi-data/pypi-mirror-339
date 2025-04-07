from .tokensets import _token_set_register
from .tokenset_basic_v3_5 import TokenSet_BASICv3_5


_basic_v7_tokens = (
    ("POT", b'\xCE\x02'),
    ("BUMP", b'\xCE\x03'),
    ("PEN", b'\xCE\x04'),
    ("RSPPOS", b'\xCE\x05'),
    ("RSPRITE", b'\xCE\x06'),
    ("RSPCOLOR", b'\xCE\x07'),
    ("XOR", b'\xCE\x08'),
    ("RWINDOW", b'\xCE\x09'),
    ("POINTER", b'\xCE\x0A'),
    ("BANK", b'\xFE\x02'),
    ("FILTER", b'\xFE\x03'),
    ("PLAY", b'\xFE\x04'),
    ("TEMPO", b'\xFE\x05'),
    ("MOVSPR", b'\xFE\x06'),
    ("SPRITE", b'\xFE\x07'),
    ("SPRCOLOR", b'\xFE\x08'),
    ("RREG", b'\xFE\x09'),
    ("ENVELOPE", b'\xFE\x0A'),
    ("SLEEP", b'\xFE\x0B'),
    ("CATALOG", b'\xFE\x0C'),
    ("DOPEN", b'\xFE\x0D'),
    ("APPEND", b'\xFE\x0E'),
    ("DCLOSE", b'\xFE\x0F'),
    ("BSAVE", b'\xFE\x10'),
    ("BLOAD", b'\xFE\x11'),
    ("RECORD", b'\xFE\x12'),
    ("CONCAT", b'\xFE\x13'),
    ("DVERIFY", b'\xFE\x14'),
    ("DCLEAR", b'\xFE\x15'),
    ("SPRSAVE", b'\xFE\x16'),
    ("COLLISION", b'\xFE\x17'),
    ("BEGIN", b'\xFE\x18'),
    ("BEND", b'\xFE\x19'),
    ("WINDOW", b'\xFE\x1A'),
    ("BOOT", b'\xFE\x1B'),
    ("WIDTH", b'\xFE\x1C'),
    ("SPRDEF", b'\xFE\x1D'),
    ("QUIT", b'\xFE\x1E'),
    ("STASH", b'\xFE\x1F'),
    ("FETCH", b'\xFE\x21'),
    ("SWAP", b'\xFE\x23'),
    ("OFF", b'\xFE\x24'),
    ("FAST", b'\xFE\x25'),
    ("SLOW", b'\xFE\x026')
    )


class TokenSet_BASICv7(TokenSet_BASICv3_5):
    """Tokens used by BASIC 7."""
    def __init__(self):
        super().__init__()
        self.delete_token("RLUM")
        self.add_tokens(_basic_v7_tokens)


_token_set_register['basic-v7'] = TokenSet_BASICv7()
