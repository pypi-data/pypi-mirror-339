from .tokensets import _token_set_register
from .tokenset_escape_c64 import TokenSet_EscapeC64


_escape_80c128_tokens = (
    ("{ulon}", b'\x02'),
    ("{bel}", b'\x07'),
    ("{tab}", b'\x09'),
    ("{lf}", b'\x0A'),
    ("{ensh}", b'\x0B'),
    ("{dish}", b'\x0C'),
    ("{flon}", b'\x0F'),
    ("{hts}", b'\x18'),
    ("{esc}", b'\x1B'),
    ("{dpur}", b'\x81'),
    ("{ulof}", b'\x82'),
    ("{flof}", b'\x8F'),
    ("{dyel}", b'\x95'),
    ("{dcyn}", b'\x97')
    )


class TokenSet_Escape80C128(TokenSet_EscapeC64):
    def __init__(self):
        super().__init__()
        self.delete_token("{orng}")
        self.delete_token("{brn}")
        self.delete_token("{gry1}")
        self.add_tokens(_escape_80c128_tokens)


_token_set_register['escape-80c128'] = TokenSet_Escape80C128()
