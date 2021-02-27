# pdf-tool

Python Command Line Tool to Merge, Insert, Delete, Split, Extract or Purge redundant PDF Pages based on PyPDF2


# How to use


Commands allow selection of positions or ranges where applicable. A passed position marks the index at which the second file appears within the new file. A passed range works the same and is inclusive.


## Merge

Merge two or more files, or a selection of pages from two or more files

``-m`` or ``--merge``

``py pdftool.py -m file1 file2 file3 ...``
``py pdftool.py -m file1 a-b file2 c file3 d-e ...``


## Insert

Insert a file, or a selection of pages at a specific position in a different file

``-i`` or ``--insert``

``py pdftool.py -i file1 pos file2``
``py pdftool.py -i file1 pos file2 a-b``


## Delete

Delete a selection of pages from a file

``-d`` or ``--delete``

``py pdftool.py -d file1 a-b``


## Split

Split a file into multiple files

``-s`` or ``--split``

``py pdftool.py -s file1 a b c ...``


## Extract

Extract multiple selections of pages from a file

``-e`` or ``--extract``

``py pdftool.py -e file1 a-b c-d e-f ...``


## Purge

Rid the file of redundant incremental pages

``-p`` ``--purge``

``py pdftool.py -p file1 file2 file3 ...``