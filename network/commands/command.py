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
    _len = 0
    def __init__():
        self._args = []
        self._len = 0
    def init(self, cmd):
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
        a = ""
        try:
            a = str(argument)
        except:
            a = "%s" % argument
        self._args.append(a)
        self._len = self._len + len(a) + 1

    # ToStuff
    def __len__(self):
        return self._len - 1
    def __str__(self):
        return self.ToString()

    def ToString(self):
        return ' '.join(self._args)
    def ToPacket(self):
        return "%s\r\n" % self
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
            if len(block) != 0:
                if block[0] == ":":
                    self.args.append(" ".join(blocks[i:])[1:])
                    break
                else:
                    self.args.append(block)
            i = i + 1