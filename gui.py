import urwid

from guihelper import FilePanel, SearchPanel, StatusBar

def exit(key):
    if key in ('esc', 'q'):
        raise urwid.ExitMainLoop()

PALETTE = [
    ('match', 'dark red', 'black')
]

class GUI():
    def __init__(self, files):
        self.searchpanel = SearchPanel()
        self.filepanel = FilePanel(files)
        self.statusbar = StatusBar(files)

        frame = urwid.Pile([('pack', self.searchpanel.get_widget())
                            , self.filepanel.get_widget()
                            , ('pack', self.statusbar.get_widget())])
        self.loop = urwid.MainLoop(frame, PALETTE, unhandled_input=exit)

    def search(self, searchtext, files):
        matches = self.filepanel.search(searchtext, files)
        self.statusbar.search(matches)

    def replace(self, replacement, files):
        self.filepanel.replace(replacement, files)

    def show(self):
        self.loop.run()

    def register_search_listener(self, listener):
        urwid.connect_signal(self.searchpanel.search, 'change', listener)

    def register_replace_listener(self, listener):
        urwid.connect_signal(self.searchpanel.replace, 'change', listener)
