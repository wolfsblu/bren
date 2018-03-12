import re
import os

from gui import GUI

class Renamer():
    def __init__(self, files, ui):
        self.ui = ui
        self.files = files
        self.matches = self.replaced = []
        self.delimiters = ("$MATCH$", "$END$")
        self.searchterm = self.replaceterm = ''
        self.searchregex = self.replaceregex = None

    def confirm(self):
        files = []
        for pair in self.replaced:
            original = pair[0]
            newname = pair[1].replace(self.delimiters[0], '').replace(self.delimiters[1], '')
            os.rename(original, newname)
            files.append(newname)
        self.files = files
        self.replaceregex = ''
        self.searchregex = re.compile('')
        self.matches = [m for f in self.files for m in [self.searchregex.finditer(f)] if m]
        self.replaced = [(f, self.searchregex.sub(self.replaceregex, f)) for f in self.files if self.searchregex.search(f)]
        self.ui.search(self.searchterm, self.matches)
        self.ui.replace(self.replaceterm, self.delimiters, self.replaced)

    def on_search_change(self, widget, search):
        self.searchterm = search
        try:
            self.searchregex = re.compile(search)
        except re.error: return
        self.matches = [m for f in self.files for m in [self.searchregex.finditer(f)] if m]
        self.ui.search(search, self.matches)

    def on_replace_change(self, widget, replacement):
        self.replaceterm = replacement
        try:
            self.replaceregex = "{}{}{}".format(self.delimiters[0]
                                                , bytes(replacement, 'utf-8').decode('unicode_escape')
                                                , self.delimiters[1])
            self.replaced = [(f, self.searchregex.sub(self.replaceregex, f)) for f in self.files if self.searchregex.search(f)]
            self.ui.replace(replacement, self.delimiters, self.replaced)
        except (re.error, UnicodeDecodeError): return
