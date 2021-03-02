import unittest
from pdftool import parse_args as pa


class TestPDFTool(unittest.TestCase):

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