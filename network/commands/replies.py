import config, irc.flags
from command import *
import network

# named commands sent by server
class RPL_PONG(Command):
    def __init__(self, msg):
        self.initServerMessage("PONG")
        self.arg(msg)

class RPL_NOTICE(Command):
    def __init__(self, sender, reciever, msg):
        if sender[0] == ":":
            sender = sender[1:]
        self.arg(":%s" % sender)
        self.arg("NOTICE")
        self.to(reciever)
        self.arg(text(msg))

class RPL_PRIVMSG(Command):
    def __init__(self, sender, reciever, msg):
        self.arg(":%s" % sender)
        self.arg("PRIVMSG")
        self.to(reciever)
        self.arg(text(msg))

class RPL_MODE(Command):
    def __init__(self, user, modes):
        self.arg(":%s" % user.hostmask) # not the only possibility
        self.arg("MODE")
        self.arg(user.name)
        self.arg(text(modes))

# numeric commands sent by server

class RPL_WELCOME(Command): #001
    def __init__(self, user):
        self.initServerMessage("001")
        self.to(user)
        self.arg(text("Welcome to the pyircd test server %s" % user.nick))

class RPL_YOURHOST(Command): #002
    def __init__(self, user):
        self.initServerMessage("002")
        self.to(user)
        self.arg(text("Your host is %s, running version %s[%s/%s]" % (config.servername, config.version, config.host, config.listenports)))

class RPL_CREATED(Command): #003
    def __init__(self, user):
        self.initServerMessage("003")
        self.to(user)
        self.arg(text("This server was created %s" % config.daemonstarted))
       
class RPL_MYINFO(Command): #004
    def __init__(self, user):
        self.initServerMessage("004")
        self.to(user)
        self.arg(config.servername)
        self.arg(config.version)
        self.arg(irc.flags.user_modes)
        self.arg(irc.flags.channel_modes)

class RPL_ISUPPORT(Command): #005
    def __init__(self, user, support):
        self.initServerMessage("005")
        self.to(user)
        self.arg(support)
        self.arg(text("Is supported by this server"))

class RPL_LUSERCLIENT(Command): #251
    def __init__(self, user, daemon):
        self.initServerMessage("251")
        self.to(user)
        self.arg(text("There are %d users and %d invisible on %d servers" % (daemon.netstats.globalusers, daemon.netstats.globalinvisible, daemon.netstats.globalservers) ))

class RPL_LUSEROP(Command): #252
    def __init__(self, user, daemon):
        self.initServerMessage("252")
        self.to(user)
        self.arg(daemon.netstats.globalopers)
        self.arg(text("IRC Operators online"))

class RPL_LUSERCHANNELS(Command): #254
    def __init__(self, user, daemon):
        self.initServerMessage("254")
        self.to(user)
        self.arg(daemon.netstats.globalchans)
        self.arg(text("channels formed"))

class RPL_LUSERME(Command): #255
    def __init__(self, user, daemon):
        self.initServerMessage("255")
        self.to(user)
        self.arg(text("I have %d clients and %d servers" % (daemon.netstats.localusers, daemon.netstats.localservers) ))

class RPL_LOCALUSERS(Command): #265
    def __init__(self, user, daemon):
        self.initServerMessage("265")
        self.to(user)
        self.arg(daemon.netstats.localusers)
        self.arg(config.maxclients)
        self.arg(text("Current local users %d, max %d" % (daemon.netstats.localusers, config.maxclients) ))

class RPL_GLOBALUSERS(Command): #266
    def __init__(self, user, daemon):
        self.initServerMessage("266")
        self.to(user)
        self.arg(daemon.netstats.globalusers)
        self.arg(daemon.netstats.globalmaxclients)
        self.arg(text("Current global users %d, max %d" % (daemon.netstats.globalusers, daemon.netstats.globalmaxclients) ))

class RPL_MOTD(Command): #372
    def __init__(self, user, line):
        self.initServerMessage("372")
        self.to(user)
        self.arg(text("- %s" % line))

class RPL_MOTDSTART(Command): #375
    def __init__(self, user):
        self.initServerMessage("375")
        self.to(user)
        self.arg(text("- %s Message of the Day -" % config.servername))

class RPL_ENDOFMOTD(Command): #376
    def __init__(self, user):
        self.initServerMessage("376")
        self.to(user)
        self.arg(text("- End of /MOTD Command -"))