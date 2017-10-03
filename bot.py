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
    await client.change_presence(game=discord.Game(name="say "+prefix+"ud <search>"))
    logging.info('on_ready,{},presence state set'.format(client.user.name))

@client.event
async def on_message(m):
    if m.author == client.user:
        return
    if m.content.startswith(prefix+'ud'):
        await ud_dict(m)
        return

async def ud_dict(m):
    mess = m.content.split(" ")
    search = " ".join(mess[1:])
    defs = ud.define(search)
    ud_url = "http://www.urbandictionary.com/define.php?term="+search
    if len(mess) > 2:
        ud_url = "http://www.urbandictionary.com/define.php?term="+"+".join(search.split(" "))
    if not defs:
        await client.send_message(m.channel, "I got nothing")
        return
    em = discord.Embed()
    em.color = discord.Colour(randint(0, 16777215))
    em.set_author(name=defs[0].word, url=ud_url)
    em.description = defs[0].definition
    if defs[0].example:
        em.add_field(name="Example", value=defs[0].example)
    em.add_field(name="Up Votes", value=str(defs[0].upvotes))
    em.add_field(name="Down Votes", value=str(defs[0].downvotes), inline=True)
    await client.send_message(m.channel, embed=em)

client.run(str(os.environ['DISCORD_BOTKEY']))
