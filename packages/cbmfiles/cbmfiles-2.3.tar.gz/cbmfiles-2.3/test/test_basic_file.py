import unittest
import io

from cbm_files.basic_file import BASICFile, InvalidFormatError


class TestBASICFile(unittest.TestCase):
    def test_read(self):
        mock_file = io.BytesIO(b'\x01\x12'
                               b'\x0d\x12\x0a\x00C\xb240703\x00'
                               b'\x14\x12d\x00\x87A\x00'
                               b'\x21\x12n\x00\x8bA\xb30\x89200\x00'
                               b'\x2a\x12x\x00\x97C,A\x00'
                               b'\x00\x00')
        prog = BASICFile(mock_file)
        self.assertEqual(list(prog.lines.keys()), [10, 100, 110, 120])

    def test_read_addr(self):
        mock_file = io.BytesIO(b'\x0d\x12\x0a\x00C\xb240703\x00'
                               b'\x14\x12d\x00\x87A\x00'
                               b'\x21\x12n\x00\x8bA\xb30\x89200\x00'
                               b'\x2a\x12x\x00\x97C,A\x00'
                               b'\x00\x00')
        prog = BASICFile(mock_file, start_addr=0x1201)
        self.assertEqual(list(prog.lines.keys()), [10, 100, 110, 120])

    def test_from_text(self):
        mock_file = io.StringIO("10 REM LINE 1\n30STOP\n")
        prog = BASICFile(None)
        prog.from_text(mock_file)
        self.assertEqual(list(prog.lines.keys()), [10, 30])
        self.assertEqual(prog.lines[30], b'\x90')

    def test_to_binary(self):
        prog = BASICFile(None)
        prog.add_line(10, 'C=40703')
        prog.add_line(100, 'READA')
        prog.add_line(110, 'IFA<0GOTO200')
        prog.add_line(120, 'POKEC,A')
        data = list(prog.to_binary(start_addr=0x1201, prepend_addr=False))
        self.assertEqual(data, [b'\x0d\x12\x0a\x00C\xb240703\x00',
                                b'\x14\x12d\x00\x87A\x00',
                                b'\x21\x12n\x00\x8bA\xb30\x89200\x00',
                                b'\x2a\x12x\x00\x97C,A\x00',
                                b'\x00\x00'])
        data = list(prog.to_binary(start_addr=0x1201))
        self.assertEqual(data[0], b'\x01\x12')

    def test_to_text(self):
        prog = BASICFile(None)
        prog.add_encoded_line(10, b'C\xb240703')
        prog.add_encoded_line(100, b'\x87A')
        prog.add_encoded_line(110, b'\x8bA\xb30\x89200')
        prog.add_encoded_line(120, b'\x97C,A')
        text = list(prog.to_text())
        self.assertEqual(text, ['10 C=40703', '100 READA', '110 IFA<0GOTO200', '120 POKEC,A'])

    def test_merge(self):
        prog1 = BASICFile(None)
        prog1.add_encoded_line(10, b'\x01')
        prog1.add_encoded_line(20, b'\x01')
        prog1.add_encoded_line(30, b'\x01')
        prog2 = BASICFile(None)
        prog2.add_encoded_line(15, b'\x02')
        prog2.add_encoded_line(20, b'\x02')
        prog2.add_encoded_line(25, b'\x02')
        prog1.merge(prog2)
        self.assertEqual(list(prog1.lines.keys()), [10, 15, 20, 25, 30])
        self.assertEqual(prog1.lines[20], b'\x02')

    def test_add_encoded_line(self):
        prog = BASICFile(None)
        prog.add_encoded_line(10, b'\x00')
        prog.add_encoded_line(100, b'\x00')
        prog.add_encoded_line(50, b'\x00')
        self.assertEqual(list(prog.lines.keys()), [10, 50, 100])

    def test_add_line(self):
        prog = BASICFile(None)
        prog.add_line(50, 'PRINT')
        self.assertEqual(prog.lines[50], b'\x99')

    def test_delete_line(self):
        prog = BASICFile(None)
        prog.add_encoded_line(10, b'\x00')
        prog.add_encoded_line(50, b'\x00')
        prog.add_encoded_line(100, b'\x00')
        prog.delete_line(50)
        self.assertEqual(list(prog.lines.keys()), [10, 100])

    def test_escape_set_name(self):
        self.assertEqual(BASICFile.escape_set_name('petscii-vic20en-uc'), 'escape-vic20')
        self.assertEqual(BASICFile.escape_set_name('dummy'), 'escape-c64')

    def test_tokenize(self):
        prog = BASICFile(None)
        self.assertEqual(prog.tokenize('GO TO'), b'\xcb \xa4')
        self.assertEqual(prog.tokenize('INPUTA'), b'\x85A')
        self.assertEqual(prog.tokenize('INPUT#2'), b'\x842')
        self.assertEqual(prog.tokenize('GOSU:'), b'\xcbSU:')
        self.assertEqual(prog.tokenize('WAND128'), b'W\xaf128')
        self.assertEqual(prog.tokenize('A=RND(1)'), b'A\xb2\xbb(1)')
        self.assertEqual(prog.tokenize('3↑2'), b'3\xae2')
        self.assertEqual(prog.tokenize('3^2'), b'3\xae2')
        self.assertEqual(prog.tokenize('REM SHORT'), b'\x8f SHORT')
        self.assertEqual(prog.tokenize('DATA ":",STOP:STOP'), b'\x83 ":",STOP:\x90')
        self.assertEqual(prog.tokenize('REM STOP:STOP'), b'\x8f STOP:STOP')
        self.assertEqual(prog.tokenize('REM "{blu}"'), b'\x8f "\x1f"')
        self.assertEqual(prog.tokenize('PRINT"{lgrn}"'), b'\x99"\x99"')
        self.assertEqual(prog.tokenize('PRINT"~2a~ff"'), b'\x99"*\xff"')
        self.assertEqual(prog.tokenize('~99"*"'), b'\x99"*"')
        self.assertEqual(prog.tokenize('?"*"'), b'\x99"*"')

    def test_expand(self):
        prog = BASICFile(None)
        self.assertEqual(prog.expand(b'A\xb2\xbb(1)'), 'A=RND(1)')
        self.assertEqual(prog.expand(b'\x99"\x09"'), 'PRINT"{ensh}"')
        self.assertEqual(prog.expand(b'W\xb2\xb5(3\xaeW)'), 'W=INT(3↑W)')

    def test_renumber(self):
        prog1 = BASICFile(None)
        prog1.add_line(10, 'GOTO20')
        prog1.add_line(20, 'REM LINE 2')
        prog1.add_line(30, 'GOTO20')

        prog2 = prog1.renumber(100, 5)
        self.assertEqual(list(prog2.lines.keys()), [100, 105, 110])
        self.assertEqual(prog2.lines[100], b'\x89105')
        self.assertEqual(prog2.lines[110], b'\x89105')

        prog2 = prog1.renumber(100, 5, range_start=20)
        self.assertEqual(list(prog2.lines.keys()), [10, 100, 105])
        self.assertEqual(prog2.lines[10], b'\x89100')
        self.assertEqual(prog2.lines[105], b'\x89100')

        with self.assertRaises(ValueError):
            _ = prog1.renumber(5, 5, range_start=20)

def test_invalid_format(self):
        mock_file = io.BytesIO(b'\x01'*8)
        with self.assertRaises(ValueError):
            _ = BASICFile(mock_file)
