import re, flags

username_regex = re.compile("/\A([a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]{2,15})\z/i")

class User():
    GUID = -1
    hostmask = ""
    
    nick = ""
    ident = ""
    hostname = ""
    
    flags = None
    
    _socket = None
    def __init__(self, socket, nick, ident, hostname):
        self._socket = socket
        self.nick = nick
        self.ident = ident
        self.hostname = hostname
        self.hostmask = "%s!%s@%s" % (nick, ident, hostname)
    def send(self, data):
        if self._socket:
            self._socket.send("%s\r\n" % data)
    