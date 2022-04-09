from dataclasses import replace
from datetime import datetime
from email import message
from random import randint
from typing import Optional, Union
from disnake.ext import commands

import re

import disnake
import asyncio
import logging

class AprilFools(commands.Cog):
    """
    A fun little April fools extention that replaces messages that have gifs with rick rolls
    """
    def __init__(self, bot, serverID):
        self.bot = bot
        self.logger = logging.getLogger(type(self).__name__)
        self.serverID = serverID
        self.tenorFinder = re.compile(r'(http|ftp|https):\/\/(tenor(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])')
        self.replacements = [
            "https://tenor.com/view/rick-roll-rick-ashley-never-gonna-give-you-up-gif-22113173",
            "https://tenor.com/view/rick-roll-nitro-gif-21997352",
            "https://tenor.com/view/get-stickbugged-lol-get-distracted-distracted-stickbug-rickroll-gif-18294537",
            "https://tenor.com/view/rick-roll-gif-19920902",
            "https://tenor.com/view/challenge-find-out-when-this-gif-ends-rickroll-rickrolled-hidden-rickroll-gif-22493495",
            "https://tenor.com/view/suffer-rickroll-llamatroll-syntheticllama-gif-21044288",
            "https://tenor.com/view/funny-unfunny-please-become-funny-8ball-magic8ball-gif-23567174",
            "https://tenor.com/view/sapo-meme-boca-pepe-gif-14416557",
            "https://tenor.com/view/youre-fucked-the-simpsons-magic-eight-gif-15834392",
            "https://tenor.com/view/rock-one-eyebrow-raised-rock-staring-the-rock-gif-22113367",
            "https://tenor.com/view/dance-spore-gif-20319309",
            "https://tenor.com/view/klm-aviation-aircraft-airplane-royal-dutch-airlines-gif-23425518",
            "https://tenor.com/view/i-see-no-problem-here-crazy-eyes-gif-12788383",
        ]

    @commands.Cog.listener()
    async def on_message(self, message : disnake.Message):
        '''
        replaces gif links in messages with aprils fools gifs 
        '''
        if(message.guild.id == self.serverID and message.author.id != 916407067437318177):

            content = message.content
            newContent = ""
            if(content is not None):
                pos = 0
                for m in self.tenorFinder.finditer(content):
                    item = self.replacements[randint(0,len(self.replacements)-1)]
                    newContent += content[pos:m.start()] + item 
                    pos = m.end()

                if(newContent):
                    newContent += content[pos:]
                    self.logger.info(f"Found gif in message \"{content}\", replacing with \"{newContent}\"")
                    await message.channel.send(content=newContent, mention_author=message.author)
                    await message.delete()            

def setup(bot):
    bot.add_cog(AprilFools(bot,916230367004987422))