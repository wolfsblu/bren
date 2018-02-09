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

    def search(self, matches):
        self.count_widget.set_text("{}/{} files".format(matches, self.file_count))

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

    def search(self, searchtext, matches):
        del self.filelist[:]
        textboxes = []
        if len(searchtext) == 0:
            for m_iter in matches:
                textboxes.append(urwid.Text(next(m_iter).string, wrap='clip'))
        else:
            for m_iter in matches:
                parts = []
                string = ''
                prev_start = prev_end = 0
                for m in m_iter:
                    string = m.string
                    if m.start() > prev_end:
                        parts.append(m.string[prev_end:m.start()])
                    prev_end = m.end()
                    prev_start = m.start()
                    parts.append(('match', m.group(0)))

                if len(parts) > 0:
                    if prev_end != len(string):
                        parts.append(string[prev_end:])

                    txt = urwid.Text(parts, wrap='clip')
                    if len(txt.get_text()) > 0:
                        textboxes.append(txt)

        self.filelist.extend(textboxes)
        return len(self.filelist)

