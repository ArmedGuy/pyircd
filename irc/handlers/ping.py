import network.commands.events, irc.commandhandler
class PingHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["PING"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) != 1:
            return
        handler.user.send(network.commands.events.PONG(cmd.args[0]))