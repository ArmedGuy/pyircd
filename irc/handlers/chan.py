import irc.commandhandler, logger, config
from irc.commands.errors import *
class JoinHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["JOIN"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) < 1:
            handler.user.send(ERR_NEEDMOREPARAMS(handler.user, "JOIN"))
            return 0
        chan = self._daemon.channel(cmd.args[0])
        result = 1
        if len(cmd.args) == 2:
            result = handler.user.join(chan, cmd.args[1])
        else:
            result = handler.user.join(chan)
        if result == 0:
            if len(chan.users) == 1 and not chan.modes.match("r"):
                chan.modes.set(config.servername, "+o %s" % handler.user.nick)
        elif result == 1: # unknown error
            pass
        elif result == 2: # chan full
            handler.user.send(ERR_CHANNELISFULL(handler.user, chan.name))
        elif result == 3: # wrong key
            handler.user.send(ERR_BADCHANNELKEY(handler.user, chan.name))
        elif result == 4: # banned
            handler.user.send(ERR_BANNEDFROMCHAN(handler.user, chan.name))
        elif result == 5: # invite only channel
            handler.user.send(ERR_INVITEONLYCHAN(handler.user, chan.name))
        return 0

class PartHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["PART"]
        self._daemon = daemon

    def handle(self, handler, cmd):
        if len(cmd.args) < 1:
            handler.user.send(ERR_NEEDMOREPARAMS(handler.user, "PART"))
            return 0
        chan = self._daemon.channel(cmd.args[0], False)
        if not chan:
            handler.user.send(ERR_NOSUCHCHANNEL(handler.user, cmd.args[0]))
            return 0
        else:
            if len(cmd.args) == 2:
                handler.user.part(chan, cmd.args[1])
            else:
                handler.user.part(chan)
            return 0

class KickHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["KICK"]
        self._daemon = daemon

    def handle(self, handler, cmd):
        if len(cmd.args) < 2:
            handler.user.send(ERR_NEEDMOREPARAMS(handler.user, "KICK"))
            return 0
        chan = self._daemon.channel(cmd.args[0], False)
        if not chan:
            handler.user.send(ERR_NOSUCHCHANNEL(handler.user, cmd.args[0]))
            return 0
        else:
            u = self._daemon.user(cmd.args[1])
            if not u:
                handler.user.send(ERR_NOSUCHNICK(handler.user, cmd.args[1]))
            if u not in chan.users:
                handler.user.send(ERR_NOTONCHANNEL(handler.user, cmd.args[1]))
            ## TODO: check if kicker has more rights than the kicked
            if len(cmd.args) == 3:
                chan.send(irc.commands.events.KICK(handler.user.hostmask, chan.name, u.nick))
            else:
                chan.send(irc.commands.events.KICK(handler.user.hostmask, chan.name, u.nick))