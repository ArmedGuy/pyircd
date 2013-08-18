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
                    return 0 # channel did not exist
                c.modes.set(handler.user, " ".join(cmd.args))
            else: # user
                u = self._daemon.user(target)
                if not u:
                    return 1
                if not handler.user.modes.matchany("oO") and (u != handler.user):
                    handler.user.send(ERR_USERSDONTMATCH(handler.user))
                    return 1 # can only mode own user
                u.modes.set(handler.user, " ".join(cmd.args))
        else:
            if len(cmd.args) == 1:
                target = cmd.args[0]
                if target[0] in "#~": # channel
                    c = self._daemon.channel(target, False)
                    if not c:
                        return 0 # channel did not exist
                    network.commands.payloads.OnChannelMode(c, handler.user)
                """else: # user
                    u = self._daemon.user(target)
                    if not u:
                        return 0
                    if not handler.user.modes.matchany("oO") and (u != handler.user):
                        return 0 # can only mode own user
                    u.modes.set(handler.user, " ".join(cmd.args))"""
            else:
                handler.user.send(ERR_NEEDMOREPARAMS(handler.user, "MODE"))
                return 1

