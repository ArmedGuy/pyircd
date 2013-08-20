import re, flags, logger, config, irc.modes, threading
import network.commands.payloads, network.commands.replies, network.commands.events

username_regex = re.compile("/\A([a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]{2,15})\z/i")

class User():
    _userlock = None
    GUID = -1
    hostmask = ""
    
    nick = ""
    ident = ""
    hostname = ""
    real_hostname = ""

    realname = ""
    
    modes = None

    channels = None
    
    _socket = None
    _useBuffer = False
    _buffer = ""
    def __init__(self, socket, nick, ident, hostname):
        self._userlock = threading.Lock()

        self._socket = socket
        self.nick = nick
        self.ident = ident
        self.hostname = hostname
        self.hostmask = "%s!%s@%s" % (nick, ident, hostname)

        self.modes = irc.modes.UserModes(self)


        self.channels = [] # local channels = full object, global channels = network pointer

    def buffer(self, use):
        if use == False and self._useBuffer == True:
            if self._buffer != "":
                with self._userlock:
                    self._socket.send(self._buffer)
                    self._buffer = ""
        else:
            with self._userlock:
                self._buffer = ""
        self._useBuffer = use

    def send(self, data):
        if self._socket:
            if self._useBuffer:
                with self._userlock:
                    if len(self._buffer) + len(data) > 1024:
                        self._socket.send(self._buffer)
                        self._buffer = "%s\r\n" % data
                    else:
                        self._buffer = "%s%s\r\n" % (self._buffer, data)
            else:
                with self._userlock:
                    self._socket.send("%s\r\n" % data)
            if hasattr(config, "debug"):
                logger.debug("[%s]: %s" % (self.nick, data), True, False)


    # channel management
    def join(self, channel, key=""): # attempt joining a channel
        """ 
        returns: 
        0 = joined successfully
        1 = error joining
        2 = channel is full
        3 = bad key
        4 = is banned
        5 = invite only
        """
        if channel.globalchannel == False:
            if "i" in channel.modes.list():
                return 5
            if "k" in channel.modes.list():
                print "trying to match %s" % key
                if not channel.modes.match("k", key):
                    print "no match for %s" % key
                    return 3 # send wrong password message
            if channel.isFull:
                return 2 # send channel full message, and redirect if set

            # TODO: check if banned etc
            if channel.modes.match("b", self.hostmask):
                if not channel.modes.match("e", self.hostmask):
                    return 4
            
            channel.users.append(self)

            self.channels.append(channel)

            network.commands.payloads.OnJoinChannel(channel, self)

            return 0
        else:
            pass

    def part(self, channel, reason="Leaving", isParting=True): # attempt leaving a channel
        if channel.globalchannel == False:
            if not self in channel.users:
                return False # user not even in channel, duh

            if isParting:
                channel.send(network.commands.events.PART(self.hostmask, channel.name, reason))
            try:
                channel.users.remove(self)
                self.channels.remove(channel)
            except: # so he wasnt in there after all
                pass
            channel.update()
        else:
            pass

    def quit(self, reason="Leaving"):
        qp = network.commands.events.QUIT(self.hostmask, reason)
        for channel in self.channels:
            channel.send(qp)
            self.part(channel, reason, False)
            