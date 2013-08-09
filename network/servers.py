import threading
import SocketServer
import pyircd.network.handlers


class ThreadedIrcServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    _currentDaemon = None
    def __init__(self, serveraddr, daemon):
        self._currentDaemon = daemon
        SocketServer.TCPServer.__init(serveraddr, pyircd.irc.handlers.IrcConnectionHandler)

    def finish_request(self, request, clientaddr):
        c = BaseServer.RequestHandlerClass(request, clientaddr, self.currentDaemon)
        c.handle()
    
class UDPServer(SocketServer.UDPServer):
    pass
    