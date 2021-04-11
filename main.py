import os
import json
import requests
import discord
from service import insert,get_data
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message,"\n")
    # print(dir(message))
    if message.author == client.user:
        return 

    if message.content.startswith('$hi'):
        await message.channel.send('hey')
    
    if message.content.startswith('!recent'):
        q=message.content.split("!recent")[1]
        rest=get_data(q,message.author.id)
        print(rest)
        await message.channel.send(rest)
        
        if len(rest)==0:
            await message.channel.send("No result found")

    if message.content.startswith('!google'):
        q=message.content.split("!google")[1]
        url='https://www.googleapis.com/customsearch/v1?key=AIzaSyCnUxZ_ZSDGmrEOcV4tTf0yDrG-OxzbPpA&cx=013384490937324803065:etsy46pgcig&q='
        res=requests.get(url+q)
        data=res.json()
        if data.get('items',None) is not None:
            items=data['items']
            items=[{'title':i['title'],'link':i['link'],"author_name":message.author.name,"author_id":message.author.id} for i in items[:6]]
            insert(items)
            _items='\n'.join([i['link']for i in items[:6]])
            await message.channel.send(_items)
        else:
            await message.channel.send('No result found for given query')

client.run(os.getenv('Token'))
