import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter


def parse_args(args):
    """
    <action> <file1> <further mandatory and or optional args>

    Takes a list of user arguments and verifies them.
    If they pass, parses the arguments and prepares them for further use.

    :param args: user args as <action> <file1> and optional args
    :return: tuple of parsed arguments
    """
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
    # main file
    file1 = xs[0]
    if not verify_file(file1):
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
        return file1, rs

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
            if not verify_file(filei):
                return
            ts = [filei]
            # iterate once or twice further to get <i> or <i> <j-k>
            j = i + 1
            while not xs[j].endswith('.pdf'):
                try:
                    ts.append(get_range(xs[j]))
                except ValueError:
                    print('Expected format for indices or ranges: i or i-j!')
            if len(ts) not in [1, 2]:
                print('Too many or too little index or range arguments for: ' + filei + '!')
                return
            if len(ts[0]) > 1:
                print('File:' + filei + ' has to be followed by a single index!')
                return
            i = j
            tss.append(ts)
        return file1, tss

    if action == 'merge':
        """
        <action> <file1> <i> <file2> <j-k> <file3> etc.
        
        merge accepts at least two files and
        optionally which ranges of those files should be merged.
        Single pages <i> or ranges of pages <j-k>.
        """
        if len(xs) < 2 or (len(xs) == 2 and not verify_file(xs[1])):
            print('Missing files!')
            return
        i = 0
        # tuples of files and their ranges to be merged
        ts = []
        while i < len(xs):
            filei = xs[i]
            if not verify_file(filei):
                return
            # for each file exactly 1 index or range may be passed
            if not xs[i + 1].endswith('.pdf'):
                try:
                    ts.append((filei, get_range(xs[i + 1])))
                except ValueError:
                    print('Expected format for indices or ranges: i or i-j!')
                i += 2
            else:
                ts.append((filei, None))
                i += 1
        return ts

    if action == 'purge':
        """
        <action> <file1> <file2> <file3> etc.
        
        purge accepts a list of files
        """
        if all(map(verify_file, xs)):
            return xs
        else:
            return


def verify_file(file):
    """
    Checks if a file exists in the current folder

    :param file: file to be checked for existence
    :return: if file exists
    """
    if not os.path.isfile(file):
        print('File not found: ' + file + '!')
        return False
    return True


def get_range(s: str):
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


def delete():
    pass


def extract():
    pass


def insert():
    pass


def merge():
    pass


def purge():
    pass


def split():
    pass


actions = {'delete': delete,
           'extract': extract,
           'insert': insert,
           'merge': merge,
           'purge': purge,
           'split': split}

if __name__ == '__main__':
    pass