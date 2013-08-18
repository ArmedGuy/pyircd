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
        if handler.user.join(chan):
            if len(chan.users) == 1 and not chan.modes.match("r"):
                chan.modes.set(config.servername, "+o %s" % handler.user.nick)
        else:
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
            return 0
        else:
            if len(cmd.args) == 2:
                handler.user.part(chan, cmd.args[1])
            else:
                handler.user.part(chan)

