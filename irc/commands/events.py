from command import *

class PONG(Command):
    def __init__(self, msg):
        self.init("PONG")
        self.arg(msg)

class NOTICE(Command):
    def __init__(self, sender, reciever, msg):
        self.arg(":%s" % sender)
        self.arg("NOTICE")
        self.to(reciever)
        self.arg(text(msg))

class NICK(Command):
    def __init__(self, sender, newNick):
        self.arg(":%s" % sender)
        self.arg("NICK")
        self.arg(newNick)

class PRIVMSG(Command):
    def __init__(self, sender, reciever, msg):
        self.arg(":%s" % sender)
        self.arg("PRIVMSG")
        self.to(reciever)
        self.arg(text(msg))

class MODE(Command):
    def __init__(self, sender, reciever, modes):
        self.arg(":%s" % sender)
        self.arg("MODE")
        self.arg(reciever)
        self.arg(text(modes))

class JOIN(Command):
    def __init__(self, sender, chan):
        self.arg(":%s" % sender)
        self.arg("JOIN")
        self.arg(chan)

class PART(Command):
    def __init__(self, sender, chan, msg="Leaving"):
        self.arg(":%s" % sender)
        self.arg("PART")
        self.arg(chan)
        self.arg(text(msg))

class KICK(Command):
    def __init__(self, sender, chan, kicked, msg="Kicked"):
        self.arg(":%s" % sender)
        self.arg("KICK")
        self.arg(chan)
        self.arg(kicked)
        self.arg(text(msg))

class QUIT(Command):
    def __init__(self, sender, reason="Leaving"):
        self.arg(":%s" % sender)
        self.arg("QUIT")
        self.arg(text(reason))

class TOPIC(Command):
    def __init__(self, sender, channel, topic):
        self.arg(":%s" % sender)
        self.arg("TOPIC")
        self.arg(channel)
        self.arg(text(topic))