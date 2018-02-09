import re

from gui import GUI

class Renamer():
    def __init__(self, files, ui):
        self.ui = ui
        self.files = files
        self.matches = self.replaced = []
        self.searchregex = self.replaceregex = None

    def on_search_change(self, widget, search):
        try:
            self.searchregex = re.compile(search)
        except re.error: return
        self.matches = [m for f in self.files for m in [self.searchregex.finditer(f)] if m]
        self.ui.search(search, self.matches)

    def on_replace_change(self, widget, replacement):
        try:
            # TODO: Allow backreferences
            self.replaceregex = "{}{}{}".format("$MATCH$", bytes(replacement, 'utf-8').decode('unicode_escape'), "$END$")
            self.replaced = [self.searchregex.sub(self.replaceregex, f) for f in self.files if self.searchregex.search(f)]
            self.ui.replace(replacement, self.replaced)
        except (re.error, UnicodeDecodeError): return
