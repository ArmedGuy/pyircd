import network.handlers, network.servers, config, threading, irc.handlers

class Daemon:
    serverName = ""
    host = ""
    listenPorts = ()
    _server = None
    _serverThread = None

    _commandHandlers = None

    # two most important arrays =D (needs to be thread safe)
    users = []
    channels = []
    
    def send(self, to, data):
        if "internal" in self._server:
            self._server["internal"].sendto(data, to)
        else:
            self._server.sendto(data, to)

class MasterDaemon(Daemon):
    def __init__(self, host, port):
        self._commandHandlers = irc.handlers.getHandlers(self)
        self.serverName = config.servername
        self.host = host
        self.listenPort = port
        
    def start(self):
        self._server = network.servers.UDPServer((self.host, self.listenPort), network.handlers.InternalRequestHandler)
        self._serverThread = threading.Thread(target=self._server.serve_forever)
        self._serverThread.daemon = True
        
        self._serverThread.start()
        
class NodeDaemon(Daemon):
    netstats = None
    def __init__(self, host, port):

        self._commandHandlers = irc.handlers.getHandlers(self)

        self.serverName = config.servername
        self.host = host
        self.listenPort = port
        self._serverThread = {}
        self._server = {}

        self.netstats = network.network_stats(self)
    
    def start(self):
        self._server["internal"] = network.servers.UDPServer((self.host, self.listenPort), network.handlers.InternalRequestHandler)
        self._serverThread["internal"] = threading.Thread(target=self._server["internal"].serve_forever)
        self._serverThread["internal"].daemon = True
        
        self._serverThread["internal"].start()
        
        if config.dumb:
            pass # download configuration from master server
        
        self._server["irc"] = network.servers.ThreadedIrcServer((self.host, self.listenPort), self)
        self._serverThread["irc"] = threading.Thread(target=self._server["irc"].serve_forever)
        self._serverThread["irc"].daemon = True
    
        self._serverThread["irc"].start()

    def delegateRequest(self, handler, cmd):
        for hnd in self._commandHandlers:
            if cmd.command in hnd.handlesCommands:
                hnd.handle(handler, cmd)
        
        
