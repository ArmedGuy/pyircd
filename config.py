version = "0.1-debug-test"


type =  "node" # node or master
servername = "test.pie-studios.com" # unique servername for a network
host = "0.0.0.0" # host that this master/node will listen on
listenport = 6667 # TCP ports to listen on as node, UDP ports to listen on as master
masterserver = ("server.pie-studios.com", 12000) # if node, connection to a master server; if master, connection to another master server, highest master must have this as None

log_file = "console.log"
motd_file = "test.txt" # file containing the message of the day