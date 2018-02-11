from setuptools import setup, find_packages

from codecs import open
from os import path

setup(
    name='bren',
    version='0.1.0',
    description='Bren is an urwid-based batch rename utility for the command line.',
    packages=find_packages(),
    install_requires=['urwid'],
    py_modules=['bren', 'gui', 'guihelper', 'renamer'],
    entry_points={
        'console_scripts': [
            'bren=bren:main',
        ],
    },
)
