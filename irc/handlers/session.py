import network, irc.commands.payloads, logger, socket, irc.user, irc.commandhandler, irc.commands.replies
class NickHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["NICK"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) != 1:
            return
        if handler.user != None:
            old = handler.user.hostmask
            handler.user.nick = cmd.args[0]
            for c in handler.user.channels:
                c.send(irc.commands.events.NICK(old, handler.user.nick))
        else:
            # TODO: check if username is available and accepted
            if "user-auth-data" in handler.cache:
                host = network.getUserHostname(handler.request)
                handler.user = irc.user.User(
                    handler.request,
                    cmd.args[0],
                    handler.cache["user-auth-data"][0],
                    host[0]
                )
                handler.user.real_hostname = host[1]
                handler.user.realname = handler.cache["user-auth-data"][1]
                handler.daemon.users.append(handler.user)
                irc.commands.payloads.OnUserConnect(self._daemon, handler.user)
            else:
                handler.cache["nick-auth-data"] = cmd.args[0]


class UserHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["USER"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) != 4:
            return
        if "nick-auth-data" in handler.cache:
            host = network.getUserHostname(handler.request)
            handler.user = irc.user.User(
                handler.request,
                handler.cache["nick-auth-data"],
                cmd.args[0],
                host[0]
            )
            handler.user.real_hostname = host[1]
            handler.user.realname = cmd.args[3]
            handler.daemon.users.append(handler.user)
            irc.commands.payloads.OnUserConnect(self._daemon, handler.user)
        else:
            handler.cache["user-auth-data"] = (cmd.args[0], cmd.args[3])

class QuitHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["QUIT"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if handler.user:
            if len(cmd.args) == 1:
                handler.user.quit(cmd.args[0])
            else:
                handler.user.quit()
            handler.terminate()