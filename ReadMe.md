# pdf-tool

Python Command Line Tool to Merge, Insert, Delete, Split, Extract or Purge redundant PDF Pages based on PyPDF2.


# Command Line Tool


Commands allow selection of positions or ranges where applicable.
A passed position marks the index at which the second file appears within the new file.
A passed range works the same and is inclusive.
Indices start at 1 and go up to the number of pages.


## Delete

Delete a selection of pages from a file.
The new file contains all pages, that **are not** at any specified index or in any range.
Only accepts a single file and its indices/ranges to be deleted.
Inverse to **Extract**.

``py pdftool.py delete file1 i``

``py pdftool.py delete file1 i j``

``py pdftool.py delete file1 a-b``

``py pdftool.py delete file1 i a-b j c-d``


## Extract

Extract multiple selections of pages from a file.
The new files contains all pages, that **are** at any specified index or in any range.
Only accepts a single file and its indices/ranges to be extracted.
Inverse to **Delete**.

``py pdftool.py extract file1 i``

``py pdftool.py extract file1 i j``

``py pdftool.py extract file1 a-b``

``py pdftool.py extract file1 i a-b j c-d``


## Insert

Insert files, or selections of pages at a specific position in a file.
The new file contains all pages of file1 and is expanded with pages from other files at specific positions.
Accepts a main file and then at least one file + position (+ range) argument.
The range refers to which pages of the other file are to be inserted and is optional.
If it is not specified, all pages will be inserted.
Pages that are specified to be inserted at the same index will be inserted in the order they were specified.


``py pdftool.py insert file1 file2 i``

``py pdftool.py insert file1 file2 i a-b``

``py pdftool.py insert file1 file2 i file3 j c-d``

``py pdftool.py insert file1 file2 i a-b file3 j c-d``

## Merge

Merge files, or a selection of pages of files.
The new file contains pages from all specified files, or their specified indices/ranges, in the order they are passed.
Accepts at least one file (+ index/range) argument.
Specifying the index/range of pages to be merged is optional.
By default, all pages will be merged.
Inverse to **Split**.

``py pdftool.py merge file1 i file2 c-d``

``py pdftool.py merge file1 file2 file3``

``py pdftool.py merge file1 i file2 j file3 k``

``py pdftool.py merge file1 a-b file2 i file3 e-f ...``


## Purge

**This feature is not available yet.**

Rid each file of redundant incremental pages.
If your professor likes to export their presentation one page per line of text revealed, this is the tool you are looking for.
Pages that are incomplete versions of their subsequent pages are removed.
Accepts at least one file as argument.

``py pdftool.py purge file1``

``py pdftool.py purge file1 file2 file3``


## Split

Split a file into multiple files at specified indices.
Each new file contains the pages from inclusively the previous index to exclusively the next index (unless it's the last index).
The first index is 1, and the last index is the number of pages.
Ranges are interpreted as multiple indices, so 1-4 == 1 2 3 4.
Accepts a main file and at least one index/range.
Inverse to **Merge**.

``py pdftool.py split file1 i``

``py pdftool.py split file1 i j``

``py pdftool.py split file1 a-b``

``py pdftool.py split file1 i a-b j c-d``


## More Examples

You only need the first two pages of a pdf:

``py pdftool.py extract file.pdf 1-2``

You want to merge all chapters of a lecture into a single file:

``py pdftool.py merge chapter1.pdf chapter2.pdf chapter3.pdf chapter4.pdf ...``

You need to hand in each of the 5 tasks of an assignment in a separate file:

``py pdftool.py split assignment.pdf 2 3 4``

You want to include your own notes in the lecuture pdf:

``py pdftool.py insert lecture.pdf notes1.pdf 5 notes2.pdf 7 1-4 notes3.pdf 10 ...``

## Some calls that yield equivalent results

Assuming all files have 10 pages

``extract file 1-2 <=> delete file 8-10``

``delete file 8-10 <=> merge file 1-2``

``extract file 1 2 3-6 7-10 <=> split file 2 3 7``

``merge file1 file2 5-8 <=> insert file1 file2 11 5-8``

``merge file <=> nothing``


# Python Module

``pdftool.py`` may also be used as a python module in other scripts.
The secure API is ``pdftool.execute()``.
Other functions may not verify your input and yield unwanted results, use them at your own discretion.
Call ``execute()`` as if you were calling the tool from the command line, but without ``py pdftool.py``:

``pdftool.execute('extract file.pdf 1-2') <=> py pdftool.py extract file.pdf 1-2``

# Future Features

- implement purge
- append? almost equal to merge
- specify output file names