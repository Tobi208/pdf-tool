import unittest
from pdftool import parse_args as pa
from pdftool import verify_file, get_range


class TestPDFTool(unittest.TestCase):

    def test_verify_file(self):
        """
        Test verify_file with actual files
        """
        self.assertFalse(verify_file('notafile.pdf'), 'file does not exist')
        self.assertTrue(verify_file('file1.pdf'), 'file exists')

    def test_get_range(self):
        """
        Test get_range
        """
        with self.assertRaises(ValueError):
            get_range('notanumber')
            get_range('1-notanumber')
            get_range('notanumber-1')
            get_range('1#2')
            get_range('2-1')
            get_range('-1-2')
            get_range('0.5-1')
            get_range('1--2')
            get_range('0-2')
        self.assertEqual(get_range('1-1'), range(0, 1), 'i = j')
        self.assertEqual(get_range('1-2'), range(0, 2), 'j = i + 1')
        self.assertEqual(get_range('100-200'), range(99, 200), 'i = 99, j = 199')

    def test_pa(self):
        """
        General parse_args test for first two arguments
        """
        self.assertFalse(pa([]), 'empty arguements')
        self.assertFalse(pa(['file1.pdf']), 'missing action')
        self.assertFalse(pa(['split']), 'missing file')
        self.assertFalse(pa(['explode', 'file1.pdf']), 'invalid action')
        self.assertFalse(pa(['split', 'noafile.pdf']), 'invalid file')

    def test_pa_delete_extract_split(self):
        """
        Test input for delete, extract, split
        General parse_args, verify_file and get_range related tests not covered here
        """
        self.assertFalse(pa(['delete', 'file1.pdf']), 'missing range')
        self.assertFalse(pa(['extract', 'file2.pdf']), 'missing range')
        self.assertFalse(pa(['split', 'file3.pdf']), 'missing range')
        self.assertFalse(pa(['delete', 'notafile.pdf', '1']), 'invalid file')
        self.assertFalse(pa(['extract', 'notafile.pdf', '1']), 'invalid file')
        self.assertFalse(pa(['split', 'notafile.pdf', '1']), 'invalid file')
        self.assertEqual(pa(['delete', 'file1.pdf', '5']), ('file1.pdf', [range(4, 5)]))
        self.assertEqual(pa(['extract', 'file1.pdf', '1-5']), ('file1.pdf', [range(0, 5)]))
        self.assertEqual(pa(['split', 'file1.pdf', '1-5', '10']), ('file1.pdf', [range(0, 5), range(9, 10)]))

    def test_pa_insert(self):
        """
        Test input for insert
        General parse_args, verify_file and get_range related tests not covered here
        """
        self.assertFalse(pa(['insert', 'file1.pdf']), 'missing file')
        self.assertFalse(pa(['insert', 'file1.pdf', 'file2.pdf']), 'missing pos')
        self.assertFalse(pa(['insert', 'file1.pdf', 'file2.pdf', '1-5']), 'missing pos')
        self.assertFalse(pa(['insert', 'file1.pdf', 'file2.pdf', 'file3.pdf']), 'missing pos')
        self.assertFalse(pa(['insert', 'file1.pdf', 'file2.pdf', '2', 'file3.pdf']), 'missing pos')
        self.assertFalse(pa(['insert', 'file1.pdf', 'file2.pdf', '2', '5-10', 'file3.pdf']), 'missing pos')
        self.assertFalse(pa(['insert', 'file1.pdf', 'file2.pdf', '2', '5-10', 'file3.pdf', '3-6']), 'missing pos')
        self.assertFalse(pa(['insert', 'file1.pdf', 'file2.pdf', '5-10', '2']), 'pos is range > 1')
        self.assertFalse(pa(['insert', 'file1.pdf', '1', 'file2.pdf']), 'pos instead of file')
        self.assertFalse(pa(['insert', 'file1.pdf', 'file2.pdf', '1', '2', '3']), 'too many pos')
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '1']),
                         ('file1.pdf', [['file2.pdf', range(0, 1)]]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '1', '5']),
                         ('file1.pdf', [['file2.pdf', range(0, 1), range(4, 5)]]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', '1-5']),
                         ('file1.pdf', [['file2.pdf', range(9, 10), range(0, 5)]]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', 'file2.pdf', '3']),
                         ('file1.pdf', [['file2.pdf', range(9, 10)],
                                        ['file2.pdf', range(2, 3)]]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', '1-5', 'file2.pdf', '3']),
                         ('file1.pdf', [['file2.pdf', range(9, 10), range(0, 5)],
                                        ['file2.pdf', range(2, 3)]]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', '1-5', 'file2.pdf', '3', '10-15']),
                         ('file1.pdf', [['file2.pdf', range(9, 10), range(0, 5)],
                                        ['file2.pdf', range(2, 3), range(9, 15)]]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', 'file2.pdf', '3', '10-15']),
                         ('file1.pdf', [['file2.pdf', range(9, 10)],
                                        ['file2.pdf', range(2, 3), range(9, 15)]]))

    def test_pa_merge(self):
        """
        Test input for merge
        """
        pass

    def test_pa_purge(self):
        """
        Test input for purge
        """
        pass


if __name__ == '__main__':
    unittest.main()