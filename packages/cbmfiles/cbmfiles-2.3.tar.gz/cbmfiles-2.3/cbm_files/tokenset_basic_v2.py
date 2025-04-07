from .tokensets import TokenSet, _token_set_register


_basic_v2_tokens = (
    ("END", b'\x80'),
    ("FOR", b'\x81'),
    ("NEXT", b'\x82'),
    ("DATA", b'\x83'),
    ("INPUT#", b'\x84'),
    ("INPUT", b'\x85'),
    ("DIM", b'\x86'),
    ("READ", b'\x87'),
    ("LET", b'\x88'),
    ("GOTO", b'\x89'),
    ("RUN", b'\x8A'),
    ("IF", b'\x8B'),
    ("RESTORE", b'\x8C'),
    ("GOSUB", b'\x8D'),
    ("RETURN", b'\x8E'),
    ("REM", b'\x8F'),
    ("STOP", b'\x90'),
    ("ON", b'\x91'),
    ("WAIT", b'\x92'),
    ("LOAD", b'\x93'),
    ("SAVE", b'\x94'),
    ("VERIFY", b'\x95'),
    ("DEF", b'\x96'),
    ("POKE", b'\x97'),
    ("PRINT#", b'\x98'),
    ("PRINT", b'\x99'),
    ("CONT", b'\x9A'),
    ("LIST", b'\x9B'),
    ("CLR", b'\x9C'),
    ("CMD", b'\x9D'),
    ("SYS", b'\x9E'),
    ("OPEN", b'\x9F'),
    ("CLOSE", b'\xA0'),
    ("GET", b'\xA1'),
    ("NEW", b'\xA2'),
    ("TAB(", b'\xA3'),
    ("TO", b'\xA4'),
    ("FN", b'\xA5'),
    ("SPC(", b'\xA6'),
    ("THEN", b'\xA7'),
    ("NOT", b'\xA8'),
    ("STEP", b'\xA9'),
    ("+", b'\xAA'),
    ("-", b'\xAB'),
    ("*", b'\xAC'),
    ("/", b'\xAD'),
    ("↑", b'\xAE'),
    ("^", b'\xAE'),
    ("AND", b'\xAF'),
    ("OR", b'\xB0'),
    (">", b'\xB1'),
    ("=", b'\xB2'),
    ("<", b'\xB3'),
    ("SGN", b'\xB4'),
    ("INT", b'\xB5'),
    ("ABS", b'\xB6'),
    ("USR", b'\xB7'),
    ("FRE", b'\xB8'),
    ("POS", b'\xB9'),
    ("SQR", b'\xBA'),
    ("RND", b'\xBB'),
    ("LOG", b'\xBC'),
    ("EXP", b'\xBD'),
    ("COS", b'\xBE'),
    ("SIN", b'\xBF'),
    ("TAN", b'\xC0'),
    ("ATN", b'\xC1'),
    ("PEEK", b'\xC2'),
    ("LEN", b'\xC3'),
    ("STR$", b'\xC4'),
    ("VAL", b'\xC5'),
    ("ASC", b'\xC6'),
    ("CHR$", b'\xC7'),
    ("LEFT$", b'\xC8'),
    ("RIGHT$", b'\xC9'),
    ("MID$", b'\xCA'),
    ("GO", b'\xCB'),
    ("π", b'\xFF'),
    ("?", b'\x99')
    )


class TokenSet_BASICv2(TokenSet):
    def __init__(self):
        super().__init__()
        self.add_tokens(_basic_v2_tokens)
        self.skip_tokenize_next_statement = b'\x83'
        self.skip_tokenize_eol = b'\x8F'
        self.ren_tokens = (0x89, 0x8A, 0x8D, 0x9B, 0xA7)
        self.fold_case = True

    def renumber_split(self, line_encoded):
        """Yield a sequence of substrings and integer line numbers."""
        next_part = bytearray()
        in_quote = False
        last_token = None
        val = None

        for b in line_encoded:
            if val is not None:
                # processing a line number
                if b >= ord('0') and b <= ord('9'):
                    val = val*10+(b-ord('0'))
                    continue
                else:
                    # line number complete
                    yield val
                    val = None

            if not in_quote:
                if b >= ord('0') and b <= ord('9') and last_token in self.ren_tokens:
                    # new line number
                    yield next_part
                    next_part = bytearray()
                    val = b-ord('0')
                    continue

                if b >= 0x80:
                    if last_token == 0xCB and b == 0xA4:
                        # convert 'GO TO' into 'GOTO'
                        last_token = 0x89
                    # ignore '-' token to handle 'LIST#-#' correctly
                    elif last_token != 0x9B or b != 0xAB:
                        last_token = b
                elif b == ord(':'):
                    # next statement
                    last_token = None

            if b == ord('"'):
                in_quote = not in_quote

            next_part.append(b)

        if val is None:
            if next_part:
                yield next_part
        else:
            yield val


_token_set_register['basic-v2'] = TokenSet_BASICv2()
