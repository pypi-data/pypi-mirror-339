from .tokensets import _token_set_register
from .tokenset_escape_vic20 import TokenSet_EscapeVIC20


_escape_c64_tokens = (
    ("{orng}", b'\x81'),
    ("{brn}", b'\x95'),
    ("{lred}", b'\x96'),
    ("{gry1}", b'\x97'),
    ("{gry2}", b'\x98'),
    ("{lgrn}", b'\x99'),
    ("{lblu}", b'\x9A'),
    ("{gry3}", b'\x9B')
    )


class TokenSet_EscapeC64(TokenSet_EscapeVIC20):
    def __init__(self):
        super().__init__()
        self.add_tokens(_escape_c64_tokens)


_token_set_register['escape-c64'] = TokenSet_EscapeC64()
