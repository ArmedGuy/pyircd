import network.handlers, network.servers, config, threading


class Daemon:
    serverName = ""
    host = ""
    listenPorts = ()
    _server = None
    _serverThread = None
    pass

class MasterDaemon(Daemon):
    def __init__(self):
        pass
        
class NodeDaemon(Daemon):
    def __init__(self, host, port):
        self.serverName = config.servername
        self.host = host
        self.listenPort = port
    
    def start(self):
        self._server = network.servers.ThreadedTCPServer((self.host, self.listenPort), network.handlers.IRCRequestHandler)
        self._serverThread = threading.Thread(target=self._server.serve_forever)
        self._serverThread.daemon = True
        
        self._serverThread.start()
        
        