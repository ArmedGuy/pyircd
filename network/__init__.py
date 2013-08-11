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
