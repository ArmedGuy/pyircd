class User:
    GUID = -1
    nick = ""
    ident = ""
    hostname = ""
    flags = None
    _socket = None
    def __init__(self, socket):
        self._socket = socket
    def send(self, data):
        if self._socket:
            self._socket.write("%s\r\n" % data)
    