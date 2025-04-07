import struct


class CRCMismatchError(Exception):
    pass


class UserFile:
    def __init__(self, fileh, start_addr=None):
        self.fileh = fileh
        self.start_addr = start_addr

    def write(self, data, start_addr=None):
        """Write a data section, continuing the previous one if `start_addr` is absent."""
        if start_addr is None:
            start_addr = self.start_addr

        if start_addr is None:
            raise ValueError("No start address")
        if len(data) == 0 or len(data) > 256:
            raise ValueError("Invalid data length")

        csum = self._calc_csum(data)

        payload = struct.pack('<HB', start_addr, len(data))
        payload += data
        payload += bytes([csum])
        self.fileh.write(payload)
        self.start_addr = start_addr+len(data)

    def read(self):
        """Read the next data section."""
        header = self.fileh.read(3)
        start_addr, data_len = struct.unpack('<HB', header)
        data = self.fileh.read(data_len)
        csum = ord(self.fileh.read(1))

        calc_csum = self._calc_csum(data)
        if calc_csum != csum:
            raise CRCMismatchError("CRC mismatch, computed {}, read {}".format(calc_csum, csum))

        return start_addr, data

    @staticmethod
    def _calc_csum(data):
        csum = 0
        for b in data:
            csum += b
            if csum > 0xFF:
                csum &= 0xFF
                csum += 1
        return csum
