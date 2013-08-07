import threading
import SocketServer


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
    
class UDPServer(SocketServer.UDPServer):
    pass
    