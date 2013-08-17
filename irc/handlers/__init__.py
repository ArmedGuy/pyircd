import ping, session, chan, mode
def getHandlers(daemon):
    return [
            session.NickHandler(daemon),
            session.UserHandler(daemon),
            session.QuitHandler(daemon),
            ping.PingHandler(daemon),
            chan.JoinHandler(daemon),
            chan.PartHandler(daemon),
            mode.ModeHandler(daemon)
    ]