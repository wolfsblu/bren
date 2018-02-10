# Bren

Bren is an urwid-based **b**atch **ren**ame utility written in Python.

## Installation

```
pip install -r requirements.txt
```

## Usage

Bren takes a file path as positional argument and allows the file names listed in the
specified file to be renamed.

```
ls -1 . > files.txt
./bren.py files.txt
```

To avoid having to generate this intermediate file it's possible to use process substitution.

```
./bren.py <(ls -1 .)
```
