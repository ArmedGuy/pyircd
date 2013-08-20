import irc.commandhandler, network.commands.payloads
from network.commands.errors import *
class ModeHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["MODE"]
        self._daemon = daemon

    def handle(self, handler, cmd):
        if len(cmd.args) > 1:
            target = cmd.args[0]
            cmd.args = cmd.args[1:]
            if target[0] in "#~": # channel
                c = self._daemon.channel(target, False)
                if not c:
                    handler.user.send(ERR_NOSUCHCHANNEL(handler.user, target))
                    return 0 # channel did not exist
                if c not in handler.user.channels:
                    handler.user.send(ERR_NOTONCHANNEL(handler.user, target))
                    return 0
                c.modes.set(handler.user, " ".join(cmd.args))
                return 0
            else: # user
                u = self._daemon.user(target)
                if not u:
                    handler.user.send(ERR_NOSUCHNICK(handler.user, target))
                    return 0
                if not handler.user.modes.matchany("oO") and (u != handler.user):
                    handler.user.send(ERR_USERSDONTMATCH(handler.user))
                    return 0 # can only mode own user
                u.modes.set(handler.user, " ".join(cmd.args))
                return 0
        else:
            if len(cmd.args) == 1:
                target = cmd.args[0]
                if target[0] in "#~": # channel
                    c = self._daemon.channel(target, False)
                    if not c:
                        handler.user.send(ERR_NOSUCHCHANNEL(handler.user, target))
                        return 0 # channel did not exist
                    network.commands.payloads.OnChannelMode(c, handler.user)
                    return 0
                """else: # user
                    u = self._daemon.user(target)
                    if not u:
                        handler.user.send(ERR_NOSUCHNICK(handler.user, target))
                        return 0
                    if not handler.user.modes.matchany("oO") and (u != handler.user):
                        handler.user.send(ERR_USERSDONTMATCH(handler.user))
                        return 0 # can only mode own user
                    u.modes.set(handler.user, " ".join(cmd.args))
                    return 0"""
            else:
                handler.user.send(ERR_NEEDMOREPARAMS(handler.user, "MODE"))
                return 0
        return 0

