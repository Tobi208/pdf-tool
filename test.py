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
        """
        pass

    def test_pa_insert(self):
        """
        Test input for insert
        """
        pass

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