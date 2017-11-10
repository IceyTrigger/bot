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
import youtube_dl
import math
import operator
from cogs.utils.paginator import Pages
bot = commands.Bot(command_prefix='?',description="Brotat285 owner: dogoo#1635\n\nHelp Commands",owner_id=293159670040887297)

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

bot = commands.Bot(command_prefix=get_prefix)
       

async def format_mod_embed(self, ctx, user, success, method, duration = None, location=None):
        '''Helper func to format an embed to prevent extra code'''
        emb = discord.Embed()
        emb.set_author(name=method.title(), icon_url=user.avatar_url)
        emb.color = await ctx.get_dominant_color(user.avatar_url)
        emb.set_footer(text=f'User ID: {user.id}')
        if success:
            if method == 'ban' or method == 'hackban':
                emb.description = f'{user} was just {method}ned.'
                
                   
@bot.command(pass_context = True)
@commands.is_owner()
async def shutdown(ctx):
    timestamp = ctx.message.timestamp                         
    embed=discord.Embed(title='Restarting', description='See you later', color=0xed, timestamp=timestamp)
    embed.set_footer(text='brotat will be back')
    await bot.say(embed=embed)
    await bot.logout()
                
@bot.command(aliases=['calc', 'maths'])
async def calculate(ctx, *, formula=None):
        """
        Do some real math
        finally a working command for mathematics
        thanks to Paul McGuire's fourFn.py module
        """
        person = ctx.message.author
        user = ctx.author

        if formula == None:
            # How can it calculate an empty message? Reee!
            msg = f'\u200BUsage: `{ctx.prefix}{ctx.invoked_with} [any maths formula]`'
            e = discord.Embed()
            e.color = await ctx.get_dominant_color(user.avatar_url)
            e.description = f'{msg}'
            await ctx.send(embed=e)
            return

        try:
            answer=bot.nsp.eval(formula)
        except:
            # If there's a problem in the input, show examples
            msg = f'\N{THINKING FACE} wrong {formula} input.\nTry any of these:'
            e = discord.Embed()
            e.color = await ctx.get_dominant_color(user.avatar_url)
            e.description = f'\u200B{msg}'
            e.add_field(name='multiplication', value="`num` * `num`", inline=True)
            e.add_field(name='division', value="`num` / `num`", inline=True)
            e.add_field(name='addition', value="`num` + `num`", inline=True)
            e.add_field(name='rest', value="`num` - `num`", inline=True)
            e.add_field(name='exponential', value="`num` ^ `num`")
            e.add_field(name='integer', 
                        value="[`num` + `num` | `num` - `num`] `num` 0 `num`..`num` 9 `num` +")
            await ctx.send(embed=e, delete_after=60)
            return

        # Correct input prints correct answer
        e = discord.Embed()
        e.color = await ctx.get_dominant_color(user.avatar_url)
        e.add_field(name='Input:', value=f'```{formula}```', inline=True)
        e.add_field(name='Result:', value=f'```{round(answer, 2)}```', inline=True)
        await ctx.send(embed=e)
                
@bot.command(name='presence')
@commands.is_owner()
async def _set(ctx, Type=None,*,thing=None):
  """Change the bot's discord game/stream!"""
  if Type is None:
    await ctx.send('Usage: `.presence [game/stream] [message]`')
  else:
    if Type.lower() == 'stream':
      await bot.change_presence(game=discord.Game(name=thing,type=1,url='https://www.twitch.tv/a'),status='online')
      await ctx.send(f'Set presence to. `Streaming {thing}`')
    elif Type.lower() == 'game':
      await bot.change_presence(game=discord.Game(name=thing))
      await ctx.send(f'Set presence to `Playing {thing}`')
    elif Type.lower() == 'clear':
      await bot.change_presence(game=None)
      await ctx.send('Cleared Presence')
    else:
      await ctx.send('Usage: `.presence [game/stream] [message]`')
        
@bot.command(no_pm = True, aliases = ['ping'])
async def latency(ctx):
        pingms = "{}".format(int(bot.latency * 1000))
        pings = "{}".format(int(bot.latency * 1))
        message = await ctx.send("Calculating some stuff in the background... beep beep...")
        await asyncio.sleep(3)
        await message.edit(content = f"Pong! - My latency is **{pings}**s | **{pingms}**ms")
        await message.edit(delete_after = 15)
        await ctx.message.delete()
        
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: discord.Member):
        await ctx.channel.send(f"Bye! {user.name}.")
        await user.kick()
        
@bot.command()
@commands.has_permissions(kick_members = True)
async def ban(ctx, user: discord.Member):
        await ctx.channel.send(f"Banned {user.name} close the door on the way out :door: .")
        await user.ban()
        
@bot.command(pass_context = True)
async def play(ctx, url):
    global playing
    playing = False
    channel = ctx.message.author.voice_channel    
    if bot.is_voice_connected(ctx.message.server):
        embed = discord.Embed(title = "Already Connected!", description = "The bot is already connected to a voice channel!", color = 0xFF0000)
        return await bot.say(embed = embed)
    voice = await bot.join_voice_channel(channel)
    global player
    player = await voice.create_ytdl_player(url)
    player.start()
    playing = True
    embed = discord.Embed(color = embed_color)
    embed.add_field(name="Now Playing:", value=player.title, inline=True)
    embed.add_field(name="Requested By:", value=ctx.message.author, inline=True)
    embed.add_field(name="Duration (Seconds):", value=player.duration, inline=True)
    embed.add_field(name="Views:", value=player.views, inline=True)
    await client.say(embed = embed)
    
@bot.command(pass_context = True)
async def stop(ctx):
    if bot.is_voice_connected(ctx.message.server):
        embed2 = discord.Embed(description = "Stopping..", color = embed_color)
        await client.say(embed = embed2)
        player.stop()
        playing = False
    else:
        embed = discord.Embed(description = "Not connected to a voice channel!", color = embed_color)
        await client.say(embed = embed)
        
@bot.command(pass_context = True)
async def pause(ctx):
    if bot.is_voice_connected(ctx.message.server):
        embed = discord.Embed(description = "Paused!", color = embed_color)
        await bot.say(embed = embed)
        player.pause()
    else:
        embed = discord.Embed(description = "Not connected to a voice channel!", color = embed_color)
        await client.say(embed = embed)
        
@bot.command(pass_context = True)
async def resume(ctx):
    if bot.is_voice_connected(ctx.message.server):
        embed = discord.Embed(description = "Resuming the song!", color = embed_color)
        await bot.say(embed = embed)
        player.resume()
    else:
        embed = discord.Embed(description = "Not connected to a voice channel!", color = embed_color)
        await client.say(embed = embed)
        
@bot.command(pass_context = True, aliases=['sinfo', 'si'])
async def serverinfo(ctx):

        server = ctx.message.server
        roles = [x.name for x in server.role_hierarchy]
        role_length = len(roles)
        roles = ', '.join(roles);
        channels = len(server.channels);
        time = str(server.created_at); time = time.split(' '); time= time[0];

        embed = discord.Embed(description= "Info on this server",title = ':thinking:', colour = {0xFF0000});
        embed.set_thumbnail(url = server.icon_url);
        embed.add_field(name = '__Server __', value = str(server))
        embed.add_field(name = '__Server ID__', value = str(server.id))
        embed.add_field(name = '__Owner__', value = str(server.owner));
        embed.add_field(name = '__Owner ID__', value = server.owner.id)
        embed.add_field(name = '__Members__', value = str(server.member_count));
        embed.add_field(name = '__Text/Voice Channels__', value = str(channels));
        embed.add_field(name = '__Roles__', value = '%s'%str(role_length));
        embed.add_field(name = '__Server Region__', value = '%s'%str(server.region));
        embed.add_field(name = '__AFK Timeout__', value = server.afk_timeout +'seconds');
        embed.add_field(name = '__AFK Channel__', value = server.afk_channel);
        embed.add_field(name = '__Verification Level__', value = server.verification_level)
        embed.add_field(name = '__Created on__', value = server.created_at.__format__('Date - %d %B %Y at time - %H:%M:%S'));
        
        return await client.say(embed = embed);
        
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
            
@bot.command()
async def ud(*msg):
    """Search words on UrbanDictionary"""
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
              
        
@bot.command(aliases=['del', 'p', 'prune'], bulk=True)
@commands.has_permissions(kick_members = True)
async def purge(ctx, limit: int):
        '''Clean a number of messages'''
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=limit + 1)
        await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=6)
        
        

        
@bot.command()
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
@commands.has_permissions(kick_members= True)
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
