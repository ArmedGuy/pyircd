import irc.modes, config, network.commands.payloads, logger, time, threading
class Channel:
    globalchannel = True # hashtag for global, ~ for local
    name = ""
    topic = None

    created = 0
    users = None

    modes = None

    _daemon = None

    _chanlock = None

    def __init__(self, daemon, name):
        self._daemon = daemon
        if name[0] == "#":
            self.globalchannel = False
            logger.info("Creating new local channel %s" % name)
        else:
            self.globalchannel = True
            logger.info("Creating new global channel %s" % name)

        self.created = int(time.time())
        self.name = name
        self.users = []

        self.modes = irc.modes.ChannelModes(self)
        self.modes.set(config.servername, "+nt")

        self._daemon.channels.append(self)
        self._chanlock = threading.Lock()

    def update(self):
        if len(self.users) == 0 and not self.modes.match("r"):
            try:
                logger.info("Removing empty & unregistered channel %s" % self.name)
                self._daemon.channels.remove(self)
            except:
                logger.error("Failed to remove empty & unregistered channel %s" % self.name)
    def nameslist(self, requester):
        ulist = []
        tmp = []
        i = 0
        prefix = ""

        canSeeUser = (requester.modes.match("oO") or self.modes.matchany("qao", (requester.nick, requester.nick, requester.nick) ))
        for u in self.users:
            prefix = ""
            if self.modes.match("v", u.nick):
                prefix = "+"
            if self.modes.match("h", u.nick):
                prefix = "%"
            if self.modes.match("o", u.nick):
                prefix = "@"
            if self.modes.match("a", u.nick):
                prefix = "&"
            if self.modes.match("q", u.nick):
                prefix = "~"

            if self.modes.match("u") and not canSeeUser: # auditorium
                if prefix in "@&~":
                    tmp.append("%s%s" % (prefix, u.nick))
                    i = i + 1
            else:
                if not u.modes.match("I") or canSeeUser:
                    tmp.append("%s%s" % (prefix, u.nick))
                    i = i + 1
            if i > 5:
                ulist.append(" ".join(tmp))
                tmp = []
                i = 0
        if len(tmp) > 0:
            ulist.append(" ".join(tmp))
        tmp = None
        return ulist

    def _get_isFull(self):
        if "l" in self.modes.list():
            if self.modes.getValue("l") <= len(self.users):
                return True
            else:
                return False
        else:
            return False

    isFull = property(_get_isFull)

    def send(self, message): # TODO: join/part hidden messages and such
        c = message.ToCommand()
        for user in self.users:
            if (not user.modes.match("d") or c.command not in ("NOTICE", "PRIVMSG")) and not (c.command in ("NOTICE", "PRIVMSG") and c.sender == user.hostmask):
                user.send(message)
        del c


