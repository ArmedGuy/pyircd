import config, irc.flags
from command import *

class RPL_WELCOME(Command): #001
    def __init__(self, user):
        self._args = []
        self._args.append(hostname())
        self._args.append("001")
        self._args.append(user.nick)
        self._args.append(text("Welcome to the pyircd test server %s" % user.nick))

class RPL_YOURHOST(Command): #002
    def __init__(self, user):
        self._args = []
        self._args.append(hostname())
        self._args.append("002")
        self._args.append(user.nick)
        self._args.append(text("Your host is %s, running version %s[%s/%s]" % (config.servername, config.version, config.host, config.listenports)))

class RPL_CREATED(Command): #003
    def __init__(self, user):
        self._args = []
        self._args.append(hostname())
        self._args.append("003")
        self._args.append(user.nick)
        self._args.append(text("This server was created at x date"))
       
class RPL_MYINFO(Command):
    def __init__(self, user):
        self._args = []
        self._args.append(hostname())
        self._args.append("004")
        self._args.append(user.nick)
        self._args.append(config.servername)
        self._args.append(config.version)
        self._args.append(irc.flags.user_modes)
        self._args.append(irc.flags.channel_modes)