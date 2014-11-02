import cStringIO

class Output:
    def __init__(self, colored=True):
        self._colored = colored
        self._requires_sep = False
        self._buffer = cStringIO.StringIO()

    def add_separator(self):
        if self._requires_sep == False:
            return
        self._buffer.write('\n')
        self._requires_sep = False

    def add(self, text):
        self._buffer.write(text)
        self._requires_sep = True

    def add_line(self, text):
        self._buffer.write(text)
        self._buffer.write('\n')
        self._requires_sep = True

    def value(self):
        return self._buffer.getvalue()

    def add_error(self, text):
        self._buffer.write('ERROR: ')
        self.add_line(text)
