from command import *
class ERR_NOSUCHNICK(Command): # 401
    def __init__(self, target, nick):
        self.init("401")
        self.to(target)
        self.arg(nick)
        self.arg(text("No such nick"))

class ERR_NOSUCHCHANNEL(Command): # 403
    def __init__(self, target, channel):
        self.init("403")
        self.to(target)
        self.arg(channel)
        self.arg(text("No such channel"))

class ERR_UNKNOWNCOMMAND(Command):
    def __init__(self, target, command):
        self.init("421")
        self.to(target)
        self.arg(command)
        self.arg(text("Unknown command"))

class ERR_ERRONEUSNICKNAME(Command): # 432
    def __init__(self, target, nick):
        self.init("432")
        self.to(target)
        self.arg(nick)
        self.arg(text("Erroneus nickname"))

class ERR_NICKNAMEINUSE(Command): # 433
    def __init__(self, target, nick):
        self.init("433")
        self.to(target)
        self.arg(nick)
        self.arg(text("Nickname is already in use."))
class ERR_USERNOTINCHANNEL(Command): # 441
    def __init__(self, target, nick, channel):
        self.init("441")
        self.to(target)
        self.arg(nick)
        self.arg(text("They aren't in that channel"))

class ERR_NOTONCHANNEL(Command): # 442
    def __init__(self, target, channel):
        self.init("442")
        self.to(target)
        self.arg(channel)
        self.arg(text("You're not in that channel"))

class ERR_NEEDMOREPARAMS(Command): # 461
    def __init__(self, target, command, param=""):
        self.init("461")
        self.to(target)
        self.arg(command)
        if param != "":
            self.arg(param)
        self.arg(text("Not enough parameters"))

class ERR_CHANNELISFULL(Command): # 471
    def __init__(self, target, channel):
        self.init("471")
        self.to(target)
        self.arg(channel)
        self.arg(text("Cannot join channel, channel is full"))

class ERR_UNKNOWNMODE(Command): # 472
    def __init__(self, target, mode):
        self.init("472")
        self.to(target)
        self.arg(mode)
        self.arg(text("is unknown mode char to me"))

class ERR_INVITEONLYCHAN(Command): # 473
    def __init__(self, target, channel):
        self.init("473")
        self.to(target)
        self.arg(channel)
        self.arg(text("Cannot join channel, you must be invited (+i)"))

class ERR_BANNEDFROMCHAN(Command): # 474
    def __init__(self, target, channel):
        self.init("474")
        self.to(target)
        self.arg(channel)
        self.arg(text("Cannot join channel, you are banned (+b)"))

class ERR_BADCHANNELKEY(Command): # 475
    def __init__(self, target, channel):
        self.init("475")
        self.to(target)
        self.arg(channel)
        self.arg(text("Cannot join channel, you need the correct key (+k)"))
class ERR_BANLISTFULL(Command): # 478
    def __init__(self, target, channel, mask):
        self.init("478")
        self.to(target)
        self.arg(channel)
        self.arg(ask)
        self.arg(text("Channel ban/ignore list is full"))

class ERR_NOPRIVILEGES(Command): # 481
    def __init__(self, target):
        self.init("481")
        self.to(target)
        self.arg(text("Permission Denied: Insufficient priveleges!"))

class ERR_UMODEUNKNWONFLAG(Command): # 501 - unknown user mode
    def __init__(self, target, mode):
        self.init("501")
        self.to(target)
        self.arg(mode)
        self.arg(text("Unknown MODE flag"))

class ERR_USERSDONTMATCH(Command): # 502
    def __init__(self, target):
        self.init("502")
        self.to(target)
        self.arg(text("Can't change mode for other users"))
