import re

from gui import GUI

class Renamer():
    def __init__(self, files):
        self.files = files
        self.ui = GUI(files)
        self.ui.register_search_listener(self.on_search_change)
        self.ui.show()

    def on_search_change(self, widget, new_text):
        try:
            regex = re.compile(new_text)
            self.ui.set_files(filter(regex.search, self.files))
        except re.error: return
