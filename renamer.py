import re

from gui import GUI

class Renamer():
    def __init__(self, files, ui):
        self.ui = ui
        self.files = files

    def on_search_change(self, widget, new_text):
        try:
            regex = re.compile(new_text)
            self.ui.set_files(filter(regex.search, self.files))
        except re.error: return
