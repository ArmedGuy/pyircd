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