from network.commands.replies import *
class OnUserConnect():
    def __init__(self, user):
        user.send(RPL_WELCOME(user).ToString())
        user.send(RPL_YOURHOST(user).ToString())
        user.send(RPL_CREATED(user).ToString())
        user.send(RPL_MYINFO(user).ToString())
        #user.send(RPL_ISUPPORT(user).ToString())
        user.send(RPL_LUSERCLIENT(user).ToString())
        user.send(RPL_LUSEROP(user).ToString())
        user.send(RPL_LUSERCHANNELS(user).ToString())
        user.send(RPL_LUSERME(user).ToString())
        user.send(RPL_LOCALUSERS(user).ToString())
        user.send(RPL_GLOBALUSERS(user).ToString())

        #TODO: send MOTD
