# pdf-tool

Python Command Line Tool to Merge, Insert, Delete, Split PDF Pages based on PyPDF2


# How to use


## Merge

Merge two or more files, or a selection of pages from two or more files

``-m`` or ``--merge``

``py pdftool.py -m file1 file2 file3 ...``
optional: select range of pages for some files
``py pdftool.py -m file1 a-b file2 c file3 d-e ...``


## Insert

Insert a file, or a selection of pages at a specific position in a different file

``-i`` or ``--insert``

``py pdftool.py -i file1 pos file2``
optional: select a range of paged to be inserted
``py pdftool.py -i file1 pos file2 a-b``


## Delete
