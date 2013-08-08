from irc.commands.replies import *
import logger
class OnUserConnect():
    def __init__(self, user):
        user.send(RPL_WELCOME(user).ToString())
        user.send(RPL_YOURHOST(user).ToString())
        user.send(RPL_CREATED(user).ToString())
        user.send(RPL_MYINFO(user).ToString())
        logger.debug("sent all info!")
