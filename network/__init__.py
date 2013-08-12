import network.commands, network.handlers, network.servers

import socket
def getUserHostname(ip): #TODO: mask part of the hostname
    time = socket.getdefaulttimeout()
    socket.setdefaulttimeout(1)
    try:
        h = socket.gethostbyaddr(ip)
        socket.setdefaulttimeout(time)
        return h[0]
    except:
        socket.setdefaulttimeout(time)
        return "unknown.host"


class network_stats:

    # global stuff

    def _get_global_users(self):
        return 0
    globalusers = property(_get_global_users)

    def _get_global_invisible(self):
        return 0
    globalinvisible = property(_get_global_invisible)

    def _get_global_opers(self):
        return 0
    globalopers = property(_get_global_opers)

    def _get_global_channels(self):
        return 0
    globalchans = property(_get_global_channels)

    def _get_global_servers(self):
        return 0
    globalservers = property(_get_global_servers)

    def _get_global_maxclients(self):
        return 0
    globalmaxclients = property(_get_global_maxclients)


    # local stuff

    def _get_local_users(self):
        return 0
    localusers = property(_get_local_users)

    def _get_local_opers(self):
        return 0
    localopers = property(_get_local_opers)

    def _get_local_servers(self):
        return 0
    localservers = property(_get_local_servers)

netstats = network_stats()
