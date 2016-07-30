class Response:
    def __init__(self, request):
        self.raw = request.response
        self._header, self.body = self.raw.split(b'\r\n\r\n')
        self.header = Header(self._header)
        del self._header
        self.content = self.body.decode('utf8') if self.body else ''


class Header:
    def __init__(self, header_info):
        fragments = header_info.decode('utf8').split('\r\n')
        self.server, \
        self.date, \
        self.content_type, \
        self.content_length, \
        self.connection = [seg.split(':')[1] for seg in fragments[1:]]
        self.protocol, self.status_code, self.status_human = fragments[0].split(' ')
        self.content_length = int(self.content_length)
        self.status_code = int(self.status_code)

    def __repr__(self):
        return self.status_human
