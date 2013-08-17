import irc.commandhandler, network.commands.replies
class MsgHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["NOTICE", "PRIVMSG"]
        self._daemon = daemon

    def handle(self, handler, cmd):
        if len(cmd.args) != 2:
            return 0 # not enough commands
        target = cmd.args[0]
        if target[0] in "#~": # channel
            c = self._daemon.channel(target)
            if not c:
                return 0 # channel not found
            if c.modes.match("n") and handler.user not in c.users:
                return 0 # no "not-in-channel" messages
            if cmd.command == "NOTICE":
                c.send(network.commands.replies.RPL_NOTICE(handler.user.hostmask, c.name, cmd.args[1]))
            else:
                c.send(network.commands.replies.RPL_PRIVMSG(handler.user.hostmask, c.name, cmd.args[1]))
        else: # user
            u = self._daemon.user(target)
            if not u:
                return 0 # user not found

            # TODO: is there anything more to check?

            if cmd.command == "NOTICE":
                c.send(network.commands.replies.RPL_NOTICE(handler.user.hostmask, u.nick, cmd.args[1]))
            else:
                c.send(network.commands.replies.RPL_PRIVMSG(handler.user.hostmask, u.nick, cmd.args[1]))