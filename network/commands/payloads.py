from network.commands.replies import *
from network.commands.events import *
import config, sys
class OnUserConnect():
    def __init__(self, daemon, user):
        user.buffer(True)
        user.send(RPL_WELCOME(user))
        user.send(RPL_YOURHOST(user))
        user.send(RPL_CREATED(user))
        user.send(RPL_MYINFO(user))
        for support in config.isupport:
            user.send(RPL_ISUPPORT(user, support))

        user.send(RPL_LUSERCLIENT(user, daemon))
        user.send(RPL_LUSEROP(user, daemon))
        user.send(RPL_LUSERCHANNELS(user, daemon))
        user.send(RPL_LUSERME(user, daemon))
        user.send(RPL_LOCALUSERS(user, daemon))
        user.send(RPL_GLOBALUSERS(user, daemon))

        user.send(RPL_MOTDSTART(user))
        for line in config.motd:
            user.send(RPL_MOTD(user, line))
        user.send(RPL_ENDOFMOTD(user))
        user.buffer(False)

        # set modes

        user.modes.set(config.servername, "+ix")

class OnJoinChannel():
    def __init__(self, channel, user):
        channel.send(JOIN(user.hostmask, channel.name))

        type = "="
        if channel.modes.match("s"):
            type = "@"
        if channel.modes.match("p"):
            type = "*"

        for ulist in channel.nameslist(user):
            user.send(RPL_NAMREPLY(user, type, channel.name, ulist))
        user.send(RPL_ENDOFNAMES(user, channel.name))

        OnTopic(channel, user)

class OnChannelMode():
    def __init__(self, channel, user):
        user.send(RPL_CHANNELMODEIS(user, channel.name, "+%s" % channel.modes.list(True)))
        user.send(RPL_CREATIONTIME(user, channel.name, channel.created))
class OnTopic():
    def __init__(self, channel, user):
        if channel.topic != None:
            user.send(RPL_TOPIC(user, channel.name, channel.topic[0]))
            user.send(RPL_TOPICWHOTIME(user, channel.name, channel.topic[1], channel.topic[2]))
        