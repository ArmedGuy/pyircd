from network.commands.replies import *
import config, sys
class OnUserConnect():
    def __init__(self, daemon, user):
        user.send(RPL_WELCOME(user).ToString())
        user.send(RPL_YOURHOST(user).ToString())
        user.send(RPL_CREATED(user).ToString())
        user.send(RPL_MYINFO(user).ToString())
        for support in config.isupport:
            user.send(RPL_ISUPPORT(user, support).ToString())

        user.send(RPL_LUSERCLIENT(user, daemon).ToString())
        user.send(RPL_LUSEROP(user, daemon).ToString())
        user.send(RPL_LUSERCHANNELS(user, daemon).ToString())
        user.send(RPL_LUSERME(user, daemon).ToString())
        user.send(RPL_LOCALUSERS(user, daemon).ToString())
        user.send(RPL_GLOBALUSERS(user, daemon).ToString())

        user.send(RPL_MOTDSTART(user).ToString())
        for line in config.motd:
            user.send(RPL_MOTD(user, line).ToString())
        user.send(RPL_ENDOFMOTD(user).ToString())

        # set modes

        user.modes.set(config.servername, "+ix")

class OnJoinChannel():
    def __init__(self, channel, user):
        channel.send(RPL_JOIN(user.hostmask, channel.name))

        type = "="
        if channel.modes.match("s"):
            type = "@"
        if channel.modes.match("p"):
            type = "*"

        for ulist in channel.nameslist(user):
            user.send(RPL_NAMREPLY(user, type, channel.name, ulist).ToString())
        user.send(RPL_ENDOFNAMES(user, channel.name).ToString())

        OnTopic(channel, user)

class OnChannelMode():
    def __init__(self, channel, user):
        user.send(RPL_CHANNELMODEIS(user, channel.name, "+%s" % channel.modes.list(True)).ToString())
        user.send(RPL_CREATIONTIME(user, channel.name, channel.created).ToString())
class OnTopic():
    def __init__(self, channel, user):
        if channel.topic != None:
            user.send(RPL_TOPIC(user, channel.name, channel.topic[0]).ToString())
            user.send(RPL_TOPICWHOTIME(user, channel.name, channel.topic[1], channel.topic[2]).ToString())
        