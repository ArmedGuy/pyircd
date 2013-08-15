user_modes = "CDFGNRSUWXabcdfgijklnopqrsuwxyz"
channel_modes = "BIMNORSabcehiklmnopqstvz"

import config, re


class ChannelModes:
    _channel = ""
    _listmodes = None
    _valuemodes = None
    _flagmodes = None
    def __init__(self, channel):
        self._channel = channel
        self._listmodes = {
            "b": ListMode("b", True), # ban includes
            "e": ListMode("e", True), # ban excludes
            "I": ListMode("I", True), # cant be invited
            "o": ListMode("o"), # channel op
            "v": ListMode("v"), # channel voice
            "a": ListMode("a"), # channel prot/adm
            "h": ListMode("h"), # channel half-op
            "q": ListMode("q")  # channel owners
        }

        self._valuemodes = {
            "l": ValueMode("l", 75), # max users in channel
            "L": ValueMode("L", None), # overflow channel
            "k": ValueMode("k", None) # passworded channel
        }

        self._flagmodes = {
            "p": False, #  private channel
            "s": False, # secret channel
            "i": False, # invite only channel
            "m": False, # moderated, only qaohv can talk
            "n": False, # No outside channel messages
            "t": False, # only chanops may set topic
            "r": False, # chan is registered
            "R": False, # need regged nickname to join
            "c": False, # ColorBlock(unicode & CTCP still allowed)
            "O": False, # IRCop only channel
            "A": False, # Admin only channel
            "K": False, # no knocks
            "V": False, # no invites
            "H": False, # no +I users may join
            "N": False, # no nickname changes
            "G": False, # G rated channel
            "u": False, # /names /who only shows @'s
            "C": False, # no CTCPs allowed
            "S": False, # TLS peeps only
            "z": False, # persistant channel
            "Q": False  # peace mode, no kicks except U:Lines, bans can be made
        }

    def handle(self, modes):
        result = self.parse(modes)
        print "add"
        for v in result[0]:
            if len(v) == 2:
                print "%s = %s" % (v)
            else:
                print v

        print "remove"
        for v in result[1]:
            if len(v) == 2:
                print "%s = %s" % (v)
            else:
                print v

    def parse(self, raw):
        data = raw.split(" ")
        add = True
        addlist = []
        removelist = []
        i = 0
        for c in data[0]:
            if c == "+":
                add = True
                continue
            if c == "-":
                add = False
                continue
            if add == True:
                if c in self._valuemodes or c in self._listmodes:
                    addlist.append((c, data[i+1]))
                    i = i + 1
                else:
                    addlist.append(c)
            else:
                if c in self._valuemodes or c in self._listmodes:
                    removelist.append((c, data[i+1]))
                    i = i + 1
                else:
                    removelist.append(c)
            if i > 3:
                break
        return (addlist, removelist)


class ValueMode:
    _type = ""
    _value = None
    def __init__(self, type, defaultValue):
        self._type = type
        self.set(defaultValue)

    def get(self):
        return self._value
    
    def set(self, value):
        self._value = value

class ListMode: # 
    _list = None
    _type = ""
    _useRegex = False
    def __init__(self, type, useRegex=False):
        self._list = []
        self._type = type
        self._useRegex = useRegex
    def add(self, item):
        if len(self._list) >= 250:
            return False
        else:
            if self._useRegex:
                self._list.append((item, re.compile(item.replace(".", "\\.").replace("*", ".*"))))
            else:
                self._list.append(item)
            return True
    def remove(self, item):
        try:
            if self._useRegex:
                i = 0
                for litem in self._list:
                    if litem[0] == item:
                        self._list.pop(i)
                        return True
                    i = i + 1
                return False
            else:
                self._list.remove(item)
            return True
        except:
            return False

    def match(self, subject):
        if not self._useRegex:
            try:
                self._list.index(subject)
                return True
            except:
                return False
        else:
            for litem in self._list:
                if litem[1].match(subject) != None:
                    return True
            return False

