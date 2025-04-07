import codecs
import logging

log = logging.getLogger(__name__)


class DataFile:
    def __init__(self, fileh, encoding='petscii-c64en-uc'):
        self.lines = []
        try:
            _ = codecs.lookup(encoding)
        except LookupError:
            log.warning("PETSCII codecs not available, using ASCII")
            encoding = 'ascii'
        self.encoding = encoding

        line_encoded = bytearray()
        while fileh:
            b = fileh.read(1)
            if b == b'':
                # EOF
                break
            if b == b'\r':
                # CR
                self.lines.append(line_encoded)
                line_encoded = bytearray()
            elif b != b'\x00':
                # not NUL
                line_encoded += b

    def from_text(self, fileh):
        """Create from Unicode text."""
        for line in fileh:
            line = line.rstrip('\n')
            try:
                self.lines.append(line.expandtabs().encode(self.encoding))
            except UnicodeEncodeError:
                raise ValueError("Unable to encode line: "+line)

    def to_binary(self):
        """Generator to return the file as binary."""
        for line in self.lines:
            yield line+b'\r'

    def to_text(self):
        """Generator to return lines as Unicode text."""
        for line in self.lines:
            try:
                yield line.decode(self.encoding)
            except UnicodeDecodeError:
                raise ValueError("Unable to decode line: "+str(line))
