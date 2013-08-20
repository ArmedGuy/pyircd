import config, irc.flags
from command import *
import network

# numeric commands sent by server

class RPL_WELCOME(Command): #001
    def __init__(self, target):
        self.init("001")
        self.to(target)
        self.arg(text("Welcome to the pyircd test server %s" % target.nick))

class RPL_YOURHOST(Command): #002
    def __init__(self, target):
        self.init("002")
        self.to(target)
        self.arg(text("Your host is %s, running version %s[%s/%s]" % (config.servername, config.version, config.host, config.listenports)))

class RPL_CREATED(Command): #003
    def __init__(self, target):
        self.init("003")
        self.to(target)
        self.arg(text("This server was created %s" % config.daemonstarted))
       
class RPL_MYINFO(Command): #004
    def __init__(self, target):
        self.init("004")
        self.to(target)
        self.arg(config.servername)
        self.arg(config.version)
        self.arg(irc.flags.user_modes)
        self.arg(irc.flags.channel_modes)

class RPL_ISUPPORT(Command): #005
    def __init__(self, target, support):
        self.init("005")
        self.to(target)
        self.arg(support)
        self.arg(text("Is supported by this server"))

class RPL_LUSERCLIENT(Command): #251
    def __init__(self, target, daemon):
        self.init("251")
        self.to(target)
        self.arg(text("There are %d users and %d invisible on %d servers" % (daemon.netstats.globalusers, daemon.netstats.globalinvisible, daemon.netstats.globalservers) ))

class RPL_LUSEROP(Command): #252
    def __init__(self, target, daemon):
        self.init("252")
        self.to(target)
        self.arg(daemon.netstats.globalopers)
        self.arg(text("IRC Operators online"))

class RPL_LUSERCHANNELS(Command): #254
    def __init__(self, target, daemon):
        self.init("254")
        self.to(target)
        self.arg(daemon.netstats.globalchans)
        self.arg(text("channels formed"))

class RPL_LUSERME(Command): #255
    def __init__(self, target, daemon):
        self.init("255")
        self.to(target)
        self.arg(text("I have %d clients and %d servers" % (daemon.netstats.localusers, daemon.netstats.localservers) ))

class RPL_LOCALUSERS(Command): #265
    def __init__(self, target, daemon):
        self.init("265")
        self.to(target)
        self.arg(daemon.netstats.localusers)
        self.arg(config.maxclients)
        self.arg(text("Current local users %d, max %d" % (daemon.netstats.localusers, config.maxclients) ))

class RPL_GLOBALUSERS(Command): #266
    def __init__(self, target, daemon):
        self.init("266")
        self.to(target)
        self.arg(daemon.netstats.globalusers)
        self.arg(daemon.netstats.globalmaxclients)
        self.arg(text("Current global users %d, max %d" % (daemon.netstats.globalusers, daemon.netstats.globalmaxclients) ))


class RPL_CHANNELMODEIS(Command): #324
    def __init__(self, target, channel, modes):
        self.init("324")
        self.to(target)
        self.arg(channel)
        self.arg(modes)

class RPL_CREATIONTIME(Command): #329
    def __init__(self, target, channel, created):
        self.init("329")
        self.to(target)
        self.arg(channel)
        self.arg(created)

class RPL_NOTOPIC(Command): # 331
    def __init__(self, target, channel):
        self.init("331")
        self.to(target)
        self.arg(channel)
        self.arg(text("No topic is set"))

class RPL_TOPIC(Command): #332
    def __init__(self, target, channel, topic):
        self.init("332")
        self.to(target)
        self.arg(channel)
        self.arg(text(topic))

class RPL_TOPICWHOTIME(Command): #333
    def __init__(self, target, channel, who, time):
        self.init("333")
        self.to(target)
        self.arg(channel)
        self.arg(who)
        self.arg(time)

class RPL_NAMREPLY(Command): # 353
    def __init__(self, target, type, channel, users):
        self.init("353")
        self.to(target)
        self.arg(type)
        self.arg(channel)
        self.arg(text(users))

class RPL_ENDOFNAMES(Command): # 366
    def __init__(self, target, channel):
        self.init("366")
        self.to(target)
        self.arg(channel)
        self.arg(text("End of /NAMES list"))

class RPL_BANLIST(Command): # 367
    def __init__(self, target, channel, banmask, nick, time):
        self.init("367")
        self.to(target)
        self.arg(channel)
        self.arg(banmask)
        self.arg(nick)
        self.arg(time)

class RPL_ENDOFBANLIST(Command): # 368
    def __init__(self, target, channel):
        self.init("368")
        self.to(target)
        self.arg(channel)
        self.arg(text("End of Channel Ban List"))

class RPL_MOTD(Command): #372
    def __init__(self, target, line):
        self.init("372")
        self.to(target)
        self.arg(text("- %s" % line))

class RPL_MOTDSTART(Command): #375
    def __init__(self, target):
        self.init("375")
        self.to(target)
        self.arg(text("- %s Message of the Day -" % config.servername))

class RPL_ENDOFMOTD(Command): #376
    def __init__(self, target):
        self.init("376")
        self.to(target)
        self.arg(text("- End of /MOTD Command -"))