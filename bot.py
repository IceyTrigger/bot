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
from cogs.utils.paginator import Pages
bot = commands.Bot(command_prefix='?',description="Brotat285 owner: dogoo#1635\n\nHelp Commands",owner_id=293159670040887297)
bot.load_extension("cogs.mod")

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
                
@commands.command(no_pm=True)
async def clean(ctx, limit: int = 15):
        '''Clean a number of bot's messages'''
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=limit + 1, check=lambda m: m.author == ctx.bot.user)
        await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=5)
        
@bot.command(aliases=['del', 'p', 'prune'], bulk=True)
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
