import config, logger, daemons, time
from tests import pyircbot

config.init()
logger.init()
logger.info("derp", True, False)
daemon = daemons.NodeDaemon("0.0.0.0", 6667)
daemon.start()

"""
settings = {
    'host': "127.0.0.1",
    'port': 6667,
    'nick': 'pyircbot',
    'ident': 'pyircbot',
    'realname': 'TheLeagueSpecialist',
    'debug': False
}
bot = pyircbot.create(settings)
standard = pyircbot.StandardBotRoutines(bot, settings)
standard.queueJoinChannels(["#Pie-Studios"])

bot.connect()
"""
 
while True:
    time.sleep(1)