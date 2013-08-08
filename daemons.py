import network.handlers, network.servers, config, threading


class Daemon:
    serverName = ""
    host = ""
    listenPorts = ()
    _server = None
    _serverThread = None
    
    def send(self, to, data, viaSocket="irc"):
        if "internal" in self._server:
            self._server[viaSocket].sendto(data, to)
        else:
            self._server.sendto(data, to)

class MasterDaemon(Daemon):
    def __init__(self, host, port):
        self.serverName = config.servername
        self.host = host
        self.listenPort = port
        
    def self(self):
        self._server = network.servers.UDPServer((self.host, self.listenPort), network.handlers.InternalRequestHandler)
        self._serverThread = threading.Thread(target=self._server.serve_forever)
        self._serverThread.daemon = True
        
        self._serverThread.start()
        
class NodeDaemon(Daemon):
    def __init__(self, host, port):
        self.serverName = config.servername
        self.host = host
        self.listenPort = port
        self._serverThread = {}
        self._server = {}
    
    def start(self):
        self._server["internal"] = network.servers.UDPServer((self.host, self.listenPort), network.handlers.InternalRequestHandler)
        self._serverThread["internal"] = threading.Thread(target=self._server["internal"].serve_forever)
        self._serverThread["internal"].daemon = True
        
        self._serverThread["internal"].start()
        
        if config.dumb:
            # download configuration from master server
        
        self._server["irc"] = network.servers.ThreadedTCPServer((self.host, self.listenPort), network.handlers.IRCRequestHandler)
        self._serverThread["irc"] = threading.Thread(target=self._server["irc"].serve_forever)
        self._serverThread["irc"].daemon = True
    
        self._serverThread["irc"].start()
        
        
