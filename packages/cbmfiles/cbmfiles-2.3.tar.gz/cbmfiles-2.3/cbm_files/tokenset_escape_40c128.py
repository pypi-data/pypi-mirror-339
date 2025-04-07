from .tokensets import _token_set_register
from .tokenset_escape_c64 import TokenSet_EscapeC64


_escape_40c128_tokens = (
    ("{bel}", b'\x07'),
    ("{tab}", b'\x09'),
    ("{lf}", b'\x0A'),
    ("{ensh}", b'\x0B'),
    ("{dish}", b'\x0C'),
    ("{hts}", b'\x18'),
    ("{esc}", b'\x1B')
    )


class TokenSet_Escape40C128(TokenSet_EscapeC64):
    def __init__(self):
        super().__init__()
        self.add_tokens(_escape_40c128_tokens)


_token_set_register['escape-40c128'] = TokenSet_Escape40C128()
