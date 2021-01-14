import signal
import sys
import asyncio
import aiohttp
import json
import requests
from PIL import Image, ImageTk, ImageShow
from tkinter import PhotoImage
import tkinter as tk
import io
import re
from poke_class import Item
from functools import reduce
import pymysql
from sql import connect_db, insert_items_query, CREATE_ITEM_TABLE, create_table
url = "https://pokeapi.co/api/v2/item/?offset=0&limit=151"
loop = asyncio.get_event_loop()
q = asyncio.Queue()
items = []
async def get_json(client, url):
    async with client.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
        assert response.status == 200
        return await response.json()

async def get_sprite_response(client, url):
    async with client.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
        poke_bytes = await response.read()
        assert response.status == 200
        return poke_bytes


async def task_creator(queue, urls):
    print('Adding a task')
    for url in urls:
        await queue.put(url)

async def getter(client):
    print('Getting a task!')
    print(f'Queue size is {q.qsize()}')
    url = await q.get()
    data = await get_json(client, url)
    id_ = data['id']
    name = data['name']
    sprite = await get_sprite_response(client, data['sprites']['default'])
    effect = data['effect_entries'][0]['effect'].replace('\n', '')
    flavor_text = data['flavor_text_entries'][0]['text'].replace('\n', ' ')
    category = data['category']['name']
    item = Item(id_, name, flavor_text, sprite, effect, category)
    items.append(item)
    q.task_done()


async def retrieve_items(client, queue, producer, consumer, urls):
    producers = asyncio.create_task(producer(queue, urls))
    consumers = [asyncio.create_task(consumer(client)) for x in range(0, len(urls))]
    await asyncio.gather(producers)
    await q.join()
    for consumer in consumers:
        consumer.cancel()
    
async def main():
    async with aiohttp.ClientSession() as client:
        await retrieve_items(client, q, task_creator, getter, urls)
        
response = requests.get(url).json()
urls = [x['url'] for x in response['results']]
loop.run_until_complete(main())

create_table(CREATE_ITEM_TABLE)
insert_items_query(items)