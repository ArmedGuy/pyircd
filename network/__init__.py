import irc.commands, network.handlers, network.servers, socket, time, md5, config
from irc.commands.events import NOTICE
def generateUserHostname(ip):
    if "." in ip:
        parts = ip.split(".")
        parts[0] = md5.new(str(parts[0])).hexdigest()[0:6].upper()
        parts[1] = md5.new(str(parts[1])).hexdigest()[0:6].upper()
        parts[2] = md5.new(str(parts[2])).hexdigest()[0:6].upper()
        parts[3] = "IP"
        return ".".join(parts)
    return "unknown.host"

def getUserHostname(con): #TODO: mask part of the hostname
    time = socket.getdefaulttimeout()
    socket.setdefaulttimeout(1)
    real_hostname = ""
    hostname = ""
    try:
        ip = con.getpeername()[0]

        con.send(NOTICE(config.servername, "AUTH", "*** Looking up hostname").ToPacket())
        h = socket.gethostbyaddr(ip)
        socket.setdefaulttimeout(time)
        con.send(NOTICE(config.servername, "AUTH", "*** Found your hostname").ToPacket())
        real_hostname = h[0]
        hostname = real_hostname
        if "." in real_hostname:
            parts = real_hostname.split(".")
            if len(parts) > 3:
                parts[0] = "mask-%d" % int(time.time())
                hostname = ".".join(parts)
            else:
                hostname = generateUserHostname(ip)
        else:
            hostname = generateUserHostname(ip)

    except:
        socket.setdefaulttimeout(time)
        con.send(NOTICE(config.servername, "AUTH", "*** Hostname not found").ToPacket())
        hostname = generateUserHostname(ip)
        real_hostname = ip

    finally:
        con.send(NOTICE(config.servername, "AUTH", "*** Your hostname is masked (%s)" % real_hostname).ToPacket())
        return (hostname,real_hostname)


class network_stats:

    _daemon = None
    def __init__(self, daemon):
        self._daemon = daemon

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