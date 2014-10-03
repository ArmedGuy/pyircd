import irc.commandhandler, irc.commands.events
from irc.commands.errors import *
class MsgHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["NOTICE", "PRIVMSG"]
        self._daemon = daemon

    def handle(self, handler, cmd):
        if len(cmd.args) != 2:
            handler.user.send(ERR_NEEDMOREPARAMS(handler.user, cmd.command))
            return 0 # not enough commands
        target = cmd.args[0]
        if target[0] in "#~": # channel
            c = self._daemon.channel(target, False)
            if not c:
                handler.user.send(ERR_NOSUCHCHANNEL(handler.user, target))
                return 0 # channel not found
            if c.modes.match("n") and handler.user not in c.users:
                handler.user.send(ERR_NOTONCHANNEL(handler.user, target))
                return 0 # no "not-in-channel" messages
            if cmd.command == "NOTICE":
                c.send(irc.commands.events.NOTICE(handler.user.hostmask, c.name, cmd.args[1]))
            else:
                c.send(irc.commands.events.PRIVMSG(handler.user.hostmask, c.name, cmd.args[1]))
        else: # user
            u = self._daemon.user(target)
            if not u:
                handler.user.send(ERR_NOSUCHNICK(handler.user, target))
                return 0 # user not found

            # TODO: is there anything more to check?

            if cmd.command == "NOTICE":
                u.send(irc.commands.events.NOTICE(handler.user.hostmask, u.nick, cmd.args[1]))
            else:
                u.send(irc.commands.events.PRIVMSG(handler.user.hostmask, u.nick, cmd.args[1]))
        return 0