import discord
import asyncio
import psutil
import random
import pip
import os
import io
from discord.ext import commands

'''Mod Commands Must Have Enough Permissons To Use Them'''

class Mod:

    def __init__(self, bot):
        self.bot = bot

@commands.command()
@commands.has_permissions(kick_members = True)
async def kick(self, ctx, user: discord.Member):
        await ctx.channel.send(f"RIP {user.name}.")
        await user.kick()



@commands.command()
@commands.has_permissions(kick_members = True)
async def ban(self, ctx, user: discord.Member):
        await ctx.channel.send(f"Banned {user.name}.")
        await user.ban()
        
        
@commands.command()
@commands.has_permissions(manage_roles = True)
async def addrole(self, ctx, user: discord.Member, role: str):
          roler = discord.utils.get(ctx.guild.roles, name=role)
          if roler is not None:
              try:
                  await user.add_roles(roler)
              except discord.Forbidden:
                  await ctx.channel.send("You don't have permissons to do this.") 
          else:
               await ctx.channel.send("I Can't Add A Nonexistent role.")
             
@commands.command()
@commands.has_permissions(manage_roles = True)
async def removerole(self, ctx, user: discord.Member, role: str):
        roler = discord.utils.find(ctx.guild.roles, name=role)
        
        if roler is not None:
            try:
                 await user.add_roles(roler)
            except discord.Forbidden:
                 await ctx.channel.send("You Don't Have Permissions To Do This")
        else:
             await ctx.channel.send("I Can't Remove A Nonexistent Role")
               
               
@commands.command()
@commands.has_permissions(ban_members = True)
async def mute(self, ctx, user: discord.Member):
        
        await ctx.channel.set_permissions(user, send_messages=False)
        await ctx.channel.send(user.mention + " Has Been Muted From This Channel.")
        
        
        
@commands.command()
@commands.has_permissions(ban_members = True)
async def unmute(self, ctx, user: discord.Member):
        
        await ctx.channel.set_permissions(user, send_messages=True)
        await ctx.channel.send(user.mention + 'Has Been Unmuted.')
        
        
@commands.command()
async def warn(self, ctx, user: discord.Member=None, reason=None):
        '''Warn a member\n Use Double Quotes " When Using Spaces In Reason'''
        warning = 'You have been warned in **{}** by **{}** for: **{}**'
        server = ctx.message.guild
        author = ctx.message.author
        await ctx.send('**{}** has been warned'.format(user))
        await user.send(warning.format(server, author, reason))
        await ctx.message.delete(ctx.message) 

        
        
def setup(bot):
        bot.add_cog(Mod(bot))
    
