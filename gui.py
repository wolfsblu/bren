import urwid

from guihelper import FilePanel, SearchPanel, StatusBar

def exit(key):
    if key in ('esc', 'q'):
        raise urwid.ExitMainLoop()

class GUI():
    def __init__(self, files):
        self.searchpanel = SearchPanel()
        self.filepanel = FilePanel(files)
        self.statusbar = StatusBar(files)

        frame = urwid.Frame(self.filepanel.get_widget()
                            , header=self.searchpanel.get_widget()
                            , footer=self.statusbar.get_widget()
                            , focus_part='header')
        self.loop = urwid.MainLoop(frame, unhandled_input=exit)

    def set_files(self, file_filter):
        files = list(file_filter)
        self.filepanel.update_files(files)
        self.statusbar.update_files(files)

    def show(self):
        self.loop.run()

    def register_search_listener(self, listener):
        urwid.connect_signal(self.searchpanel.search, 'change', listener)

    def register_replace_listener(self, listener):
        urwid.connect_signal(self.replace, 'change', listener)
