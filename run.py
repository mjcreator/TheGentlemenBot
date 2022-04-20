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
class ColorFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt, datefmt=None, style = '%'):
        super().__init__()
        self.fmt = fmt
        self.datefmt = datefmt
        self.style = style
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.datefmt, style=self.style)
        return formatter.format(record)

@contextmanager
def setupLogging():
    try:
        logging.getLogger('disnake').setLevel(logging.INFO)
        logging.getLogger('disnake.http').setLevel(logging.WARNING)
        logging.getLogger('disnake.state').addFilter(RemoveNoise())

        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmtStr = '[{asctime}] [{levelname:<7}] {name}: {message}'
        fmt = logging.Formatter(fmtStr, dt_fmt, style='{')

        Filehandler = RotatingFileHandler(filename=config.logFile, encoding='utf-8', mode='w', maxBytes=config.logSize, backupCount=config.logBackupCount)
        Filehandler.setFormatter(fmt)
        Filehandler.setLevel(logging.INFO)
        log.addHandler(Filehandler)

        consoleHandler = logging.StreamHandler(stream=stderr)
        consoleHandler.setFormatter(ColorFormatter(fmtStr, dt_fmt, style='{'))
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