from sys import stderr
import disnake
import asyncio

from contextlib import contextmanager

import logging
from logging.handlers import RotatingFileHandler


from bot import GentlemenBot
import config

class RemoveNoise(logging.Filter):
    def __init__(self):
        super().__init__(name='discord.state')

    def filter(self, record):
        if record.levelname == 'WARNING' and 'referencing an unknown' in record.msg:
            return False
        return True

@contextmanager
def setupLogging():
    try:
        logging.getLogger('disnake').setLevel(logging.INFO)
        logging.getLogger('disnake.http').setLevel(logging.WARNING)
        logging.getLogger('disnake.state').addFilter(RemoveNoise())

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')

        Filehandler = RotatingFileHandler(filename=config.logFile, encoding='utf-8', mode='w', maxBytes=config.logSize, backupCount=config.logBackupCount)
        Filehandler.setFormatter(fmt)
        log.addHandler(Filehandler)

        consoleHandler = logging.StreamHandler(stream=stderr)
        consoleHandler.setFormatter(fmt)
        consoleHandler.setLevel(logging.DEBUG)
        log.addHandler(consoleHandler)

        log.log(100,"##########  Bot Starting ##########")

        yield
    finally:
        log.log(100,"##########  Bot Stopped ##########")
        for hdl in log.handlers:
            hdl.close()
            log.removeHandler(hdl)

def runBot():
    bot = GentlemenBot()

    bot.run()

def main():
    with setupLogging():
        runBot()


if __name__ == '__main__':
    main()