import urwid

def exit(key):
    if key in ('esc', 'q'):
        raise urwid.ExitMainLoop()

class GUI():
    def __init__(self, files):
        # TODO: Refactor widget initialization
        self.file_count = len(files)
        txt = [urwid.Text(f, wrap='clip') for f in files]

        self.left = urwid.SimpleFocusListWalker(txt)
        left_box = urwid.ListBox(self.left)

        self.search = urwid.Edit(caption='Search: ')
        self.replace = urwid.Edit(caption='Replace: ')
        txt_fields = urwid.Columns([urwid.LineBox(self.search), urwid.LineBox(self.replace)])
        header = urwid.Pile([txt_fields])
        self.footer = urwid.Text("{0}/{0} files".format(len(files)))

        cols = urwid.Columns([urwid.LineBox(left_box), urwid.LineBox(left_box)])
        frame = urwid.Frame(cols, header=header, footer=urwid.Padding(self.footer, left=1))
        self.loop = urwid.MainLoop(frame, unhandled_input=exit)

    def set_files(self, files):
        del self.left[:]
        filtered_count = 0
        for file in files:
            filtered_count += 1
            self.left.append(urwid.Text(file, wrap='clip'))

        self.footer.set_text("{}/{} files".format(filtered_count, self.file_count))

    def show(self):
        self.loop.run()

    def register_search_listener(self, listener):
        urwid.connect_signal(self.search, 'change', listener)

    def register_replace_listener(self, listener):
        urwid.connect_signal(self.replace, 'change', listener)
