from network.commands.replies import *
import config, sys
class OnUserConnect():
    def __init__(self, user):
        try:
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
            user.send(RPL_MOTDSTART(user).ToString())
            for line in config.motd:
                user.send(RPL_MOTD(user, line).ToString())
            user.send(RPL_ENDOFMOTD(user).ToString())
        except:
            for var in sys.exc_info():
                logger.error(str("%s" % var).strip())
