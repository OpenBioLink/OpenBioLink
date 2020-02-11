import io


class TqdmBuffer(io.StringIO):
    foo = ""
    buf = ""

    def __init__(self):
        super(TqdmBuffer, self).__init__()

    def write(self, buf):
        TqdmBuffer.foo = buf.strip("\r\n\t ")

    def flush(self):
        TqdmBuffer.buf = TqdmBuffer.foo
