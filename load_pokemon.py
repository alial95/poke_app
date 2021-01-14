import signal
import sys
import asyncio
import aiohttp
import json
import requests
from PIL import Image, ImageTk
from tkinter import PhotoImage
import tkinter as tk
import io
import re
from poke_class import Pokemon
from functools import reduce
import pymysql
from sql import CREDENTIALS, CREATE_POKEMON_TABLE, connect_db, insert_pokemon_query, create_table, CREATE_POKEDEX_DATABASE, MAKE_DB_CREDENTIALS, create_database
lst = []
lst2 = []
lst3 = []
pokemon = []
loop = asyncio.get_event_loop()
q = asyncio.Queue()
url = "https://pokeapi.co/api/v2/pokemon-species/?offset=0&limit=151"
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
    print('Getting a task')
    print(f'Queue size is {q.qsize()}')
    url = await q.get()
    data = await get_json(client, url)
    sprite_url = await get_json(client, data['varieties'][0]['pokemon']['url'])
    spriteurl = sprite_url['sprites']['front_default']
    description = data["flavor_text_entries"][0]['flavor_text']
    colour = data['color']['name']
    pokedex = data['id']
    _type = sprite_url['types'][0]['type']['name']
    sprite = await get_sprite_response(client,spriteurl)
    pokemon_data = Pokemon(data['name'], description, colour, pokedex, sprite, _type)
    pokemon.append(pokemon_data)
    print(len(pokemon))
    q.task_done()
    print('task finished')

async def retrieve_poke(client, q, producer, consumer, urls):
    producers = asyncio.create_task(producer(q, urls))
    consumers = [asyncio.create_task(consumer(client)) for x in range(0, len(urls))]
    await asyncio.gather(producers)
    await q.join()
    for consumer in consumers:
        consumer.cancel()

async def main():
    async with aiohttp.ClientSession(loop=loop) as client:
        await retrieve_poke(client, q, task_creator, getter, urls)

data = requests.get(url).json()
urls = [x['url'] for x in data['results']]
loop.run_until_complete(main())
create_database(CREATE_POKEDEX_DATABASE)
create_table(CREATE_POKEMON_TABLE)
insert_pokemon_query(pokemon)

