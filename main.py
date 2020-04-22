"""
https://discordapp.com/oauth2/authorize?client_id=702434593093189822&scope=bot&permissions=68608
"""

import discord
import os
from dotenv import load_dotenv
from random import choice

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN = os.getenv('ADMIN')

client = discord.Client()

@client.event
async def on_ready():
    print('Bot prêt.')

@client.event
async def on_message(message):
    print('Message received.')
    if message.author == client.user:
        return
    if message.content.startswith('!scrapmemes'):
        channel = message.channel
        if int(message.author.id) == int(ADMIN):
            print('Scraping...')
            files = 0
            cache = 0
            with open("scrap_log.txt", "w+") as log:
                log.write("===== NEW SCRAP ====\n")
                async for message in channel.history(limit=None):
                    author_name = message.author.display_name
                    if len(message.attachments) > 0:
                        for attachment in message.attachments:
                            url = attachment.url
                            if url.endswith('.png') or url.endswith('.gif') or url.endswith('.jpg') or url.endswith('.jpeg'):
                                files += 1
                                filename = channel.name + "-" + str(message.author.id) + "-" + str(message.id) + "-" + url.split('/')[-1]
                                fullpath = os.path.join('./downloads', filename)
                                exists = os.path.exists(fullpath)
                                if exists:
                                    cache += 1
                                else:
                                    await attachment.save(fullpath)
                                log.write('{0} - {1} - {2}\n'.format(author_name, url, ['OK', 'Cached'][exists]))
                                print('{0} - {1} - {2}'.format(author_name, url, ['OK', 'Cached'][exists]))
                await channel.send("J'ai trouvé {0} nouvelles images ! En cache: {1}".format(files - cache, cache))
        """
        else:
            messages = [
                "Non vraiment, ça sert à rien...",
                "Stop, t'as pas le droit.",
                "Toi-même.",
                "Demande à Ran si tu peux faire ça.",
                "Wesh arrête là",
                "NON",
                "Nique.",
                "ptdr",
                "Tu t'es cru où ?",
                "Va réviser toi là"
            ]
            await channel.send(choice(messages))
        """
client.run(TOKEN)
