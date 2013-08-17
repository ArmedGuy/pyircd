import re, flags, logger, config, irc.modes, network.commands.payloads, network.commands.replies

username_regex = re.compile("/\A([a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]{2,15})\z/i")

class User():
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
    def __init__(self, socket, nick, ident, hostname):
        self._socket = socket
        self.nick = nick
        self.ident = ident
        self.hostname = hostname
        self.hostmask = "%s!%s@%s" % (nick, ident, hostname)

        self.modes = irc.modes.UserModes(self)


        self.channels = [] # local channels = full object, global channels = network pointer

    def send(self, data):
        if self._socket:
            self._socket.send("%s\r\n" % data)
            if hasattr(config, "debug"):
                logger.debug(data, True, False)


    # channel management
    def join(self, channel, key=""): # attempt joining a channel
        if channel.globalchannel == False:
            if "k" in channel.modes.list():
                if not channel.modes.match("k", key):
                    return False # send wrong password message
            if channel.isFull:
                return False # send channel full message, and redirect if set

            # TODO: check if banned etc
            channel.users.append(self)

            self.channels.append(channel)

            network.commands.payloads.OnJoinChannel(channel, self)
        else:
            pass

    def part(self, channel, reason="Leaving", isParting=True): # attempt leaving a channel
        if channel.globalchannel == False:
            if not self in channel.users:
                return False # user not even in channel, duh

            if isParting:
                channel.send(network.commands.replies.RPL_PART(self.hostmask, channel.name, reason))
            try:
                channel.users.remove(self)
                self.channels.remove(channel)
            except: # so he wasnt in there after all
                pass
            channel.update()
        else:
            pass

    def quit(self, reason="Leaving"):
        qp = network.commands.replies.RPL_QUIT(self.hostmask, reason)
        for channel in self.channels:
            channel.send(qp)
            self.part(channel, reason, False)
            