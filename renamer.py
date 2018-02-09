import re

from gui import GUI

class Renamer():
    def __init__(self, files, ui):
        self.ui = ui
        self.files = files
        self.matches = []

    def on_search_change(self, widget, new_text):
        try:
            regex = re.compile(new_text)
            self.matches = [m for f in self.files for m in [regex.finditer(f)] if m]
            self.ui.search(new_text, self.matches)
        except re.error: return

    def on_replace_change(self, widget, new_text):
        pass
