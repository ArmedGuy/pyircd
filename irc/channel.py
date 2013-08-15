import irc.modes
class Channel:
    globalchannel = True # hashtag for global, ~ for local
    name = ""
    topic = ""

    users = None

    modes = None

    def __init__(self, name):
        if name[0] == "~":
            self.globalchannel = False
        else:
            self.globalchannel = True

        self.name = name
        self.users = []
        self.modes = irc.modes.ChannelModes(self)

        self.modes.handle("+nt")
        # Cnpstz

