import urwid

class SearchPanel():
    def __init__(self):
        self.search = urwid.Edit(caption='Search: ')
        self.replace = urwid.Edit(caption='Replace: ')

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
        self.previewlist = urwid.SimpleFocusListWalker(textboxes)

    def get_widget(self):
        matchlist = urwid.ListBox(self.filelist)
        matchborder = urwid.LineBox(matchlist)

        previewlist = urwid.ListBox(self.previewlist)
        previewborder = urwid.LineBox(previewlist)

        return urwid.Columns([matchborder, previewborder])

    def search(self, searchtext, matches):
        textboxes = []
        del self.filelist[:]
        del self.previewlist[:]

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
        self.previewlist.extend(textboxes)
        return len(self.filelist)

    def replace(self, replacement, files):
        # TODO: Colorize replacement part
        del self.previewlist[:]
        textboxes = []
        for file in files:
            parts = []
            s = file.find("$MATCH$")
            e = file.find("$END$")
            ps = pe = 0
            while s >= 0:
                if s > 0:
                    parts.append(file[pe:s].replace('$MATCH$', '').replace('$END$', ''))
                parts.append(('match', file[s:e].replace('$MATCH$', '').replace('$END$', '')))
                ps = s
                pe = e
                s = file.find("$MATCH$", s + 1)
                e = file.find("$END$", e + 1)

            if len(parts) > 0:
                if pe != len(file):
                    parts.append(file[pe:].replace('$MATCH$', '').replace('$END$', ''))
                txt = urwid.Text(parts, wrap='clip')
                if len(txt.get_text()) > 0:
                    textboxes.append(txt)

        self.previewlist.extend(textboxes)
        #self.previewlist.extend([urwid.Text(f, wrap='clip') for f in files])

