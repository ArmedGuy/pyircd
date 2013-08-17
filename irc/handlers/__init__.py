import ping, session, chan, mode, topic, msg
def getHandlers(daemon):
    return [
            session.NickHandler(daemon),
            session.UserHandler(daemon),
            session.QuitHandler(daemon),
            ping.PingHandler(daemon),
            chan.JoinHandler(daemon),
            chan.PartHandler(daemon),
            mode.ModeHandler(daemon),
            topic.TopicHandler(daemon),
            msg.MsgHandler(daemon)
    ]