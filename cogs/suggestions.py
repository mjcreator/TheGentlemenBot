from datetime import datetime
from email import message
from typing import Optional, Union
from disnake.ext import commands

import disnake
import asyncio
import logging

class Suggestion(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(type(self).__name__)
        self.suggestChannel = {916230367004987422 : 916387144182923285}


        self.upvoteEmoji = disnake.PartialEmoji(name="✅")#.from_str("upvote:524907425531428864")
        self.downvoteEmoji = disnake.PartialEmoji(name="❌")#.from_str("downvote:524907425032175638")

        self.voteReactions = [self.upvoteEmoji.name, self.downvoteEmoji.name]
        #self.logger.debug(f"vote emoji's: {self.voteReactions}")

    @commands.slash_command()
    @commands.default_member_permissions(manage_channels=True, manage_guild=True)
    async def set_suggestion_channel(self, inter : disnake.CommandInteraction, channel : disnake.TextChannel):
        '''
        Sets the channel that suggestions should be posted in.

        Parameters 
        ----------
        channel: The channel to post suggestions in
        '''
        
        self.suggestChannel[inter.guild_id] = channel.id
        self.logger.info(f'Changed the suggestion channel for {inter.guild.name}({inter.guild_id}) to {channel.name}({channel.id})')
        await inter.send(f'Set suggestion channel to {channel.name}')

    @commands.slash_command(aliases=['suggestion'])
    async def suggest(self, inter : disnake.CommandInteraction, description:str, role : str = None, user : disnake.User = None):
        '''
        Submits a suggestion for the server. 

        Parameters 
        ----------
        description: what it is you are suggesting
        role: name of a role to suggest
        user: user a role should be applied to
        '''
        if(description == ""):
            await inter.send("Your suggestion is missing a description", ephemeral=True)
            return
        
        embed = disnake.Embed(
            description=description,
            color=9021952,
            timestamp=inter.created_at,
        )
        author = inter.author
        embed.set_author(
            name=author.display_name,
            icon_url=author.display_avatar.url
        )

        params = ""
        if(role is not None):
            embed.add_field(name="Add Role:", value=role)
            params += f" New role `{role}`"
        if(user is not None):
            embed.add_field(name="To:", value=user.mention)
            params += f" for {user.mention}. "

        self.logger.info(f"Suggestion submitted by {author.name}#{author.discriminator} with description \"{description}\"; Params:{params}")

        message = f"Suggestion submitted:{params}\n{description}"

        guildID = inter.guild_id
        if(guildID in self.suggestChannel):
            msg = await inter.guild.get_channel(self.suggestChannel[guildID]).send(embed=embed)
            await msg.add_reaction(self.upvoteEmoji)
            await msg.add_reaction(self.downvoteEmoji)
        else:
            msg = await inter.channel.send(embed=embed)
            await msg.add_reaction(self.upvoteEmoji)
            await msg.add_reaction(self.downvoteEmoji)

        await inter.send(message, delete_after=5)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        if payload.guild_id is None or payload.member is None or payload.member.bot:
            return
        
        self.logger.debug(f"new reaction from {payload.member.name} with {payload.emoji}")
        message = self.bot.get_message(payload.message_id)
        print(message.mentions)
        if(message and message.author == self.bot.user):
            self.logger.debug(f"message has reactions {message.reactions}")
            for reaction in message.reactions:
                self.logger.debug(f"Reaction has emoji {reaction.emoji} and is a vote? {reaction.emoji in self.voteReactions}; Is my reaction? {payload.emoji.name == reaction.emoji}")

                if(reaction.emoji in self.voteReactions and payload.emoji.name != reaction.emoji):
                    otherReactions = await reaction.users().get(id=payload.member.id)
                    if otherReactions is not None:
                        self.logger.debug("user already voted, removing other reaction")
                        await reaction.remove(payload.member)
        else:
            self.logger.debug(f"unable to find message {payload.message_id}")

def setup(bot):
    bot.add_cog(Suggestion(bot))