import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter


def parse_args(args: [str]):
    """
    <action> <file1> <further mandatory and or optional args>

    Takes a list of user arguments and verifies them.
    If they pass, parses the arguments and prepares them for further use.

    :param args: user args as <action> <file1> and optional args
    :return: tuple of parsed arguments
    """
    if not all(map(lambda s: type(s) == str, args)):
        print('List of strings required!')
        return
    # <action> <file1> are mandatory
    if len(args) < 2:
        print('Missing <action> and/or <file1>!')
        return
    action = args[0]
    if action not in actions:
        print('Undefined <action>: ' + action + '!')
        return
    # list of arguments after action
    xs = args[1:]
    # list of necessary files
    files = []
    # main file
    file1 = xs[0]
    if not verify_file(file1, files):
        return

    if action in ['delete', 'extract', 'split']:
        """
        <action> <file1> <i> <j-k> etc.
        
        delete, extract and split each accept a main file
        and then a list of indices or ranges
        of pages to be d/e/s, but at least 1.
        """
        if len(xs) < 2:
            print('Missing indices or ranges!')
            return
        try:
            rs = list(map(get_range, xs[1:]))
        except ValueError:
            print('Expected format for indices or ranges: i or i-j!')
            return
        return files, file1, rs

    if action == 'insert':
        """
        <action> <file1> <file2> <i> <j-k> <file2> <l> etc.
        
        insert accepts a main file and then a list of:
        file to be inserted into main file, index of main file to be inserted at,
        and optionally, which range of pages of file to be inserted.
        So each tuple - at least 1 - is length 2 or 3.
        """
        if len(xs) < 3:
            print('Missing files, indices or ranges!')
            return
        # skip main file
        i = 1
        # list of tuples
        tss = []
        while i < len(xs):
            # file marks start of a tuple
            filei = xs[i]
            if not verify_file(filei, files):
                return
            ts = [filei]
            # iterate once or twice further to get <i> or <i> <j-k>
            j = i + 1
            while j < len(xs) and not xs[j].endswith('.pdf'):
                try:
                    ts.append(get_range(xs[j]))
                except ValueError:
                    print('Expected format for indices or ranges: i or i-j!')
                j += 1
            if len(ts) not in [2, 3]:
                print('Too many or too little index or range arguments for: ' + filei + '!')
                return
            if len(ts[1]) > 1:
                print('File: ' + filei + ' has to be followed by a single index!')
                return
            i = j
            tss.append(ts)
        return files, file1, tss

    if action == 'merge':
        """
        <action> <file1> <i> <file2> <j-k> <file3> etc.
        
        merge accepts at least two files and
        optionally which ranges of those files should be merged.
        Single pages <i> or ranges of pages <j-k>.
        """
        if len(xs) < 2 or (len(xs) == 2 and not verify_file(xs[1], [])):
            print('Missing files!')
            return
        i = 0
        # tuples of files and their ranges to be merged
        ts = []
        while i < len(xs):
            filei = xs[i]
            if not verify_file(filei, files):
                return
            # for each file exactly 1 index or range may be passed
            if i < len(xs) - 1 and not xs[i + 1].endswith('.pdf'):
                try:
                    ts.append((filei, get_range(xs[i + 1])))
                except ValueError:
                    print('Expected format for indices or ranges: i or i-j!')
                i += 2
            else:
                ts.append((filei, None))
                i += 1
        return files, ts

    if action == 'purge':
        """
        <action> <file1> <file2> <file3> etc.
        
        purge accepts a list of files
        """
        if all(map(lambda x: verify_file(x, files), xs)):
            return files, xs
        else:
            print('Purge only accepts list of files')
            return


def verify_file(file: str, files: [str]) -> bool:
    """
    Checks if a file exists in the current folder and appends it to collection

    :param file: file to be checked for existence
    :param files: list of files file should be appended to if it exists
    :return: if file exists
    """
    if not os.path.isfile(file):
        print('File not found: ' + file + '!')
        return False
    files.append(file)
    return True


def get_range(s: str) -> range:
    """
    Parses a string containing a single number or
    two numbers connected with a dash to a range.
    Single numbers produce a range too.
    Range must span at least 1 index.

    ValueError is handled else where.

    :param s: string to be parsed
    :return: string parsed to range
    """
    if '-' in s:
        x = s.split('-')
        if len(x) != 2:
            raise ValueError
        i = int(x[0]) - 1
        j = int(x[1])
    else:
        i = int(s) - 1
        j = int(s)
    if i >= j or i < 0 or j < 1:
        raise ValueError
    return range(i, j)


def get_filereaders(fs: [str]) -> {str, PdfFileReader}:
    """
    Aquire a map of file names to corresponding file readers

    :param fs: list of files, may contain duplicates
    :return: map of file names to corresponding file readers
    """
    files = {}
    # can not use dict comprehension, because making identical readers is slow
    for f in fs:
        if f not in files:
            files[f] = PdfFileReader(open(f, 'br'))
    return files


def delete(page_nums: {str, int}, file1: str, rs: [range]) -> [[(str, [int])]]:
    """
    Compile assembly instructions for page deletion

    :param page_nums: dict of number of pages of all files
    :param file1: file to delete pages from
    :param rs: list of ranges of pages to be deleted
    :return: assembly instructions
    """
    total_range = range(page_nums[file1])
    del_ranges = [i for del_range in rs for i in del_range]
    retain = [i for i in total_range if i not in del_ranges]
    return [[(file1, retain)]]


def extract(page_nums: {str, int}, file1: str, rs: [range]) -> [[(str, [int])]]:
    """
    Compile assembly instructions for page extraction

    :param page_nums: dict of number of pages of all files
    :param file1: file to extract pages from
    :param rs: list of ranges of pages to be extracted
    :return: assembly instructions
    """
    total_range = range(page_nums[file1])
    ext_ranges = [i for ext_range in rs for i in ext_range]
    retain = [i for i in total_range if i in ext_ranges]
    return [[(file1, retain)]]


def insert(page_nums: {str, int}, file1: str, tss: [(str, int, range)]):
    """
    Compile assembly instructions for page insertions

    :param page_nums: dict of number of pages of all files
    :param file1: file to extract pages from
    :param tss: collection of files, their indices to be inserted at in file1 and which pages
    :return: assembly instructions
    """
    tss = [(file, i, list(r)) if r else (file, i, list(range(page_nums[file])))
           for (file, i, r) in tss]

    instructions = []
    j = 0
    for file, i, r in tss:
        instructions.append((file1, list(range(j, i))))
        instructions.append((file, r))
        j = i
    instructions.append((file1, list(range(j, page_nums[file1]))))

    return [instructions]


def merge(page_nums: {str, int}, ts: [(str, range)]) -> [[(str, [int])]]:
    """
    Compile assembly instructions for page merging

    :param page_nums: dict of number of pages of all files
    :param ts: collection of files and their ranges to be merged together
    :return: assembly instructions
    """
    return [[(file, list(r)) if r else (file, list(range(page_nums[file]))) for file, r in ts]]


def purge():
    pass


def split(page_nums: {str, int}, file1: str, rs: [range]) -> [[(str, [int])]]:
    """
    Compile assembly instructions for page splitting

    :param page_nums: dict of number of pages of all files
    :param file1: file to be split
    :param rs: list of ranges of pages to be split at
    :return: assembly instructions
    """
    total_len = page_nums[file1]
    total_range = range(total_len)
    spl_ranges = [i for spl_range in rs for i in spl_range]
    split_at = [i for i in total_range if i in spl_ranges]
    split_at.sort()

    # create new set of instructions for each split
    all_instructions = []
    j = 0
    for i in split_at:
        instruction = (file1, list(range(j, i)))
        all_instructions.append([instruction])
        j = i
    all_instructions.append([(file1, list(range(j, total_len)))])

    return all_instructions


def assemble(filereaders: {str, PdfFileReader}, all_instructions: [[(str, [int])]]):
    """
    Assemble all files given a list of instructions for each file

    :param filereaders: map of file names to opened file readers
    :param all_instructions: collection of instructions on how to assemble a file
    """
    for instructions in all_instructions:

        # find next free file name
        file_out = instructions[0][0][:-4] + '_out1.pdf'
        i = 2
        while os.path.isfile(file_out):
            file_out = file_out[:-5] + str(i) + '.pdf'
            i += 1

        writer = PdfFileWriter()

        # instruction = (file, [indices])
        for file, r in instructions:
            filereader = filereaders[file]
            # write pages
            for i in r:
                writer.addPage(filereader.getPage(i))

        with open(file_out, 'wb') as out:
            writer.write(out)


actions = {'delete': delete,
           'extract': extract,
           'insert': insert,
           'merge': merge,
           'purge': purge,
           'split': split}

if __name__ == '__main__':
    pass