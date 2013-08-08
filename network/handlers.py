import SocketServer, time, logger, config, sys
from irc.commands.command import UserCommandString
from irc.handlers import *

class InternalRequestHandler(SocketServer.BaseRequestHandler):
    pass

class IRCConnectionHandler(SocketServer.BaseRequestHandler):
    _alive = True
    _authed = True
    _owner = None
    def handle(self):
        #self.request.setblocking(False)
        tempbuf = ""
        if config.serverpassword:
            self._authed = False
        while self._alive:
            try:
                sockbuf = self.request.recv(4096)
                if sockbuf == "": # dead connection
                    self._alive = False
                    self.request.close()
                else:
                    sockbuf = tempbuf + sockbuf
                    if "\n" in sockbuf: # should always happen
                        pcks = sockbuf.split("\n") # Splits them up as full IRC Commands, anyone cut off by buffer size gets put in a temp buffer and used next loop
                        tempbuf = pcks.pop() 
                        for pck in pcks:
                            pck = pck.rstrip()
                            self.process(pck)
            except:
                for var in sys.exc_info():
                    logger.error(str("%s" % var).strip())
                time.sleep(0.01)
                
    def process(self, packet):
        cmd = UserCommandString(packet)
        if not cmd.valid:
            return
        logger.debug("got %s" % cmd.command)
        
        