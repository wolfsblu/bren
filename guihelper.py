import urwid

class SearchPanel():
    def __init__(self):
        self.search = urwid.Edit(caption='Search: ')
        self.replace = urwid.Edit(caption='Replace: ')
        self.search = urwid.Edit(caption='Search: ')

    def get_widget(self):
        cols = urwid.Columns([urwid.LineBox(self.search),
                              urwid.LineBox(self.replace)])
        return urwid.Pile([cols])

class StatusBar():
    def __init__(self, files):
        self.file_count = len(files)
        self.count_widget = urwid.Text("{0}/{0} files".format(self.file_count))

    def get_widget(self):
        return urwid.Padding(self.count_widget, left=1)

    def update_files(self, files):
        self.count_widget.set_text("{}/{} files".format(len(files), self.file_count))

class FilePanel():
    def __init__(self, files):
        textboxes = [urwid.Text(f, wrap='clip') for f in files]
        self.filelist = urwid.SimpleFocusListWalker(textboxes)

    def get_widget(self):
        matchlist = urwid.ListBox(self.filelist)
        matchborder = urwid.LineBox(matchlist)

        # TODO: Use preview file name list
        previewlist = urwid.ListBox(self.filelist)
        previewborder = urwid.LineBox(previewlist)

        return urwid.Columns([matchborder, previewborder])

    def update_files(self, files):
        del self.filelist[:]
        textboxes = [urwid.Text(f, wrap='clip') for f in files]
        self.filelist.extend(textboxes)

