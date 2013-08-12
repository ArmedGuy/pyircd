import SocketServer, time, logger, config, sys, socket
from network.commands.command import UserCommandString
from irc.handlers import *

class InternalRequestHandler(SocketServer.BaseRequestHandler):
    pass

class IrcConnectionHandler(SocketServer.BaseRequestHandler):
    alive = True
    daemon = None
    user = None
    cache = None # when requests require several commands
    def __init__(self, request, client_address, server):
        self.daemon = server.daemon
        self.cache = {}
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        tempbuf = ""
        while self.alive:
            try:
                sockbuf = self.request.recv(4096)
                if sockbuf == "": # dead connection
                    self.alive = False
                    self.request.close()
                else:
                    sockbuf = tempbuf + sockbuf
                    if "\n" in sockbuf: # should always happen
                        pcks = sockbuf.split("\n") # Splits them up as full IRC Commands, anyone cut off by buffer size gets put in a temp buffer and used next loop
                        tempbuf = pcks.pop() 
                        for pck in pcks:
                            pck = pck.rstrip()
                            self.process(pck)
            except socket.error:
                self.alive = False
            except:
                for var in sys.exc_info():
                    logger.error(str("%s" % var).strip())
                time.sleep(0.01)
                
    def process(self, packet):
        if hasattr(config, 'debug'):
            logger.debug(packet, True, False)
        cmd = UserCommandString(packet)
        if not cmd.valid:
            self.alive = False
            self.request.close()
            return
        self.daemon.delegateRequest(self, cmd)
        