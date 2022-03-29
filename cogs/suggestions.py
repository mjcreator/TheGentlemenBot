from datetime import datetime
from email import message
from typing import Optional, Union
from disnake.ext import commands

import disnake
import asyncio
import logging

class Suggestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("Suggestion")
        self.suggestChannel = {916230367004987422 : 916387144182923285}


        self.upvoteEmoji = disnake.PartialEmoji(name="✅")#.from_str("upvote:524907425531428864")
        self.downvoteEmoji = disnake.PartialEmoji(name="❌")#.from_str("downvote:524907425032175638")

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

        embed.set_author(
            name=inter.author.nick,
            icon_url=inter.author.display_avatar.url
        )

        message = f"Suggestion submitted:"
        if(role is not None):
            embed.add_field(name="Add Role:", value=role)
            message += f" New role `{role}`"
        if(user is not None):
            embed.add_field(name="To:", value=user.mention)
            message += f" for {user.mention}. "

        message += f"\n{description}"
        
        self.logger.info(message)

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
    
    # @suggest.command(name='role')
    # async def suggest_role(self, ctx, roleName:str, description:str):
    #     self.logger.debug(f"Role suggestion submitted: role={roleName}; \"{description}\"")
    #     await ctx.send("role suggestion submitted", delete_after=5)
    
    # @suggest.command(name='user-role')
    # async def suggest_user_role(self, ctx, roleName:str, member: disnake.Member, description:str):
    #     self.logger.debug(f"User role suggestion submitted: for={member.nick}, role={roleName}, \"{description}\"")
    #     await ctx.send("role suggestion submitted", delete_after=5)


def setup(bot):
    bot.add_cog(Suggestion(bot))