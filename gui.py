import urwid

from guihelper import FilePanel, SearchPanel, StatusBar

def exit(key):
    if key in ('esc', 'q'):
        raise urwid.ExitMainLoop()

PALETTE = [
    #('default', 'white', 'black'),
    ('match', 'dark red', 'black')
]

class GUI():
    def __init__(self, files):
        self.searchpanel = SearchPanel()
        self.filepanel = FilePanel(files)
        self.statusbar = StatusBar(files)

        frame = urwid.Frame(self.filepanel.get_widget()
                            , header=self.searchpanel.get_widget()
                            , footer=self.statusbar.get_widget()
                            , focus_part='header')
        self.loop = urwid.MainLoop(frame, PALETTE, unhandled_input=exit)

    def search(self, searchtext, file_filter):
        files = list(file_filter)
        matches = self.filepanel.search(searchtext, files)
        self.statusbar.search(matches)

    def show(self):
        self.loop.run()

    def register_search_listener(self, listener):
        urwid.connect_signal(self.searchpanel.search, 'change', listener)

    def register_replace_listener(self, listener):
        urwid.connect_signal(self.replace, 'change', listener)
