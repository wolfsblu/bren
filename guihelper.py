import urwid

class SearchPanel():
    def __init__(self):
        self.search = urwid.Edit(caption='Replace: ')
        self.replace = urwid.Edit(caption='With: ')

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

    # TODO: Refactor search and replace
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

    def replace(self, replacement, delim, replaced):
        del self.previewlist[:]
        textboxes = []
        for pair in replaced:
            parts = []
            file = pair[1]
            s = file.find(delim[0])
            e = file.find(delim[1])
            ps = pe = 0
            if len(replacement) == 0:
                parts = [file.replace(delim[0], '').replace(delim[1], '')]
            else:
                while s >= 0:
                    if s > 0:
                        parts.append(file[pe:s].replace(delim[1], ''))
                    parts.append(('match', file[s:e].replace(delim[0], '')))
                    ps = s
                    pe = e
                    s = file.find(delim[0], s + 1)
                    e = file.find(delim[1], e + 1)

            if len(parts) > 0:
                if pe != len(file) and len(replacement) > 0:
                    parts.append(file[pe:].replace(delim[1], ''))
                txt = urwid.Text(parts, wrap='clip')
                if len(txt.get_text()) > 0:
                    textboxes.append(txt)

        self.previewlist.extend(textboxes)
