import SocketServer, logger

class IRCRequestHandler(SocketServer.BaseRequestHandler):
    _alive = True
    def handle(self):
        tempbuf = ""
        while _alive:
            try:
                sockbuf = self.request.recv(4096)
                if sockbuf == "": # dead connection
                    _alive = False
                    self.request.close()
                else:
                    sockbuf = tempbuf + sockbuf
                    if "\n" in sockbuf: # should always happen
                        pcks = sockbuf.split("\n") # Splits them up as full IRC Commands, anyone cut off by buffer size gets put in a temp buffer and used next loop
                        tempbuf = pcks.pop() 
                        for pck in pcks:
                            pck = pck.rstrip()
                            packet = IrcPacket(pck)