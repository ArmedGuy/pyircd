import config, logger, daemons, time

logger.init()
logger.info("derp", True, False)
daemon = daemons.NodeDaemon()
daemon.start()

while True:
    time.sleep(1)