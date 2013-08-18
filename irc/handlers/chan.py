import irc.commandhandler, logger, config
from network.commands.errors import *
class JoinHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["JOIN"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) < 1:
            handler.user.send(ERR_NEEDMOREPARAMS(handler.user, "JOIN"))
            return 1
        chan = self._daemon.channel(cmd.args[0])
        result = handler.user.join(chan)
        if result == 0:
            if len(chan.users) == 1 and not chan.modes.match("r"):
                chan.modes.set(config.servername, "+o %s" % handler.user.nick)
        elif result == 1: # unknown error
            pass
        elif result == 2: # chan full
            pass
        elif result == 3: # wrong key
            pass
        elif result == 4: # banned
            pass
        elif result == 5: # invite only channel
            pass

class PartHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["PART"]
        self._daemon = daemon

    def handle(self, handler, cmd):
        if len(cmd.args) < 1:
            handler.user.send(ERR_NEEDMOREPARAMS(handler.user, "PART"))
            return 1
        chan = self._daemon.channel(cmd.args[0], False)
        if not chan:
            handler.user.send(ERR_NOSUCHCHANNEL(handler.user, cmd.args[0]))
            return 1
        else:
            if len(cmd.args) == 2:
                handler.user.part(chan, cmd.args[1])
            else:
                handler.user.part(chan)

