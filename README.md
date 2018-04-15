# Bren

Bren is an urwid-based **b**atch **ren**ame utility written in Python.

## Installation

```
virtualenv .env
. .env/bin/activate[.fish]
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
# Bash
./bren.py <(ls -1 .)

# Fish
./bren.py (ls -1 | psub)
```

## Screenshot

![Screenshot](https://github.com/helmi77/bren/blob/master/screenshots/bren.png "Screenshot")
