import irc.commandhandler, logger
class JoinHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["JOIN"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) < 1:
            return 0
        chan = self._daemon.channel(cmd.args[0])
        if handler.user.join(chan):
            pass # user.join sends bad messages etc
        else:
            pass

class PartHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["PART"]
        self._daemon = daemon

    def handle(self, handler, cmd):
        if len(cmd.args) < 1:
            return 0
        chan = self._daemon.channel(cmd.args[0], False)
        if not chan:
            return 0
        else:
            if len(cmd.args) == 2:
                handler.user.part(chan, cmd.args[1])
            else:
                handler.user.part(chan)

