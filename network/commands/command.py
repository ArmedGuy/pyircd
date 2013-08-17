import config, commands, logger

# documentation for commands here: http://www.technerd.net/irc-commands.html
accepted_commands = [
"PRIVMSG", "PASS", "NICK", "USER", "MODE", "CAP", "QUIT", "WHO", "WHOWAS", "WHOIS", 
"NAMES", "ISON", "JOIN", "PART", "MOTD", "RULES", "LUSERS", "MAP", "PING", "PONG",
"STATS", "LINKS", "ADMIN", "USERHOST", "TOPIC", "INVITE", "NOTICE", "KICK", "AWAY",
"LIST", "KNOCK", "SETNAME", "TIME", "OPER", "WALLOPS", "GLOBOPS", "CHATOPS", "LOCOPS",
"KILL", "KLINE", "UNKLINE", "ZLINE", "UNZLINE", "GLINE", "SHUN", "GZLINE", "TKLINE",
"TZLINE", "AKILL", "RAKILL", "REHASH", "RESTART", "DIE", "LAG", "SQUIT", "CONNECT",
"SAPART", "SAMODE", "RPING"]



def hostname():
    return ":%s" % config.servername
def text(data):
    return ":%s" % data
    
# Base command-builder class
class Command:
    _args = None
    def __init__():
        self._args = []
    def initServerMessage(self, cmd):
        self.arg(hostname())
        self.arg(cmd)
    def to(self, reciever):
        if hasattr(reciever, "nick"):
            self.arg(reciever.nick)
        else:
            self.arg(reciever)
    def arg(self, argument):
        if self._args == None:
            self._args = []
        try:
            self._args.append(str(argument))
        except:
            self._args.append("%s" % argument)

    # ToStuff
    def ToString(self):
        return ' '.join(self._args)
    def ToPacket(self):
        return "%s\r\n" % self.ToString()
    def ToCommand(self):
        return UserCommandString(self.ToString())


# parse incoming commands
class UserCommandString:
    valid = False
    sender = ""
    command = ""
    args = []
    def __init__(self, raw):
        self.sender = ""
        self.command = ""
        self.valid = False
        self.args = []
        blocks = raw.split(" ")
        if(raw[0] == ":"):
            self.sender = blocks[0][1:]
            blocks = blocks[1:]
        if blocks[0] in accepted_commands:
            self.command = blocks[0]
            blocks = blocks[1:]
            self.valid = True
        else:
            return
        i = 0
        for block in blocks:
            if(block[0] == ":"):
                self.args.append(" ".join(blocks[i:])[1:])
            else:
                self.args.append(block)
            i = i + 1