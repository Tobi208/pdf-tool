import unittest
from pdftool import parse_args as pa
from pdftool import *


class TestPDFTool(unittest.TestCase):

    def test_verify_file(self):
        """
        Test verify_file with actual files
        """
        with self.assertRaises(FileNotFoundError):
            verify_file('notafile.pdf', set())
        with self.assertRaises(TypeError):
            verify_file('notapdf.docx', set())
        self.assertIsNone(verify_file('file1.pdf', set()), 'file exists')

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
        with self.assertRaises(TypeError):
            pa(['split', 'file1.pdf', '1', 1])
            pa(['split', 'file1.pdf', '1', True])
        with self.assertRaises(ValueError):
            pa([])
            pa(['file1.pdf'])
            pa(['split'])
        with self.assertRaises(KeyError):
            pa(['explode', 'file1.pdf'])
        with self.assertRaises(FileNotFoundError):
            pa(['split', 'notafile.pdf'])

    def test_pa_delete_extract_split(self):
        """
        Test input for delete, extract, split
        General parse_args, verify_file and get_range related tests not covered here
        """
        with self.assertRaises(ValueError):
            pa(['delete', 'file1.pdf'])
            pa(['extract', 'file2.pdf'])
            pa(['split', 'file3.pdf'])
            pa(['split', 'file2.pdf', 'file3.pdf'])
        self.assertEqual(pa(['delete', 'file1.pdf', '5']), ({'file1.pdf'}, 'file1.pdf', [range(4, 5)]))
        self.assertEqual(pa(['extract', 'file1.pdf', '1-5']), ({'file1.pdf'}, 'file1.pdf', [range(0, 5)]))
        self.assertEqual(pa(['split', 'file1.pdf', '1-5', '10']),
                         ({'file1.pdf'}, 'file1.pdf', [range(0, 5), range(9, 10)]))

    def test_pa_insert(self):
        """
        Test input for insert
        General parse_args, verify_file and get_range related tests not covered here
        """
        with self.assertRaises(ValueError):
            pa(['insert', 'file1.pdf'])
            pa(['insert', 'file1.pdf', 'file2.pdf'])
            pa(['insert', 'file1.pdf', 'file2.pdf', '5', 'file3.pdf'])
            pa(['insert', 'file1.pdf', 'file2.pdf', 'file3.pdf'])
            pa(['insert', 'file1.pdf', 'file2.pdf', '2', 'file3.pdf'])
            pa(['insert', 'file1.pdf', 'file2.pdf', '2', '5-10', 'file3.pdf'])
        with self.assertRaises(TypeError):
            pa(['insert', 'file1.pdf', 'file2.pdf', '5', 'file3.pdf', '1-5'])
            pa(['insert', 'file1.pdf', 'file2.pdf', '2', '5-10', 'file3.pdf', '3-6'])
            pa(['insert', 'file1.pdf', 'file2.pdf', '5-10', '2'])
            pa(['insert', 'file1.pdf', '1', 'file2.pdf'])
            pa(['insert', 'file1.pdf', 'file2.pdf', '1', '2', '3'])
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '1']),
                         ({'file1.pdf', 'file2.pdf'}, 'file1.pdf', [('file2.pdf', 0, None)]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '1', '5']),
                         ({'file1.pdf', 'file2.pdf'}, 'file1.pdf', [('file2.pdf', 0, range(4, 5))]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', '1-5']),
                         ({'file1.pdf', 'file2.pdf'}, 'file1.pdf', [('file2.pdf', 9, range(0, 5))]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', 'file2.pdf', '3']),
                         ({'file1.pdf', 'file2.pdf'}, 'file1.pdf',
                          [('file2.pdf', 9, None), ('file2.pdf', 2, None)]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', '1-5', 'file2.pdf', '3']),
                         ({'file1.pdf', 'file2.pdf'}, 'file1.pdf',
                          [('file2.pdf', 9, range(0, 5)), ('file2.pdf', 2, None)]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', '1-5', 'file2.pdf', '3', '10-15']),
                         ({'file1.pdf', 'file2.pdf'}, 'file1.pdf',
                          [('file2.pdf', 9, range(0, 5)), ('file2.pdf', 2, range(9, 15))]))
        self.assertEqual(pa(['insert', 'file1.pdf', 'file2.pdf', '10', 'file2.pdf', '3', '10-15']),
                         ({'file1.pdf', 'file2.pdf'}, 'file1.pdf',
                          [('file2.pdf', 9, None), ('file2.pdf', 2, range(9, 15))]))

    def test_pa_merge(self):
        """
        Test input for merge
        General parse_args, verify_file and get_range related tests not covered here
        """
        with self.assertRaises(TypeError):
            pa(['merge', 'file1.pdf', '1', '2', 'file2.pdf'])

        self.assertEqual(pa(['merge', 'file1.pdf']),
                         ({'file1.pdf'}, [('file1.pdf', None)]))
        self.assertEqual(pa(['merge', 'file1.pdf', '2']),
                         ({'file1.pdf'}, [('file1.pdf', range(1, 2))]))
        self.assertEqual(pa(['merge', 'file1.pdf', '2-5']),
                         ({'file1.pdf'}, [('file1.pdf', range(1, 5))]))
        self.assertEqual(pa(['merge', 'file1.pdf', 'file2.pdf']),
                         ({'file1.pdf', 'file2.pdf'}, [('file1.pdf', None), ('file2.pdf', None)]))
        self.assertEqual(pa(['merge', 'file1.pdf', '5', 'file2.pdf']),
                         ({'file1.pdf', 'file2.pdf'}, [('file1.pdf', range(4, 5)), ('file2.pdf', None)]))
        self.assertEqual(pa(['merge', 'file1.pdf', 'file2.pdf', '10']),
                         ({'file1.pdf', 'file2.pdf'}, [('file1.pdf', None), ('file2.pdf', range(9, 10))]))
        self.assertEqual(pa(['merge', 'file1.pdf', '1-15', 'file2.pdf']),
                         ({'file1.pdf', 'file2.pdf'}, [('file1.pdf', range(0, 15)), ('file2.pdf', None)]))
        self.assertEqual(pa(['merge', 'file1.pdf', '1-15', 'file2.pdf', '100-200']),
                         ({'file1.pdf', 'file2.pdf'},
                          [('file1.pdf', range(0, 15)), ('file2.pdf', range(99, 200))]))
        self.assertEqual(pa(['merge', 'file1.pdf', 'file2.pdf', '100-200']),
                         ({'file1.pdf', 'file2.pdf'},
                          [('file1.pdf', None), ('file2.pdf', range(99, 200))]))

    def test_pa_purge(self):
        """
        Test input for purge
        General parse_args, verify_file and get_range related tests not covered here
        """
        with self.assertRaises(TypeError):
            pa(['purge', 'file1.pdf', '1'])
            pa(['purge', 'file1.pdf', '1', 'file2.pdf'])

        self.assertEqual(pa(['purge', 'file1.pdf']),
                         ({'file1.pdf'}, ['file1.pdf']))
        self.assertEqual(pa(['purge', 'file1.pdf', 'file2.pdf']),
                         ({'file1.pdf', 'file2.pdf'}, ['file1.pdf', 'file2.pdf']))

    def test_delete(self):
        """
        Test file & range logic of delete
        """
        page_nums = {'file1.pdf': 16, 'file2.pdf': 32, 'file3.pdf': 1}
        self.assertEqual(delete(page_nums, 'file3.pdf', [range(0, 1)]),
                         [[('file3.pdf', [])]])
        self.assertEqual(delete(page_nums, 'file1.pdf', [range(0, 1)]),
                         [[('file1.pdf', list(range(1, 16)))]])
        self.assertEqual(delete(page_nums, 'file1.pdf', [range(0, 15)]),
                         [[('file1.pdf', list(range(15, 16)))]])
        self.assertEqual(delete(page_nums, 'file1.pdf', [range(0, 1), range(15, 16)]),
                         [[('file1.pdf', list(range(1, 15)))]])
        self.assertEqual(delete(page_nums, 'file2.pdf', [range(0, 32, 2)]),
                         [[('file2.pdf', list(range(1, 32, 2)))]])
        self.assertEqual(delete(page_nums, 'file2.pdf', [range(0, 8), range(24, 32)]),
                         [[('file2.pdf', list(range(8, 24)))]])
        self.assertEqual(delete(page_nums, 'file2.pdf', [range(30, 31)]),
                         [[('file2.pdf', list(range(0, 30)) + [31])]])

    def test_extract(self):
        """
        Test file & range logic of extract
        """
        page_nums = {'file1.pdf': 16, 'file2.pdf': 32, 'file3.pdf': 1}
        self.assertEqual(extract(page_nums, 'file3.pdf', [range(0, 1)]),
                         [[('file3.pdf', [0])]])
        self.assertEqual(extract(page_nums, 'file1.pdf', [range(0, 1)]),
                         [[('file1.pdf', [0])]])
        self.assertEqual(extract(page_nums, 'file1.pdf', [range(0, 15)]),
                         [[('file1.pdf', list(range(0, 15)))]])
        self.assertEqual(extract(page_nums, 'file1.pdf', [range(0, 1), range(15, 16)]),
                         [[('file1.pdf', [0, 15])]])
        self.assertEqual(extract(page_nums, 'file2.pdf', [range(0, 32, 2)]),
                         [[('file2.pdf', list(range(0, 32, 2)))]])
        self.assertEqual(extract(page_nums, 'file2.pdf', [range(0, 8), range(24, 32)]),
                         [[('file2.pdf', list(range(0, 8)) + list(range(24, 32)))]])
        self.assertEqual(extract(page_nums, 'file2.pdf', [range(30, 31)]),
                         [[('file2.pdf', [30])]])

    def test_insert(self):
        """
        Test file & range logic of insert
        """
        page_nums = {'file1.pdf': 16, 'file2.pdf': 32, 'file3.pdf': 1}
        self.assertEqual(insert(page_nums, 'file1.pdf', [('file3.pdf', 8, None)]),
                         [[('file1.pdf', list(range(8))),
                           ('file3.pdf', [0]),
                           ('file1.pdf', list(range(8, 16)))]])
        self.assertEqual(insert(page_nums, 'file1.pdf', [('file3.pdf', 8, range(0, 1))]),
                         [[('file1.pdf', list(range(8))),
                           ('file3.pdf', [0]),
                           ('file1.pdf', list(range(8, 16)))]])
        self.assertEqual(insert(page_nums, 'file1.pdf',
                                [('file2.pdf', 5, range(16)),
                                 ('file2.pdf', 10, range(16, 32))]),
                         [[('file1.pdf', list(range(5))),
                           ('file2.pdf', list(range(16))),
                           ('file1.pdf', list(range(5, 10))),
                           ('file2.pdf', list(range(16, 32))),
                           ('file1.pdf', list(range(10, 16)))]])

    def test_merge(self):
        """
        Test file & range logic of merge
        """
        page_nums = {'file1.pdf': 16, 'file2.pdf': 32, 'file3.pdf': 1}
        self.assertEqual(merge(page_nums, [('file1.pdf', None)]),
                         [[('file1.pdf', list(range(16)))]])
        self.assertEqual(merge(page_nums, [('file1.pdf', range(0, 1))]),
                         [[('file1.pdf', [0])]])
        self.assertEqual(merge(page_nums, [('file1.pdf', range(0, 1)), ('file1.pdf', range(1, 2))]),
                         [[('file1.pdf', [0]), ('file1.pdf', [1])]])
        self.assertEqual(merge(page_nums, [('file1.pdf', range(2)), ('file1.pdf', range(2, 4))]),
                         [[('file1.pdf', [0, 1]), ('file1.pdf', [2, 3])]])
        self.assertEqual(merge(page_nums, [('file1.pdf', None), ('file2.pdf', None)]),
                         [[('file1.pdf', list(range(16))), ('file2.pdf', list(range(32)))]])
        self.assertEqual(merge(page_nums, [('file1.pdf', range(14)), ('file2.pdf', None)]),
                         [[('file1.pdf', list(range(14))), ('file2.pdf', list(range(32)))]])
        self.assertEqual(merge(page_nums, [('file1.pdf', None), ('file2.pdf', range(16))]),
                         [[('file1.pdf', list(range(16))), ('file2.pdf', list(range(16)))]])
        self.assertEqual(merge(page_nums, [('file1.pdf', range(14)), ('file2.pdf', range(16))]),
                         [[('file1.pdf', list(range(14))), ('file2.pdf', list(range(16)))]])
        self.assertEqual(merge(page_nums, [('file1.pdf', range(7, 14)), ('file2.pdf', range(5, 16))]),
                         [[('file1.pdf', list(range(7, 14))), ('file2.pdf', list(range(5, 16)))]])

    def test_split(self):
        """
        Test file & range logic for split
        """
        page_nums = {'file1.pdf': 16}
        self.assertEqual(split(page_nums, 'file1.pdf', [range(8, 9)]),
                         [[('file1.pdf', list(range(0, 8)))], [('file1.pdf', list(range(8, 16)))]])
        self.assertEqual(split(page_nums, 'file1.pdf', [range(5, 6), range(10, 11)]),
                         [[('file1.pdf', list(range(0, 5)))],
                          [('file1.pdf', list(range(5, 10)))],
                          [('file1.pdf', list(range(10, 16)))]])
        self.assertEqual(split(page_nums, 'file1.pdf', [range(5, 10)]),
                         [[('file1.pdf', list(range(0, 5)))],
                          [('file1.pdf', list(range(5, 6)))],
                          [('file1.pdf', list(range(6, 7)))],
                          [('file1.pdf', list(range(7, 8)))],
                          [('file1.pdf', list(range(8, 9)))],
                          [('file1.pdf', list(range(9, 16)))]])

    def test_assemble(self):
        """
        Test file assembly from instructions
        """
        all_instructions = [
            [('file1.pdf', [0, 1, 2]), ('file2.pdf', [3, 4, 5])],
            [('file3.pdf', [11, 10, 9]), ('file2.pdf', [2, 1, 0])]
        ]
        filereaders = get_filereaders({'file1.pdf', 'file2.pdf', 'file3.pdf'})

        # assemble(filereaders, all_instructions)


if __name__ == '__main__':
    unittest.main()
