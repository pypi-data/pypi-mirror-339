import unittest
import io

from cbm_files.user_file import UserFile


class TestUserFile(unittest.TestCase):
    def test_user_file_read(self):
        mock_file = io.BytesIO(b'\x00\x06\x09'
                               b'ABCDEFGHI'
                               b'\x6f')
        user_file = UserFile(mock_file)
        start_addr, data = user_file.read()
        self.assertEqual(start_addr, 0x600)
        self.assertEqual(data, b'ABCDEFGHI')

    def test_user_file_write(self):
        mock_file = io.BytesIO()
        user_file = UserFile(mock_file, start_addr=0x500)
        user_file.write(b'MNBVCXZ')
        data = mock_file.getbuffer()
        self.assertEqual(data[:3], b'\x00\x05\x07')
        self.assertEqual(data[3:-1], b'MNBVCXZ')
        self.assertEqual(data[-1], 0x2a)
