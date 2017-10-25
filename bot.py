import discord
from discord.ext import commands
import time
import datetime
import asyncio
import traceback
import textwrap
import io
import aiohttp
import os
import psutil
import pip
import wikipedia
import random as rng

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['?', '%', '!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if message.guild.id is None:
        # Only allow ? to be used in DMs
        return '$'

        # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix='?',description="Brotat285 owner: dogoo#1635\n\nHelp Commands",owner_id=293159670040887297)

bot = commands.Bot(command_prefix=get_prefix)

@bot.command(no_pm = True, aliases = ['ping'])
async def latency(ctx):
        pingms = "{}".format(int(bot.latency * 1000))
        pings = "{}".format(int(bot.latency * 1))
        message = await ctx.send("Calculating some stuff in the background... beep beep...")
        await asyncio.sleep(3)
        await message.edit(content = f"Pong! - My latency is **{pings}**s | **{pingms}**ms")
        await message.edit(delete_after = 15)
        await ctx.message.delete()
        
@bot.command(pass_context = True, no_pm = True)
async def announce(ctx, *, announcement: str):
    if ctx.message.author.server_permissions.administrator:
     """Sends an announcement in the channel you use the command"""
    embed=discord.Embed(title = "__Announcement__", description= announcement, color = 0xFF0000)
    await bot.delete_message(ctx.message)
    await bot.say(embed = embed)
    if not ctx.message.author.server_permissions.administrator:
        await bot.say("**You do not have permissions for this command!**")
        
@bot.command(pass_context=True)
async def echo(ctx, *, echo: str):
        '''Speaks for you'''
        if echo.__contains__("@everyone") or echo.__contains__("@here"):
            try:
                await ctx.message.delete()
            except: pass
            await ctx.send(f"{ctx.author.mention}, Really ? You think you're smart enough to fool me ? :smirk:")
            return
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(echo)
            
@bot.command(pass_context=True, hidden=True)
async def botleavep(ctx, serverid: str):
    '''Leave server(BOT OWNER ONLY)
    example:
    -----------
    :leaveserver 102817255661772800
    '''
    server = bot.get_server(serverid)
    if server:
        await bot.leave_server(server)
        msg = ':door:  {} = Left server!'.format(server.name)
    else:
        msg = ':x: Could not find the ID of that server/Forgot to say ID of server!'
        return await bot.say(msg)
    await bot.say(msg)
            
@bot.command(pass_context = True)
async def yetify(ctx):
    try:
        for member in ctx.message.server.members:
            if member is not ctx.message.server.owner:
                if member.nick is not None:
                    name = member.nick
                    await bot.change_nickname(member, "Yeti {}".format(name))
                else:
                    name = member.name
                    await bot.change_nickname(member, "Yeti {}".format(name))
        await bot.say("This server has been Yetified!")
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await bot.say("Permissions too low!")
        
@bot.command(pass_context = True)
async def clearnicks(ctx):
    try:
        for member in ctx.message.server.members:
            if member is not ctx.message.server.owner:
                name = member.name
                await bot.change_nickname(member, name)
        await bot.say("This server's nicknames have been cleared!")
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await bot.say("Permissions too low!")
            
@bot.command()
async def ud(*msg):
    """Search words on Urban Dictionary"""
    word = ' '.join(msg)
    api = "http://api.urbandictionary.com/v0/define"
    async with aiohttp.ClientSession() as session:
        async with session.get(api, params={'term': word}) as r:
            response = await r.json()

        if len(response["list"]) == 0:
            x = "Could not find that word!"
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.description = x
            await bot.say(embed=embed)
            
        else:
                embed = discord.Embed(title='Urban Dictionary - ' + word, color=0x00FF00)
                embed.description = response['list'][0]['definition']
                embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/B4lcjSHEDA8RcuizSOAdc92ithHovZT6WkRAX-da_6o/https/erisbot.com/assets/emojis/urbandictionary.png')
                embed.add_field(name="Examples:", value=response['list'][0]["example"][:1000])
                embed.set_footer(text="Tags: " + ', '.join(response['tags']))
                await bot.say(embed=embed)
            
@bot.command()
async def baninfo(ctx, *, name_or_id):
        '''Check the reason of a ban from the audit logs.'''
        ban = await ctx.get_ban(name_or_id)
        em = discord.Embed()
        em.color = await ctx.get_dominant_color(ban.user.avatar_url)
        em.set_author(name=str(ban.user), icon_url=ban.user.avatar_url)
        em.add_field(name='Reason', value=ban.reason or 'None')
        em.set_thumbnail(url=ban.user.avatar_url)
        em.set_footer(text=f'User ID: {ban.user.id}')

        await ctx.send(embed=em)
        
@bot.command()
async def clean(ctx, limit : int=15):
        '''Clean a number of your own messages'''
        await ctx.purge(limit=limit+1, check=lambda m: m.author == ctx.author)
        
@commands.command(aliases=['g'])
async def google(ctx, *, query):
        """
        Searches google and gives you top result.
        Written By Rapptz
        """
        await ctx.trigger_typing()
        try:
            card, entries = await self.get_google_entries(ctx, query)
        except RuntimeError as e:
            await ctx.send(str(e))
        else:
            if card:
                value = '\n'.join(entries[:3])
                if value:
                    card.add_field(name='Search Results', value=value, inline=False)
                return await ctx.send(embed=card)

            if len(entries) == 0:
                return await ctx.send('No results found... sorry.')

            next_two = entries[1:3]
            first_entry = entries[0]
            if first_entry[-1] == ')':
                first_entry = first_entry[:-1] + '%29'

            if next_two:
                formatted = '\n'.join(map(lambda x: '<%s>' % x, next_two))
                msg = '{}\n\n**See also:**\n{}'.format(first_entry, formatted)
            else:
                msg = first_entry

            self._last_google = msg
            await ctx.send(msg)
        
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: discord.Member):
        await ctx.channel.send(f"RIP {user.name}.")
        await user.kick()
        
@bot.command(aliases=['del','p','prune'])
async def purge(ctx, limit : int):
        '''Clean a number of messages'''
        await ctx.purge(limit=limit+1) # TODO: add more functionality
        
@commands.command()
async def choose(ctx, *choices: commands.clean_content):
        """Chooses between multiple choices.
        To denote multiple choices, you should use double quotes.
        """
        if len(choices) < 2:
            return await ctx.send('Not enough choices to pick from.')

        await ctx.send(rng.choice(choices))
    
@bot.command()
@commands.has_permissions(ban_members = True)
async def unmute(ctx, user: discord.Member):
        await ctx.channel.set_permissions(user, send_messages=True)
        await ctx.channel.send(user.mention + 'Has Been Unmuted.') 
        
@bot.command(aliases=['av'])
async def avatar(self, ctx, *, member: discord.Member = None):
        '''Gets someones pfp'''
        member = member or ctx.author
        av = member.avatar_url
        if ".gif" in av:
            av += "&f=.gif"
        em = discord.Embed(url=av)
        em.set_author(name=str(member), icon_url=av)
        em.set_image(url=av)
        await ctx.send(embed=em)
     
@bot.command()
async def warn(ctx, user: discord.Member=None, reason=None):
        '''Warn a member\n Use Double Quotes " When Using Spaces In Reason'''
        warning = 'You have been warned in **{}** by **{}** for: **{}**'
        server = ctx.message.guild
        author = ctx.message.author
        await ctx.send('**{}** has been warned'.format(user))
        await user.send(warning.format(server, author, reason))
        await ctx.message.delete(ctx.message)
        
@bot.command()
@commands.has_permissions(ban_members = True)
async def mute(ctx, user: discord.Member):        
        await ctx.channel.set_permissions(user, send_messages=False)
        await ctx.channel.send(user.mention + " Has Been Muted From This Channel.")
        
        
@bot.command(pass_context=True, no_pm=True)
async def removerole(ctx, user: discord.Member, *, role):
    if ctx.message.author.server_permissions.administrator:
        await bot.remove_roles(user, discord.utils.get(ctx.message.server.roles, name=role))
        await bot.say("Removed the role %s from %s" % (role, user.mention))
    else:
        embed = discord.Embed(description = "**You cannot use removerole command!**", color = 0xFF0000)
        return await bot.say(embed = embed)

@bot.command(pass_context = True)
async def addrole(ctx, user: discord.Member, *, role: str):
        server_roles = [role for role in ctx.message.server.roles if not role.is_everyone]
        add = discord.utils.find(lambda m: role.lower() in m.name.lower(), ctx.message.server.roles)
        if not add:
            await self.bot.say('That role doesnt exist')
        if ctx.message.author.server_permissions.manage_roles:
            try:
                await self.bot.add_roles(user, add)
                await self.bot.say('I gave {} the {} role'.format(user, role))
            except discord.Forbidden:
                await self.bot.say('I need **Manage Roles** for this')
        else:
             await self.bot.say('You need *Manage Roles** for this')
                
@bot.command(pass_context = True)
async def ctdev(ctx, *, pmessage : str = None):
        '''Contact the dev'''
        invite = await ctx.channel.create_invite(max_uses = 1, xkcd = True)
        bot_owner = 293159670040887297
        embed_color = 0x808080
        dev = bot.get_user(293159670040887297)
    
        if pmessage == None:
            embed = discord.Embed(description = "**"+ ctx.author.name +"** my developers need to know something right? Type a feedback!", color = embed_color_error)
            await ctx.send(embed = embed)
            await ctx.message.delete()
        else:
#            msg = "User: {}\nServer: {}\nFeedBack: {}\nServer Invite: {}".format(ctx.author, ctx.guild, pmessage, invite.url)
            embed = discord.Embed(title = "Invite to {} discord server!".format(ctx.guild), colour = embed_color, url = "{}".format(invite.url), description = "**Feedback:** {}".format(pmessage), timestamp = datetime.datetime.utcfromtimestamp(1507439238))
            embed.set_thumbnail(url = "{}".format(ctx.author.avatar_url))
            embed.set_author(name = "{} sent:".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await dev.send(embed = embed)
#            await dev.send(msg)
            embed = discord.Embed(description = "I have PMed **{}#{}** with your feedback! Thank you for your help!".format(dev.name, dev.discriminator), color = embed_color_succes)
            await ctx.send(embed = embed)
            await ctx.message.delete()
#            return await ctx.send(ctx.author.mention + " I have PMed my creator your feedback! Thank you for the help!")

@bot.command(aliases=['wikipedia'], pass_context=True)
async def wiki(ctx, *, search: str = None):
        '''Wikipedia ok!!!'''
        if search == None:
            await ctx.channel.send(f'Usage: `{ctx.prefix}wiki [search terms]`')
            return

        results = wikipedia.search(search)
        if not len(results):
            no_results = await ctx.channel.send("Sorry, didn't find any result.")
            await asyncio.sleep(5)
            await ctx.message.delete(no_results)
            return

        newSearch = results[0]
        try:
            wik = wikipedia.page(newSearch)
        except wikipedia.DisambiguationError:
            more_details = await ctx.channel.send('Please input more details.')
            await asyncio.sleep(5)
            await ctx.message.delete(more_details)
            return

        emb = discord.Embed()
        emb.title = wik.title
        emb.url = wik.url
        textList = textwrap.wrap(wik.content, 500, break_long_words=True, replace_whitespace=False)
        emb.add_field(name="Wikipedia Results", value=textList[0] + "...")
        await ctx.send(embed=emb)


@bot.command(pass_context=True, hidden=True, name='eval')
@commands.is_owner()
async def _eval(ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            from contextlib import redirect_stdout
            ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')

@bot.command(name='presence')
@commands.is_owner()
async def _set(ctx, Type=None,*,thing=None):
  """Change the bot's discord game/stream!"""
  if Type is None:
    await ctx.send('Usage: `.presence [game/stream] [message]`')
  else:
    if Type.lower() == 'stream':
      await bot.change_presence(game=discord.Game(name=thing,type=1,url='https://www.twitch.tv/youngboyivan'),status='online')
      await ctx.send(f'Set presence to. `Streaming {thing}`')
    elif Type.lower() == 'game':
      await bot.change_presence(game=discord.Game(name=thing))
      await ctx.send(f'Set presence to `Playing {thing}`')
    elif Type.lower() == 'clear':
      await bot.change_presence(game=None)
      await ctx.send('Cleared Presence')
    else:
      await ctx.send('Usage: `.presence [game/stream] [message]`')
    
@bot.command()
async def invite(ctx):
    await ctx.send('https://discordapp.com/oauth2/authorize?client_id=371320386693890048&scope=bot&permissions=2146958591')

class MainCommands():
    def __init__(self, bot):
        self.bot = bot

    @bot.event
    async def on_ready():
        """Shows bot's status"""
        print("Logged in as:")
        print("Name : {}".format(bot.user.name))
        print("ID : {}".format(bot.user.id))
        print("----------------")
if not os.environ.get('TOKEN'):
    print("no token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('"'))