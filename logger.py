log_file = None
write_lock = None
import config, datetime, threading
def init():
    global log_file, write_lock
    log_file = open(config.log_file, 'a')
    write_lock = threading.Lock()
    
def write(data, toConsole=True, toFile=True):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data = "[%s]%s" % (date,data)
    with write_lock:
        if log_file != None:
            if toConsole: 
                print "%s" % data
            if toFile: 
                log_file.write("%s\n" % data)
        else:
            if toConsole:
                print "%s" % data
            print "Logfile not initialized!"

def debug(data, toConsole=True, toFile=True):
    write("[DEBUG]: %s" % data)
def verbose(data, toConsole=True, toFile=True):
    write("[VERBOSE]: %s" % data)  
def info(data, toConsole=True, toFile=True):
    write("[INFO]: %s" % data)
def warning(data, toConsole=True, toFile=True):
    write("[WARNING]: %s" % data)
def error(data, toConsole=True, toFile=True):
    write("[ERROR]: %s" % data)
def fatal(data, toConsole=True, toFile=True):
    write("[FATAL]: %s" % data)