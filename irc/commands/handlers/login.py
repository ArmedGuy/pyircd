class NickAuth(CommandHandler):
    def __init__(self, daemon):
        self.handleCommands = ["NICK"]
        self._daemon = daemon
    def handle(self, user, command):
        pass
        