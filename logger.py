log_file = None
import config, datetime
def init():
    global log_file
    log_file = open(config.log_file, 'a')
    
def write(data, toConsole=True, toFile=True):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data = "[%s]%s" % (date,data)
    if log_file != None:
        if toConsole: 
            print "%s\n" % data
        if toFile: 
            log_file.write("%s\n" % data)
    else:
        if toConsole:
            print "%s\n" % data
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