from .tokensets import _token_set_register
from .tokenset_escape_pet2001 import TokenSet_EscapePet2001


_escape_vic20_tokens = (
    ("{wht}", b'\x05'),
    ("{dish}", b'\x08'),
    ("{ensh}", b'\x09'),
    ("{red}", b'\x1C'),
    ("{grn}", b'\x1E'),
    ("{blu}", b'\x1F'),
    ("{f1}", b'\x85'),
    ("{f3}", b'\x86'),
    ("{f5}", b'\x87'),
    ("{f7}", b'\x88'),
    ("{f2}", b'\x89'),
    ("{f4}", b'\x8A'),
    ("{f6}", b'\x8B'),
    ("{f8}", b'\x8C'),
    ("{blk}", b'\x90'),
    ("{pur}", b'\x9C'),
    ("{yel}", b'\x9E'),
    ("{cyn}", b'\x9F')
    )


class TokenSet_EscapeVIC20(TokenSet_EscapePet2001):
    def __init__(self):
        super().__init__()
        self.add_tokens(_escape_vic20_tokens)


_token_set_register['escape-vic20'] = TokenSet_EscapeVIC20()
_token_set_register['escape-vic1001'] = TokenSet_EscapeVIC20()
