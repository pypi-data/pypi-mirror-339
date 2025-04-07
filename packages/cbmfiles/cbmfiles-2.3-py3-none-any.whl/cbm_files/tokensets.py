
class TokenSet:
    def __init__(self):
        self.string_to_token = dict()
        self.skip_tokenize_next_statement = -1
        self.skip_tokenize_eol = -1
        self.fold_case = False

    def add_tokens(self, tokens):
        self.string_to_token.update(tokens)

    def delete_token(self, token):
        del self.string_to_token[token]

    def renumber(self, line_encoded, transform_map):
        ret = bytearray()
        for part in self.renumber_split(line_encoded):
            if isinstance(part, int):
                ret += str(transform_map.get(part, part)).encode('ascii')
            else:
                ret += part

        return ret

    def tokenize(self, line):
        """Return token and matching string or `None`, `None`."""
        for s, t in self.string_to_token.items():
            if self.fold_case:
                line = line.upper()
            if line.startswith(s):
                return t, s

        return None, None

    def expand(self, line_encoded):
        """Return string and matching token or `None`, `None`."""
        for s, t in self.string_to_token.items():
            if line_encoded.startswith(t):
                return s, t

        return None, None


_token_set_register = {}


def lookup(set_name):
    """Return the token set for a given name."""
    if set_name in _token_set_register:
        return _token_set_register[set_name]
    raise LookupError("unknown token set: "+set_name)


def token_set_names():
    return _token_set_register.keys()
