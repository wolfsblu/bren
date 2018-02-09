import re

from gui import GUI

class Renamer():
    def __init__(self, files, ui):
        self.ui = ui
        self.files = files

    def on_search_change(self, widget, new_text):
        try:
            regex = re.compile(new_text)
            matches = [m for l in self.files for m in [regex.finditer(l)] if m]
            #self.ui.set_files(filter(regex.search, self.files))
            self.ui.set_files(new_text, matches)
        except re.error: return
