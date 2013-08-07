from * import commands
class OnUserConnect():
    def __init__(self, user):
        user.send(RPL_WELCOME(user))
        user.send(RPL_YOURHOST(user))
        user.send(RPL_CREATED(user))
        user.send(RPL_MYINFO(user))
