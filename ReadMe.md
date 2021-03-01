# pdf-tool

Python Command Line Tool to Merge, Insert, Delete, Split, Extract or Purge redundant PDF Pages based on PyPDF2


# How to use


Commands allow selection of positions or ranges where applicable. A passed position marks the index at which the second file appears within the new file. A passed range works the same and is inclusive.


## Delete

Delete a selection of pages from a file

``py pdftool.py delete file1 a-b``


## Extract

Extract multiple selections of pages from a file

``py pdftool.py extract file1 a-b c-d e-f ...``


## Insert

Insert a file, or a selection of pages at a specific position in a different file

``py pdftool.py insert file1 file2 pos``
``py pdftool.py insert file1 file2 pos a-b file3 pos c-d ...``


## Merge

Merge two or more files, or a selection of pages from two or more files

``py pdftool.py merge file1 file2 file3 ...``
``py pdftool.py merge file1 a-b file2 c file3 d-e ...``


## Purge

Rid the file of redundant incremental pages

``py pdftool.py purge file1 file2 file3 ...``


## Split

Split a file into multiple files

``py pdftool.py split file1 a b c ...``


