import irc.commandhandler, network.commands.payloads, network.commands.replies, network.commands.events, time
from network.commands.errors import *
class TopicHandler(irc.commandhandler.CommandHandler):
    def __init__(self, daemon):
        self.handlesCommands = ["TOPIC"]
        self._daemon = daemon
    def handle(self, handler, cmd):
        if len(cmd.args) < 1:
            handler.user.send(ERR_NEEDMOREPARAMS(handler.user, "TOPIC"))
            return 0
        c = self._daemon.channel(cmd.args[0])
        if not c:
            handler.user.send(ERR_NOSUCHCHANNEL(handler.user, cmd.args[0]))
            return 0 # channel not found
        if c not in handler.user.channels:
            handler.user.send(ERR_NOTONCHANNEL(handler.user, c.name))
            return 0 # not in channel
        if len(cmd.args) == 2:
            n = handler.user.nick
            if c.modes.match("t"):
                if c.modes.matchany("hoaq", (n, n, n, n) ):
                    c.topic = (cmd.args[1], n, int(time.time()))
                    c.send(network.commands.events.TOPIC(handler.user.hostmask, c.name, cmd.args[1]))
                else:
                    handler.user.send(ERR_NOPRIVILEGES(handler.user))
                    return 0 # no access
            else:
                c.topic = (cmd.args[1], n, int(time.time()))
                c.send(network.commands.events.TOPIC(handler.user.hostmask, c.name, cmd.args[1]))
        else:
            if c.topic != None:
                network.commands.payloads.OnTopic(c, handler.user)
            else:
                network.commands.replies.RPL_NOTOPIC(handler.user, c)
        return 0

