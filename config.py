version = "0.1-debug-test"

dumb = False
type =  "node" # can be:
"""
    * "node" - regular node that connects to a master
    * "vnode" - "virtual" node that shares servername with other vnodes(physical hostnames can differ)
    * "master" - master that handles nodes and vnodes, and syncs with other masters
    * "master-node" - both a master and a node
"""

servername = "test.pie-studios.com" # unique servername for a network, starting with a "."(dot) will prefix the string with the underlying OS hostname
serverpassword = None

host = "0.0.0.0" # host that this master/node will listen on
listenports = (6667) # TCP ports to listen on as node, UDP ports to listen on as master
masterserver = ("server.pie-studios.com", 12000) # if node, connection to a master server; if master, connection to another master server, highest master must have this as None

log_file = "console.log"
motd_file = "test.txt" # file containing the message of the day