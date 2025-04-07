from .tokensets import TokenSet


_escape_pet2001_tokens = (
    ("{stop}", b'\x03'),
    ("{swlc}", b'\x0E'),
    ("{down}", b'\x11'),
    ("{rvon}", b'\x12'),
    ("{home}", b'\x13'),
    ("{del}", b'\x14'),
    ("{rght}", b'\x1D'),
    ("{sret}", b'\x8D'),
    ("{swuc}", b'\x8E'),
    ("{up}", b'\x91'),
    ("{rvof}", b'\x92'),
    ("{clr}", b'\x93'),
    ("{inst}", b'\x94'),
    ("{left}", b'\x9D')
    )


class TokenSet_EscapePet2001(TokenSet):
    def __init__(self):
        super().__init__()
        self.raw = True
        self.add_tokens(_escape_pet2001_tokens)
