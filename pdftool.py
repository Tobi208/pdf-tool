import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter


def parse_args(args):

    if len(args) < 2:
        print('Missing <action> and/or <file1>!')
        return
    action = args[0]
    if action not in actions:
        print('Undefined <action>: ' + action + '!')
        return
    xs = args[1:]
    file1 = xs[0]
    if not verify_file(file1):
        return

    if action in ['delete', 'extract', 'split']:
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
        if len(xs) < 3:
            print('Missing files, indices or ranges!')
            return
        i = 1
        tss = []
        while i < len(xs):
            filei = xs[i]
            if not verify_file(filei):
                return
            ts = [filei]
            j = i + 1
            while not xs[j].endwith('.pdf'):
                try:
                    ts.append(get_range(xs[j]))
                except ValueError:
                    print('Expected format for indices or ranges: i or i-j!')
            if len(ts) not in [1, 2]:
                print('Too many or too little index or range arguments for: ' + filei + '!')
                return
            i = j
            tss.append(ts)
        return file1, tss

    if action == 'merge':
        if len(xs) < 2:
            print('Missing files!')
            return
        i = 0
        ts = []
        while i < len(xs):
            filei = xs[i]
            if not verify_file(filei):
                return
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
        if all(map(verify_file, xs)):
            return xs
        else:
            return


def verify_file(file):
    if not os.path.isfile(file):
        print('File not found: ' + file + '!')
        return False
    return True


def get_range(s: str):
    if '-' in s:
        x = s.split('-')
        if len(x) != 2:
            raise ValueError
        return range(int(x[0]) - 1, int(x[1]))
    else:
        return range(int(s) - 1, int(s))


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