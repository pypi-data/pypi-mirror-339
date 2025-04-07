from .tokensets import _token_set_register
from .tokenset_basic_v2 import TokenSet_BASICv2


_basic_v3_5_tokens = (
    ("RGR", b'\xCC'),
    ("RLCR", b'\xCD'),
    ("RLUM", b'\xCE'),
    ("JOY", b'\xCF'),
    ("RDOT", b'\xD0'),
    ("DEC", b'\xD1'),
    ("HEX$",b'\0xD2'),
    ("ERR$",b'\0xD3'),
    ("INSTR", b'\xD4'),
    ("ELSE", b'\xD5'),
    ("RESUME", b'\xD6'),
    ("TRAP", b'\xD7'),
    ("TRON", b'\xD8'),
    ("TROFF", b'\xD9'),
    ("SOUND", b'\xDA'),
    ("VOL", b'\xDB'),
    ("AUTO", b'\xDC'),
    ("PUDEF", b'\xDD'),
    ("GRAPHIC", b'\xDE'),
    ("PAINT", b'\xDF'),
    ("CHAR", b'\xE0'),
    ("BOX", b'\xE1'),
    ("CIRCLE", b'\xE2'),
    ("GSHAPE", b'\xE3'),
    ("SSHAPE", b'\xE4'),
    ("DRAW", b'\xE5'),
    ("LOCATE", b'\xE6'),
    ("COLOR", b'\xE7'),
    ("SCNCLR", b'\xE8'),
    ("SCALE", b'\xE9'),
    ("HELP", b'\xEA'),
    ("DO", b'\xEB'),
    ("LOOP", b'\xEC'),
    ("EXIT", b'\xED'),
    ("DIRECTORY", b'\xEE'),
    ("DSAVE", b'\xEF'),
    ("DLOAD", b'\xF0'),
    ("HEADER", b'\xF1'),
    ("SCRATCH", b'\xF2'),
    ("COLLECT", b'\xF3'),
    ("COPY", b'\xF4'),
    ("RENAME", b'\xF5'),
    ("BACKUP", b'\xF6'),
    ("DELETE", b'\xF7'),
    ("RENUMBER", b'\xF8'),
    ("KEY", b'\xF9'),
    ("MONITOR", b'\xFA'),
    ("USING", b'\xFB'),
    ("UNTIL", b'\xFC'),
    ("WHILE", b'\xFD')
    )


class TokenSet_BASICv3_5(TokenSet_BASICv2):
    """Tokens used by BASIC 3.5."""
    def __init__(self):
        super().__init__()
        self.add_tokens(_basic_v3_5_tokens)


_token_set_register['basic-v3.5'] = TokenSet_BASICv3_5()
