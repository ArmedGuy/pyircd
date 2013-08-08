import socket, threading, thread, os, sys, time
def create(settings):
    return IrcBot(settings)
# Revision, yolo
class IrcBot:
    _settings = {}
    _debug = None
    _client = "ArmedGuys IRC Bot"
    _version = "0.5"
    _env = "Python"
    _socket = None
    # Channels the bot is in
    _channels = []
    # Message Loop
    _messageThreadRunning = True
    _messageThread = None
    # Event Queue Loop
    _queueThreadRunning = True
    _queueThread = None
    _queue = None
    def __init__(self, settings):
        self._settings = settings
        self._queue = IrcEventQueue()
        if "debug" in settings:
            self._debug = DebugLog(settings['nick'])
        
    def connect(self):
        if "host" in self._settings and "port" in self._settings:
            self._socket = socket.create_connection((self._settings['host'], self._settings['port']))
            # Register events
            self._queue.RegisterHandler(IrcEvent.PacketRecieved, self.onpacket)
            self._queue.RegisterHandler(IrcEvent.MessageRecieved, self.onmessage)
            self._queue.RegisterHandler(IrcEvent.PingRecieved, self.onping)
            # before sending, create message & queue loops
            
            self.startQueueThread() # start event queue thread
            self.startMessageThread() # start message queue thread
            
            # begin connection
            if "serverpassword" in self._settings:
                self.out("PASS %s\r\n" % self._settings['serverpassword'])
            self.out("NICK %s\r\n" % self._settings['nick'])
            self.out("USER %s %s bla :%s\r\n" % (self._settings['ident'], self._settings['host'], self._settings['realname']))
        
    def reconnect(self): # reconnect assumes events are all intact, that socket is closed and that queue thread is still running
        if self._messageThreadRunning == False and self._queueThreadRunning == True:
            self._socket = socket.create_connection((self._settings['host'], self._settings['port']))
            # before sending, create message & queue loops
            self._messageThreadRunning = True # reset msgthread state
            self.startMessageThread() # start message queue thread
            
            # begin connection
            if "serverpassword" in self._settings:
                self.out("PASS %s\r\n" % self._settings['serverpassword'])
            self.out("NICK %s\r\n" % self._settings['nick'])
            self.out("USER %s %s bla :%s\r\n" % (self._settings['ident'], self._settings['host'], self._settings['realname']))
    def startMessageThread(self):
        try:
            self._messageThread = threading.Thread(target=self.messageThread)
            self._messageThread.start()
        except:
            print "exception: %s" % str(sys.exec_info())
            
    def startQueueThread(self):
        try:
            self._queueThread = threading.Thread(target=self.queueThread)
            self._queueThread.start()
        except:
            print "exception: %s" % str(sys.exec_info())
        
    def messageThread(self):
        tempbuf = ""
        while self._messageThreadRunning == True:
            try:
                sockbuf = self._socket.recv(4096)
                if sockbuf == "": # dead connection
                    self._messageThreadRunning = False
                    self._queue.event(IrcEvent.BotLostConnection, None)
                    self._socket.close()
                    if "debug" in self._settings:
                        self._debug.write("BOT LOST CONNECTION", "Unknown reason")
                else:
                    sockbuf = tempbuf + sockbuf
                    if "\n" in sockbuf: # should always happen
                        pcks = sockbuf.split("\n") # Splits them up as full IRC Commands, anyone cut off by buffer size gets put in a temp buffer and used next loop
                        tempbuf = pcks.pop() 
                        for pck in pcks:
                            pck = pck.rstrip()
                            if "debug" in self._settings:
                                self._debug.write("GOT PACKET", pck)
                            packet = IrcPacket(pck)
                            self._queue.event(IrcEvent.PacketRecieved, packet)
            except:
                print "exception: %s\n" % str(sys.exc_info())
                self._messageThreadRunning = False
                self._socket.close()
                self._queue.event(IrcEvent.BotLostConnection, None)
                if "debug" in self._settings:
                    self._debug.write("MESSAGETHREAD EXCEPTION", str(sys.exc_info()))
                
        
    def queueThread(self):
        while self._queueThreadRunning == True:
            next = self._queue.next()
            self._queue.Handle(next)
            time.sleep(0.001)
            
######################################### EVENT HANDLER HANDLING HANDLE HANDLING HANDLE HAND #############
    def RegisterEventHandler(self, type, handler):
        self._queue.RegisterHandler(type, handler)
        
    def UnregisterEventHandler(self, type, handler):
        self._queue.UnregisterHandler(type, handler)
            
######################################### EVENT HANDLING #################################################

    def onpacket(self, type, data):
        if type == IrcEvent.PacketRecieved:
            if data.command == "PING":
                self._queue.event(IrcEvent.PingRecieved, data.message)
            if data.command == "ERROR":
                self._queue.event(IrcEvent.IrcError, data)
            else: # can't say this is the best implementation, but hey, it woerkz
                self._queue.event(IrcEvent.MessageRecieved, data)
            
    def onping(self, type, data):
        if type == IrcEvent.PingRecieved:
            self.out("PONG :%s\r\n" % data)
            
    def onmessage(self, type, data):
        # print "Recieved message of type: %s from %s" % (data.command, data.sender)
        if type == IrcEvent.MessageRecieved:
            if data.command == "PRIVMSG":
                self._queue.event(IrcEvent.PrivmsgRecieved, data)
                #print "privmsg reciever: %s" % data.params[0]
                if data.params[0][0] != "#":
                    self._queue.event(IrcEvent.QueryRecieved, data)
                else:
                    self._queue.event(IrcEvent.ChanmsgRecieved, data)
                    
            if data.command == "NOTICE":
                self._queue.event(IrcEvent.NoticeRecieved, data)
                
            if data.command == "TOPIC":
                self._queue.event(IrcEvent.TopicChanged, data)
                
            if data.command == "JOIN":
                self._queue.event(IrcEvent.UserJoined, data)
            
            if data.command == "PART":
                self._queue.event(IrcEvent.UserLeft, data)
                
            if data.command == "NICK":
                self._queue.event(IrcEvent.NickChanged, data)
                
######################################### BOT CONTROL ####################################################
    def exit(self, message):
        self.out("QUIT :%s" % message)
        self._queueThreadRunning = False
        self._messageThreadRunning = False
        self._socket.close()
        
    # basic send types
    def out(self, data):
        if len(data) == 0: return
        if "debug" in self._settings:
            self._debug.write("SENT PACKET", data.rstrip())
        if "\r\n" not in data:
            data = data + "\r\n"
        if self._socket:
            self._socket.send(data)
            
    def msg(self, target, message):
        self.out("PRIVMSG %s :%s\r\n" % (target,message))
        
    def notice(self, target, message):
        self.out("NOTICE %s :%s\r\n" % (target, message))
    
    # Channel stuff
    def join(self, channel):
        self._channels.append(channel)
        self.out("JOIN :%s\r\n" % channel)
        
    def leave(self, channel):
        self.out("PART :%s\r\n" % channel)
        try:
            self._channels.remove(channel)
        except:
            pass
        
    # Other stuff
    def status(self, status):
        if status == "":
            self.out("NICK %s\r\n" % self._settings['nick'])
        else:
            self.out("NICK %s|%s\r\n" % (self._settings['nick'], status))

########################### EVENT QUEUE #########################################
class IrcEvent:
    PacketRecieved = 0
    MessageRecieved = 1
    PingRecieved = 2
    NoticeRecieved = 3
    PrivmsgRecieved = 4
    ChanmsgRecieved = 5
    QueryRecieved = 6
    TopicChanged = 7
    UserJoined = 8
    UserLeft = 9
    NickChanged = 10
    BotLostConnection = 11
    IrcError = 12
    

class IrcEventQueue:
    EventHandlers = {}
    next = None
    _queue = None
    def RegisterHandler(self, event, handler):
        if event in self.EventHandlers:
            self.EventHandlers[event].append(handler)
        else:
            self.EventHandlers[event] = [handler]
    def UnregisterHandler(self, event, handler):
        if event in IrcEventQueue.EventHandlers:
            try:
                self.EventHandlers[event].remove(handler)
            except:
                pass
    def Handle(self, event):
        if event[0] in self.EventHandlers:
            for e in self.EventHandlers[event[0]]:
                e(event[0], event[1])
    
    # Constructor
    def __init__(self):
        self._queue = self.ThreadsafeQueue()
        self.next = self._queue.get
        
    def event(self, type, data): # queue an event
        self._queue.enqueue((type, data))

    class ThreadsafeQueue:
        def __init__(self):
            self._eventList = []
            self._newEventCondition = threading.Condition()
            
        def enqueue(self, event): # adds an event to the queue
            with self._newEventCondition:
                self._eventList.append(event)
                self._newEventCondition.notify()
                
        def empty(self): # returns True if list is empty
            with self._newEventCondition:
                return len(self._eventList) == 0
        
        def get(self):
            with self._newEventCondition:
                while self.empty():
                    self._newEventCondition.wait()
                return self._eventList.pop(0)

########################### BOT COMPONENTS ######################################
class IrcPacket:
    sender = ""
    command = "" # command, numerical or text
    params = None # any numerical reply params
    message = "" # after "last" :
    def __init__(self, buf):
        self.params = []
        if buf[0] == ":": # events generally
            self.sender = ""
            if ":" in buf[1:]:
                d = buf[1:].split(":",1)
                cm = d[0].strip()
                if " " in cm: # must probably always happen, else will "never" happen
                    cmpar = cm.split(" ")
                    self.sender = cmpar[0]
                    self.command = cmpar[1]
                    self.params = cmpar[2:]
                else:
                    self.command = cm
                self.message = d[1]
            else:
                cm = buf[1:].strip()
                if " " in cm: # must probably always happen, else will "never" happen
                    cmpar = cm.split(" ")
                    self.sender = cmpar[0]
                    self.command = cmpar[1]
                    self.params = cmpar[2:]
                else:
                    self.command = cm
        else:
            self.sender = None
            if ":" in buf:
                d = buf.split(":",1)
                cm = d[0].strip()
                if " " in cm: # must probably always happen, else will "never" happen
                    cmpar = cm.split(" ")
                    self.command = cmpar[0]
                    self.params = cmpar[1:]
                else:
                    self.command = cm
                self.message = d[1]
            else:
                cm = buf.strip()
                if " " in cm:  # must probably always happen, else will "never" happen
                    cmpar = cm.split(" ")
                    self.command = cmpar[0]
                    self.params = cmpar[1:]
                else:
                    self.command = cm
                
class IrcUser:
    nick = ""
    ident = ""
    host = ""
    def __init__(self, userstring):
        if "!" in userstring:
            d = userstring.split('!')
            self.nick = d[0]
            d = d[1].split("@")
            self.ident = d[0]
            self.host = d[1]
         
class DebugLog:
    f = None
    def __init__(self, prefix):
        self.f = open("%s_irc.log" % prefix, "w")
    
    def write(self, prefix, data):
        self.f.write("[%s] [%s]: %s\r\n" % (time.time(), prefix, data))
        self.f.flush()
        
        
############# STANDARD BOT ROUTINES ##############
class StandardBotRoutines:
    _bot = None
    _botSettings = None
    
    # channels to join
    _channels = []
    
    # nickserv password to use
    _nickservpassword = None
    def __init__(self, bot, settings):
        self._bot = bot
        self._botSettings = settings
        self._bot.RegisterEventHandler(IrcEvent.MessageRecieved, self.onMsgRecieved)
    
    # join channel and nickserv auth
    def queueJoinChannels(self, channels):
        self._channels = channels
        
    def queueNickServAuth(self, password):
        self._nickservpassword = password
    
    # automatic reconnect after internet connection issue
    def autoReconnect(self):
        self._bot.RegisterEventHandler(IrcEvent.BotLostConnection, self.onLostConn)
        
    def onLostConn(self, type, data):
        time.sleep(5)
        print "reconnecting..."
        self._bot.reconnect()
    
    # handles join and nickserv pw
    def onMsgRecieved(self, type, data):
        if type == IrcEvent.MessageRecieved and data.command == "376": # end MOTD, auth w/ NickServ and join channels
            if self._nickservpassword != None:
                self._bot.msg("NickServ", "IDENTIFY %s" % self._nickservpassword)
            for channel in self._channels:
                self._bot.join(channel)
        
############# TEST CODE ###############

if __name__ == "__main__":   
    def user_joined(data1, data2):
        bot.notice("#Pie-Studios", "Travis CI build currently running!")
        bot.exit("Tests complete!")
    settings = {
        'host': "127.0.0.1",
        'port': 6667,
        'nick': 'pyircbot',
        'ident': 'pyircbot',
        'realname': 'TheLeagueSpecialist',
        'debug': False
    }
    bot = create(settings)
    standard = StandardBotRoutines(bot, settings)
    standard.queueJoinChannels(["#Pie-Studios"])
    
    bot.connect()