import urwid

from widgets import ReplaceText, SearchText

class SearchPanel():
    def __init__(self):
        self.search = urwid.Edit(caption='Replace: ')
        self.replace = urwid.Edit(caption='With: ')

    def get_widget(self):
        cols = urwid.Columns([urwid.LineBox(self.search),
                              urwid.LineBox(self.replace)])
        return urwid.Pile([cols])

    def reset(self):
        self.search.set_edit_text('')
        self.replace.set_edit_text('')

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
                st = SearchText([next(m_iter)])
                textboxes.append(st)
        else:
            for m_iter in matches:
                st = SearchText(m_iter)
                if not st.is_empty():
                    textboxes.append(st)

        self.filelist.extend(textboxes)
        self.previewlist.extend(textboxes)
        return len(self.filelist)

    def replace(self, replacement, delim, replaced):
        del self.previewlist[:]
        textboxes = []
        for pair in replaced:
            rt = ReplaceText(pair, replacement, delim)
            if not rt.is_empty():
                textboxes.append(rt)

        self.previewlist.extend(textboxes)
