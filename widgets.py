import urwid

class Text(urwid.WidgetWrap):
    def parse_match(self, m_iter):
        pass

    def is_empty(self):
        return self.widget is None or len(self.get_text()) <= 0

    def get_text(self):
        return self.widget.get_text()

    def set_text(self, markup):
        self.widget.set_text(markup)

    def rows(self, size, focus=False):
        if self.is_empty():
            return 0
        return self.widget.rows(size, focus)

class SearchText(Text):
    def __init__(self, m_iter):
        self.widget = None
        self.parse_match(m_iter)
        urwid.WidgetWrap.__init__(self, self.widget)

    def parse_match(self, m_iter):
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
            self.widget = urwid.Text(parts, wrap='clip')

class ReplaceText(Text):
    def __init__(self, pair, replacement, delim):
        self.widget = None
        self.parse_match(pair, replacement, delim)
        urwid.WidgetWrap.__init__(self, self.widget)

    def parse_match(self, pair, replacement, delim):
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
                parts.append(('match', replacement))
                ps = s
                pe = e
                s = file.find(delim[0], s + 1)
                e = file.find(delim[1], e + 1)

        if len(parts) > 0:
            if pe != len(file) and len(replacement) > 0:
                parts.append(file[pe:].replace(delim[1], ''))
            self.widget = urwid.Text(parts, wrap='clip')