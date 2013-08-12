import config, irc.flags
from command import *
import network

# named commands sent by server
class RPL_PONG(Command):
    def __init__(self, msg):
        self.initServerMessage("PONG")
        self.arg(msg)

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
        self.arg(text("This server was created at x date"))
       
class RPL_MYINFO(Command): #004
    def __init__(self, user):
        self.initServerMessage("004")
        self.to(user)
        self.arg(config.servername)
        self.arg(config.version)
        self.arg(irc.flags.user_modes)
        self.arg(irc.flags.channel_modes)

class RPL_ISUPPORT(Command): #005
    def __init__(self, user):
        self.initServerMessage("005")
        # TODO: fix

class RPL_LUSERCLIENT(Command): #251
    def __init__(self, user): # TODO, load from daemon
        self.initServerMessage("251")
        self.to(user)
        self.arg(text("There are %d users and %d invisible on %d servers" % (network.netstats.globalusers,network.netstats.globalinvisible,network.netstats.globalservers) ))

class RPL_LUSEROP(Command): #252
    def __init__(self, user):
        self.initServerMessage("252")
        self.to(user)
        self.arg(network.netstats.globalopers)
        self.arg(text("IRC Operators online"))

class RPL_LUSERCHANNELS(Command): #254
    def __init__(self, user):
        self.initServerMessage("254")
        self.to(user)
        self.arg(network.netstats.globalchans)
        self.arg(text("channels formed"))

class RPL_LUSERME(Command): #255
    def __init__(self, user):
        self.initServerMessage("255")
        self.to(user)
        self.arg(text("I have %d clients and %d servers" % (network.netstats.localusers, network.netstats.localservers) ))

class RPL_LOCALUSERS(Command): #265
    def __init__(self, user):
        self.initServerMessage("265")
        self.to(user)
        self.arg(network.netstats.localusers)
        self.arg(config.maxclients)
        self.arg(text("Current local users %d, max %d" % (network.netstats.localusers, config.maxclients) ))

class RPL_GLOBALUSERS(Command): #266
    def __init__(self, user):
        self.initServerMessage("266")
        self.to(user)
        self.arg(network.netstats.globalusers)
        self.arg(network.netstats.globalmaxclients)
        self.arg(text("Current global users %d, max %d" % (network.netstats.globalusers, network.netstats.globalmaxclients) ))

class RPL_MOTD(Command): #372
    def __init__(self, user, line):
        self.initServerMessage("372")
        self.to(user)
        self.arg(text(line))

class RPL_MOTDSTART(Command): #375
    def __init__(self, user):
        self.initServerMessage("375")
        self.to(user)
        self.arg(text("- %s Message of the Day -" % config.servername))

class RPL_ENDOFMOTD(Command): #376
    def __init__(self, user):
        self.initServerMessage("376")
        self.to(user)
        self.arg(text("- End of MOTD -"))