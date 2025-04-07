from .tokensets import _token_set_register
from .tokenset_escape_vic20 import TokenSet_EscapeVIC20


_escape_c16_tokens = (
    ("{esc}", b'\x1B'),
    ("{orng}", b'\x81'),
    ("{flon}", b'\x82'),
    ("{flof}", b'\x84'),
    ("{help}", b'\x8C'),
    ("{brn}", b'\x95'),
    ("{ylgn}", b'\x96'),
    ("{pink}", b'\x97'),
    ("{blgr}", b'\x98'),
    ("{lblu}", b'\x99'),
    ("{dblu}", b'\x9A'),
    ("{lgrn}", b'\x9B')
    )


class TokenSet_EscapeC16(TokenSet_EscapeVIC20):
    def __init__(self):
        super().__init__()
        self.add_tokens(_escape_c16_tokens)


_token_set_register['escape-c16'] = TokenSet_EscapeC16()
