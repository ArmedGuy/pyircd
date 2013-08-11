import irc.handlers, irc.user, network, network.commands.payloads, logger, socket
class NickHandler(irc.handlers.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["NICK"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) != 1:
            return
        if handler.user != None:
            # change nick
            pass
        else:
            # TODO: check if username is available
            if "user-auth-data" in handler.cache:
                handler.user = irc.user.User(handler.request, cmd.args[0], handler.cache["user-auth-data"][0], network.getUserHostname(handler.request.getpeername()[0]))
                handler.user.realname = handler.cache["user-auth-data"][1]
                network.commands.payloads.OnUserConnect(handler.user)
            else:
                handler.cache["nick-auth-data"] = cmd.args[0]

class UserHandler(irc.handlers.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["USER"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) != 4:
            return
        if "nick-auth-data" in handler.cache:
            handler.user = irc.user.User(handler.request, handler.cache["nick-auth-data"], cmd.args[0], network.getUserHostname(handler.request.getpeername()[0]))
            handler.user.realname = cmd.args[3]
            network.commands.payloads.OnUserConnect(handler.user)
        else:
            handler.cache["user-auth-data"] = (cmd.args[0], cmd.args[3])
        