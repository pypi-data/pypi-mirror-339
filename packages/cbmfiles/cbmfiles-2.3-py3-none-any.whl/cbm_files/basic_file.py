import codecs
import logging
import re
import struct

from . import tokensets
from . import tokenset_basic_v2  # noqa: F401
from . import tokenset_basic_v3_5  # noqa: F401
from . import tokenset_basic_v4  # noqa: F401
from . import tokenset_basic_v7  # noqa: F401
from . import tokenset_simons_basic  # noqa: F401
from . import tokenset_vic20_super_expander  # noqa: F401
from . import tokenset_vic20_super_expander_jp  # noqa: F401
from . import tokenset_escape_40c128  # noqa: F401
from . import tokenset_escape_80c128  # noqa: F401
from . import tokenset_escape_c16  # noqa: F401
from . import tokenset_escape_c64  # noqa: F401
from . import tokenset_escape_pet2001  # noqa: F401
from . import tokenset_escape_vic20  # noqa: F401


log = logging.getLogger(__name__)


class InvalidFormatError(Exception):
    pass


class BASICFile:
    line_re = re.compile(r'(\d+) *(.*)')

    def __init__(self, fileh, start_addr=None, token_set='basic-v2', encoding='petscii-c64en-uc'):
        if start_addr is None and fileh is not None:
            # read start address from file
            data = fileh.read(2)
            if len(data) != 2:
                raise InvalidFormatError("Invalid start address")
            self.start_addr, = struct.unpack('<H', data)
        else:
            self.start_addr = start_addr
        self.lines = {}

        self.token_set = token_set
        try:
            _ = codecs.lookup(encoding)
        except LookupError:
            log.warning("PETSCII codecs not available, using ASCII")
            encoding = 'ascii'
        self.encoding = encoding

        while fileh is not None:
            # link to start of next line (or NULL)
            data = fileh.read(2)
            if len(data) != 2:
                raise InvalidFormatError("Invalid link address")
            link, = struct.unpack('<H', data)

            if link == 0:
                # final line, NUL follows
                break

            data = fileh.read(2)
            if len(data) != 2:
                raise InvalidFormatError("Invalid line number")
            line_no, = struct.unpack('<H', data)

            # encoded line ends with NUL
            line_encoded = bytearray()
            while True:
                b = fileh.read(1)
                if len(b) == 0:
                    raise InvalidFormatError("Missing EOL")
                if b == b'\x00':
                    # EOL
                    break
                line_encoded += b

            self.add_encoded_line(line_no, line_encoded)

    def from_text(self, fileh):
        """Tokenize text file."""
        for line in fileh:
            m = self.line_re.match(line.strip())
            if m is None:
                raise ValueError("Syntax error in line: "+line)
            try:
                self.add_line(int(m.group(1)), m.group(2))
            except UnicodeEncodeError:
                raise ValueError("Unable to encode line: "+line)

    def to_binary(self, start_addr=None, prepend_addr=True):
        """Generator to return the program as binary."""
        if start_addr is None:
            start_addr = self.start_addr
        if prepend_addr:
            if start_addr is None:
                raise ValueError("No start address")
            yield struct.pack('<H', start_addr)

        for line_no, line_encoded in self.lines.items():
            start_addr += len(line_encoded) + 5
            yield struct.pack('<HH', start_addr, line_no) + line_encoded + b'\x00'

        yield b'\x00' * 2

    def to_text(self, start=0, end=65535):
        """Generator to return the program as Unicode text."""
        if end < start:
            raise ValueError("End {} is before start {}".format(end, start))
        for line_no, line_encoded in self.lines.items():
            if line_no >= start and line_no <= end:
                yield "{} {}".format(line_no, self.expand(line_encoded))

    def merge(self, other):
        """Merge the lines of one program into another."""
        for line_no, line_encoded in other.lines.items():
            self.add_encoded_line(line_no, line_encoded)

    def renumber(self, line_start, line_inc, range_start=None, range_end=None):
        """
        Return a new object where lines between `range_start` & `range_end` are
        renumbered from `line_start` in `line_inc` increments.
        """
        if range_start is None:
            range_start = 0
        if range_end is None:
            range_end = 65535
        if range_end < range_start:
            raise ValueError("Range end {} is before start {}".format(range_end, range_start))
        if line_start < 0:
            raise ValueError("Line start is negative")
        if line_inc < 0:
            raise ValueError("Line increment is negative")

        transform_map = {}

        # build the line number mapping, old -> new
        for line_no in self.lines.keys():
            if line_no >= range_start and line_no <= range_end:
                if line_start > 65535:
                    raise ValueError("New line number too large")
                transform_map[line_no] = line_start
                line_start += line_inc

        # check no new line collides with a line not being renumbered
        unchanged = set(self.lines.keys())-set(transform_map.keys())
        if unchanged & set(transform_map.values()):
            raise ValueError("Renumbered lines would intersect with unchanged lines")

        other = BASICFile(None, start_addr=self.start_addr)
        tokenizer = tokensets.lookup(self.token_set)

        # replace transformed line numbers in the encoded line and add at new line number
        for line_no, line_encoded in self.lines.items():
            renumbered_line = tokenizer.renumber(line_encoded, transform_map)
            other.add_encoded_line(transform_map.get(line_no, line_no), renumbered_line)

        return other

    def add_line(self, line_no, line):
        """Add a line in the form of text."""
        self.add_encoded_line(line_no, self.tokenize(line))

    def delete_line(self, line_no):
        del self.lines[line_no]

    def add_encoded_line(self, line_no, line_encoded):
        """Add or replace a line in its correct position."""
        self.lines[line_no] = line_encoded
        self.lines = dict(sorted(self.lines.items(), key=lambda x: x[0]))

    @staticmethod
    def escape_set_name(encoding):
        """Return the name of the escape token set based on the encoding name."""
        if '-' in encoding:
            # format is 'petscii-<machine><lang>-<case>'
            machine = encoding.split('-')[1]
            return 'escape-'+machine[:-2]
        return 'escape-c64'

    def tokenize(self, line):
        """Convert a line of text to a binary encoded form."""
        tokenizer = tokensets.lookup(self.token_set)
        escaper = tokensets.lookup(self.escape_set_name(self.encoding))
        ret = bytearray()
        in_quote = False
        skip_to_eol = False
        skip_to_next_statement = False
        ts = tokenizer

        while line:
            if line[0] == '"':
                in_quote = not in_quote
                ts = escaper if in_quote else tokenizer
                ret.append(ord('"'))
                line = line[1:]
                continue

            if line[0] == '~':
                # escaped hex character, e.g. '~2a'
                ret.append(int(line[1:3], 16))
                line = line[3:]
                continue

            token, match = ts.tokenize(line)
            if token is not None:
                if in_quote or not (skip_to_eol or skip_to_next_statement):
                    ret += token
                    line = line[len(match):]
                    if not in_quote:
                        skip_to_eol = token == ts.skip_tokenize_eol
                        skip_to_next_statement = token == ts.skip_tokenize_next_statement
                    continue

            if not in_quote and line[0] == ':':
                skip_to_next_statement = False

            ret += line[0].encode(self.encoding)
            line = line[1:]

        return ret

    def expand(self, line_encoded):
        """Convert a binary encoded line to text."""
        tokenizer = tokensets.lookup(self.token_set)
        escaper = tokensets.lookup(self.escape_set_name(self.encoding))
        ret = ''
        in_quote = False
        ts = tokenizer

        while line_encoded:
            if line_encoded[0] == ord('"'):
                in_quote = not in_quote
                ts = escaper if in_quote else tokenizer
                line_encoded = line_encoded[1:]
                ret += '"'
                continue

            token, match = ts.expand(line_encoded)
            if token is not None:
                if in_quote:
                    ret += token
                else:
                    try:
                        ret += token.encode('ascii').decode(self.encoding)
                    except UnicodeEncodeError:
                        # characters like '↑', 'π'
                        ret += token
                line_encoded = line_encoded[len(match):]
                continue

            ret += bytes([line_encoded[0]]).decode(self.encoding)
            line_encoded = line_encoded[1:]

        return ret
