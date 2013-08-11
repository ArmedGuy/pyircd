import threading
import SocketServer
import network.handlers


class ThreadedIrcServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon = None
    def __init__(self, serveraddr, daemon):
        self.daemon = daemon
        SocketServer.TCPServer.__init__(self, serveraddr, network.handlers.IrcConnectionHandler)
    
class UDPServer(SocketServer.UDPServer):
    pass
    