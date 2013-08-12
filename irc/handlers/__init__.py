import ping, login
def getHandlers(daemon):
    return [
            login.NickHandler(daemon),
            login.UserHandler(daemon),
            ping.PingHandler(daemon)
    ]