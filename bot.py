import os
import logging
import discord
import urbandictionary as ud
from random import randint

prefix = "!"
client = discord.Client()
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
        filename="/var/log/udbot.log", level=logging.INFO)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="say "+prefix+"ud <search>"))
    logging.info('on_ready,{0.user},presence state set'.format(client))

@client.event
async def on_message(m):
    if m.author == client.user:
        return
    if m.content.startswith(prefix+'ud'):
        await ud_handler(m)
        return
    if m.content.startswith(prefix+'urandom'):
        await ud_random_handler(m)
        return

async def ud_handler(m):
    mess = m.content.split(" ")
    search = " ".join(mess[1:])
    defs = ud.define(search)
    location = None
    if not m.guild:
        location = "priv-"+m.author.name
    else:
        location = m.guild.name
    if not defs:
        logging.info('ud_handler,{},{},{},failed'.format(m.author.name, location, search))
        await m.channel.send("I got nothing")
        return
    logging.info('ud_handler,{},{},{},success'.format(m.author.name, location, search))
    await ud_response(m, defs[0])

async def ud_random_handler(m):
    location = None
    if m.channel.is_private:
        location = "priv-"+m.author.name
    else:
        location = m.server.name
    d = ud.random()[0]
    logging.info('ud_random_handler,{},{},{},success'.format(m.author.name, location, d.word))
    await ud_response(m, d)

async def ud_response(m, d):
    ud_url = "http://www.urbandictionary.com/define.php?term="+d.word
    if len(d.word.split(" ")) > 1:
        ud_url = "http://www.urbandictionary.com/define.php?term="+"+".join(d.word.split(" "))
    em = discord.Embed()
    em.color = discord.Colour(randint(0, 16777215))
    em.set_author(name=d.word, url=ud_url)
    em.description = d.definition
    if d.example:
        em.add_field(name="Example", value=d.example, inline=False)
    em.add_field(name="Up Votes", value=str(d.upvotes))
    em.add_field(name="Down Votes", value=str(d.downvotes))
    await m.channel.send(embed=em)

client.run(str(os.environ['DISCORD_BOTKEY']))
