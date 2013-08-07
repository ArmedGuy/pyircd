import config, flags
def hostname():
    return ":%s" % config.servername
def text(data):
    return ":%s" % data
# Base command class
class Command:
    _args = []
    def ToString(self):
        return ' '.join(self._args)

        
class RPL_WELCOME(Command): #001
    def __init__(self, user):
        _args.append(hostname())
        _args.append("001")
        _args.append(user.nick)
        _args.append(text("Welcome to the pyircd test server %s" % user.nick))

class RPL_YOURHOST(Command): #002
    def __init__(self, user):
        _args.append(hostname())
        _args.append("002")
        _args.append(user.nick)
        _args.append(text("Your host is %s, running version %s[%s/%d], running version %s" % (config.servername, config.host, config.listenport, config.version)))

class RPL_CREATED(Command): #003
    def __init__(self, user):
        _args.append(hostname())
        _args.append("003")
        _args.append(user.nick)
        _args.append(text("This server was created at x date"))
       
class RPL_MYINFO(Command):
    def __init__(self, user):
        _args.append(hostname())
        _args.append("004")
        _args.append(user.nick)
        _args.append(config.servername)
        _args.append(config.version)
        _args.append(flags.user_modes)
        _args.append(flags.channel_modes)