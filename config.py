version = "0.1-debug-test"

dumb = False
type =  "node" # can be:
"""
    * "node" - regular node that connects to a master
    * "vnode" - "virtual" node that shares servername with other vnodes(physical hostnames can differ)
    * "master" - master that handles nodes and vnodes, and syncs with other masters
    * "master-node" - both a master and a node
"""

servername = ".pie-studios.com" # unique servername for a network, starting with a "."(dot) will prefix the string with the underlying OS hostname
serverpassword = None

host = "0.0.0.0" # host that this master/node will listen on
listenports = (6667) # TCP ports to listen on as node, UDP ports to listen on as master
masterserver = ("server.pie-studios.com", 12000) # if node, connection to a master server; if master, connection to another master server, highest master must have this as None
maxclients = 256 # max clients per daemon/port

log_file = "console.log"
motd_file = "motd.txt" # file containing the message of the day
motd = [] # will be filled

daemonstarted = "" # time when daemon was started

debug = True

# stuff that is listed in isupport
isupport = []
support = {
    "CASEMAPPING": "rfc1459", #
    "PREFIX": "(qaohv)~&@%+",
    "CHANTYPES": "#~",
    "KICKLEN": "160",
    "MODES": "4",
    "NICKLEN": "32",
    "TOPICLEN": "256",
    "STATUSMSG": "~&@%+",
    "NETWORK": "Boardcast.in", # supposed to be replaced
    "MAXLIST": "beI:250",
    "CHANLIMIT": "#~:75",
    "CHANNELLEN": "50",
    "CHANMODES": "b,k,l,BCMNORScimnpstz",
    "SAFELIST": "",
    "FNC": "",
    "KNOCK": "",
    "AWAYLEN": "160",
    "EXCEPTS": "e",
    "INVEX": "I"
}

def init():

    # resolve "dynamic" servername
    global servername
    if servername[0] == ".":
        import socket
        servername = "%s%s" % (socket.gethostname(), servername)

    # load MOTD
    try:
        global motd, motd_file
        motd = []
        file = open(motd_file)
        for line in file.readlines():
            motd.append(line.rstrip())
    except:
        pass

    # compile ISUPPORT list
    global support, isupport
    l = []
    for key in support.keys():
        if support[key] == "":
            l.append(key)
        else:
            l.append("%s=%s" % (key, support[key]))
        if len(l) == 10:
            isupport.append(" ".join(l))
            l = []
    if len(l) != 0:
        isupport.append(" ".join(l))
        l = None

    # compute daemon start time for RPL_004
    global daemonstarted
    import datetime
    daemonstarted = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")