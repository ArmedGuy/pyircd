user_modes = "CDFGNRSUWXabcdfgijklnopqrsuwxyz"
channel_modes = "ACGHIKLNOQRSVabcefhiklmnopqrstuvz"
channelmodes_with_params = "befIovahqlLk"

import config, re, threading, time
from irc.commands.events import MODE
from irc.commands.replies import *
from irc.commands.errors import *

class ChannelModes:
    _modelock = None
    _channel = ""
    _listmodes = {}
    _valuemodes = {}
    _flagmodes = {}

    def __init__(self, channel):
        self._modelock = threading.Lock()
        self._channel = channel
        self._listmodes = {
            "b": BanListMode(), # ban includes
            "e": ListMode("e", True), # ban excludes
            "I": ListMode("I", True), # cant be invited
            "o": ListMode("o"), # channel op
            "v": ListMode("v"), # channel voice
            "a": ListMode("a"), # channel prot/adm
            "h": ListMode("h"), # channel half-op
            "q": ListMode("q")  # channel owners
        }

        self._valuemodes = {
            "l": ValueMode("l", None), # max users in channel
            "L": ValueMode("L", None), # overflow channel
            "k": ValueMode("k", None), # passworded channel
            "f": ValueMode("f", None) # against floods
        }

        self._flagmodes = {
            "p": False, #  private channel
            "s": False, # secret channel
            "i": False, # invite only channel
            "m": False, # moderated, only qaohv can talk
            "M": False, # reg-moderated, only +r's can talk
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
            "z": False, # TLS peeps
            "Q": False  # peace mode, no kicks except U:Lines, bans can be made
        }
    def modes(self): # temporary
        modes = []
        for m in self._listmodes:
            modes.append(m)
        for m in self._flagmodes:
            modes.append(m)
        for m in self._valuemodes:
            modes.append(m)
        modes.sort()
        return "".join(modes)

    def list(self, forCmd=False):
        keys = []
        for k in self._flagmodes.keys():
            if self._flagmodes[k] == True:
                keys.append(k)
        if not forCmd:
            for k in self._valuemodes.keys():
                if self._valuemodes[k].isset():
                    keys.append(k)
        return "".join(keys)

    def match(self, mode, match=""):
        if mode in self._flagmodes:
            return self._flagmodes[mode]
        if mode in self._valuemodes:
            return self._valuemodes[mode].match(match)
        if mode in self._listmodes:
            return self._listmodes[mode].match(match)

    def matchany(self, modes, matches=None):
        i = 0
        for mode in modes:
            if mode in channelmodes_with_params:
                if matches != None and self.match(mode, matches[i]):
                    return True
                i = i + 1
            else:
                if self.match(mode):
                    return True
        return False

    def matchall(self, modes, matches=None):
        i = 0
        for mode in modes:
            if mode in channelmodes_with_params:
                if matches != None and not self.match(mode, matches[i]):
                    return False
                i = i + 1
            else:
                if not self.match(mode):
                    return False
        return True

    def set(self, setter, modes):
        result = self.parse(setter, modes)
        if not result:
            return False
        set = []
        set.append([])
        set.append([])
        origin = ""
        if hasattr(setter, 'nick'):
            origin = setter.nick
        else:
            origin = setter
        # add
        for add in result[0]:
            if len(add) != 2:
                if self.hasAccess(setter, add):
                    res = self.addsingle(setter, add) 
                    if(res == 0):
                        set[0].append(add)
                    if(res == 1):
                        # not found, or is server while listing
                        pass
                    if (res == 2):
                        break # is list
                else:
                    pass # no access
            else:
                if self.hasAccess(setter, add[0]):
                    if(self.additem(setter, add[0], add[1])):
                        set[0].append(add)
                    else:
                        pass # not found or list is full
                else:
                    pass # no access
        # remove
        for rem in result[1]:
            if len(rem) != 2:
                if self.hasAccess(setter, rem):
                    if self.remsingle(setter, rem):
                        set[1].append(rem)
                    else:
                        pass # failed to remove, noexistant
                else:
                    pass # no access
            else:
                if self.hasAccess(setter, rem[0]):
                    if self.remitem(setter, rem[0], rem[1]):
                        set[1].append(rem) # successfully removed from list
                    else:
                        pass # failed to add to listremove from list
                    continue
                else:
                    pass # no access

        # send channel notice
        setModes = ""
        args = []
        tmp = []
        if len(set[0]) != 0:
            for a in set[0]:
                if len(a) == 2:
                    tmp.append(a[0])
                    args.append(a[1])
                else:
                    tmp.append(a)
            setModes = "+%s" % "".join(tmp)
            tmp = []
        if len(set[1]) != 0:
            for r in set[1]:
                if len(r) == 2:
                    tmp.append(r[0])
                    args.append(r[1])
                else:
                    tmp.append(a)
            setModes = "%s-%s" % (setModes, "".join(tmp))
        if setModes != "":
            setModes = "%s %s" % (setModes, " ".join(args))
            if hasattr(setter, 'hostmask'):
                self._channel.send(MODE(setter.hostmask, self._channel.name, setModes))
            else:
                self._channel.send(MODE(setter, self._channel.name, setModes))
    
    # add stuff
    def addsingle(self, setter, key): # + version
        if key in self._listmodes:
            if key in "b":
                for i in self._listmodes["b"].list():
                    setter.send(RPL_BANLIST(setter, self._channel.name, i[0], i[1], i[2]))
                setter.send(RPL_ENDOFBANLIST(setter, self._channel.name))
                return 2
            else:
                return 1
        if key in self._flagmodes:
            with self._modelock:
                self._flagmodes[key] = True
            return 0
        else:
            return 1

    def additem(self, setter, key, value):
        origin = ""
        if hasattr(setter, 'nick'):
            origin = setter.nick
        else:
            origin = setter
        if key in self._listmodes:
            with self._modelock:
                if key in "b":
                    return self._listmodes[key].add(value, origin)
                else:
                    return self._listmodes[key].add(value)
        else:
            return self.setvalue(key, value)

    # remove stuff
    def remsingle(self, setter, key):
        if key in self._flagmodes:
            with self._modelock:
                self._flagmodes[key] = False
            return True
        if key in self._valuemodes:
            with self._modelock:
                self._valuemodes[key].default()
            return True
        return False

    def remitem(self, setter, key, value):
        if key in self._listmodes:
            with self._modelock:
                return self._listmodes[key].remove(value)
        if key in self._valuemodes:
            if self._valuemodes[key].match(value):
                with self._modelock:
                    return self._valuemodes[key].default(value)
        return False
    # get and set vaules
    def setvalue(self, key, value):
        if key in self._valuemodes:
            with self._modelock:
                self._valuemodes[key].set(value)
            return True
        else:
            return False

    def getvalue(self, key):
        if key in self._valuemodes:
            return self._valuemodes[key]
        else:
            return None
    
    # parse modes
    def parse(self, setter, raw):
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
                if (c in self._valuemodes or c in self._listmodes) and len(data) > 1:
                    try:
                        addlist.append((c, data[i+1]))
                    except IndexError:
                        if hasattr(setter, 'nick'):
                            setter.send(ERR_NEEDMOREPARAMS(setter, "MODE", "+%s" % c))
                        return False
                    i = i + 1
                else:
                    if c in self._valuemodes or c not in "beI":
                        if hasattr(setter, 'nick'):
                            setter.send(ERR_NEEDMOREPARAMS(setter, "MODE", "+%s" % c))
                        return False

                    addlist.append(c)
                    if c in "beI":
                        break
            else:
                if c in self._valuemodes or c in self._listmodes:
                    try:
                        removelist.append((c, data[i+1]))
                    except IndexError:
                        if hasattr(setter, 'nick'):
                            setter.send(ERR_NEEDMOREPARAMS(setter, "MODE", "-%s" % c))
                        return False
                    i = i + 1
                else:
                    removelist.append(c)
            if i > 3:
                break
        return (addlist, removelist)

    def hasAccess(self, setter, mode):
        if hasattr(setter, 'nick'):
            # stuff opers and services can set
            user = setter

            if mode in "AOr-aLqu-cCfGhKlMNopQRsVHz-beiIkmntv" and user.modes.matchany("So"):
                return True

            # stuff owner can set
            if mode in "aLqu-cCfGhKlMNopQRsVHz-beiIkmntv" and self.match("q", (user.nick)):
                return True

            # stuff a and o can set
            if mode in "cCfGhKlMNopQRsVHz-beiIkmntv" and self.matchany("ao", (user.nick, user.nick)):
                return True

            # stuff half-op can set
            if mode in "beiIkmntv" and self.match("h", (user.nick)):
                return True
            return False
        else:  # for now, no nick = es server
            return True

class UserModes:
    _modelock = None
    _modes = None

    _opermodes = None
    _user = None
    def __init__(self, user):
        self._modelock = threading.Lock()
        self._user = user
        self._modes = {
            "O": False, # local IRC Op
            "o": False, # global IRC op
            "i": False, # invisible
            "w": False, # can read wallop messages
            "g": False, # can read/sen to globops and locops
            "h": False, # available for help
            "s": False, # can see server notices
            "k": False, # can see all the kills which were executed
            "S": False, # for services, protects them
            "a": False, # is a services admin
            "A": False, # is a server admin
            "N": False, # is a network admin
            "T": False, # is a tech admin
            "C": False, # is a Co-Admin
            "c": False, # see all connects/disconnects on local server
            "f": False, # listen to flood alerts from server
            "r": False, # nickname registered
            "x": False, # hides hostname
            "e": False, # can listen to server messages sent to +e users
            "b": False, # can read and sent to chatops
            "W": False, # (IRCops only) lets you see when people whois you
            "q": False, # (services admins only) Only U:lines can lick you
            "B": False, # bot marker
            "F": False, # lets you recieve far connect notices and local notices
            "I": False, # makes you invisible in channels
            "H": False, # hide IRCop status in who and whois
            "d": False, # deaf, cant recieve channel messages
            "t": False, # says you are using a vhost
            "G": False, # G-rated client, filters out bad words
            "z": False, # Marks the client as being on secure connection
        }
    def set(self, setter, modes):
        result = self.parse(modes)
        set = []
        set.append([])
        set.append([])
        # add
        for add in result[0]:
            if self.hasAccess(setter, add):
                with self._modelock:
                    self._modes[add] = True
                set[0].append(add)
            else:
                pass # no access
        for rem in result[1]:
            if self.hasAccess(setter, rem):
                with self._modelock:
                    self._modes[rem] = False
                set[1].append(rem)
            else:
                pass # no access

        # compile message to send to user
        setModes = ""
        if len(set[0]) > 0:
            setModes = "+%s" % "".join(set[0])
        if len(set[1]) > 0:
            setModes = "%s-%s" % (setModes, "".join(set[0]))

        if hasattr(setter, 'hostmask'):
            self._user.send(MODE(setter.hostmask, self._user.nick, setModes))
        else:
            self._user.send(MODE(setter, self._user.nick, setModes))

    def parse(self, raw):
        add = True
        addlist = []
        removelist = []
        for c in raw:
            if c == "+":
                add = True
                continue
            if c == "-":
                add = False
                continue
            if add == True:
                addlist.append(c)
            else:
                removelist.append(c)
        return (addlist, removelist)

    def match(self, mode):
        try:
            return self._modes[mode]
        except:
            return False

    def matchall(self, modes):
        for m in modes:
            if not self.match(m):
                return False
        return True

    def matchany(self, modes):
        for m in modes:
            if self.match(m):
                return True
        return False

    def list(self):
        keys = []
        for key in self._modes.keys():
            if self._modes[key] == True:
                keys.append(key)
        return "".join(keys)

    def hasAccess(self, setter, mode): # TODO: fix this, properly
        return True # for now

        if hasattr(setter, 'nick'):
            if mode in "OowghskSaANTCcfrxebWqBFIHtGz" and setter.modes.matchany("oS"):
                pass
        else: # for now, a server
            return True




class ValueMode:
    _type = ""
    _value = None
    _defValue = None
    def __init__(self, type, defaultValue):
        self._type = type
        self._defValue = defaultValue
        self.set(defaultValue)

    def get(self):
        return self._value
    
    def set(self, value):
        self._value = value

    def match(self, match):
        return (self._value == match)
    
    def default(self):
        self._value = self._defValue
        return True
    
    def isset(self):
        return (self._value != self._defValue)

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
    def list(self):
        tmp = []
        if not self._useRegex:
            return list
        else:
            for i in self._list:
                tmp.append(i[0])
            return tmp

class BanListMode(ListMode):
    _banListInfo = {}
    def __init__(self):
        self._banListInfo = {}
        ListMode.__init__(self, 'b', True)

    def add(self, item, nick):
        self._banListInfo[item] = (nick, int(time.time()))
        return ListMode.add(self, item)
    def remove(self, item):
        try:
            self._banListInfo.pop(item)
        except:
            pass
        return ListMode.remove(self, item)

    def list(self):
        tmp = []
        for key in self._banListInfo.keys():
            tmp.append((key, self._banListInfo[key][0], self._banListInfo[key][1]))
        return tmp