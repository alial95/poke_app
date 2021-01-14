import pymysql
from contextlib import contextmanager
from poke_class import Pokemon, Item
import os
from dotenv import load_dotenv
load_dotenv()
password = os.getenv('MYSQL_PASSWORD')
CREDENTIALS = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": password,
    "db": "pokedex"
}
MAKE_DB_CREDENTIALS = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
}
CREATE_POKEDEX_DATABASE = 'CREATE DATABASE IF NOT EXISTS POKEDEX;'
CREATE_POKEMON_TABLE = 'CREATE TABLE IF NOT EXISTS POKEMON (pokedex_entry INT NOT NULL PRIMARY KEY, name VARCHAR(100), colour VARCHAR(100), description VARCHAR(100), image BLOB, type VARCHAR(100));'
CREATE_ITEM_TABLE = 'CREATE TABLE IF NOT EXISTS ITEMS (item_id INT NOT NULL PRIMARY KEY, name VARCHAR(100), description VARCHAR(100), image BLOB, effect VARCHAR(100), category VARCHAR(100));'
@contextmanager
def connect_db(credentials=CREDENTIALS):
    connection = pymysql.connect(**credentials)
    try:
        yield connection
    finally:
        connection.close()
def create_database(query):
    with connect_db(MAKE_DB_CREDENTIALS) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

def create_table(query):
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

def insert_pokemon_query(lst):
    with connect_db() as conn:
        with conn.cursor() as cursor:
            for pokemon in lst:
                cursor.execute("""INSERT IGNORE INTO pokemon (pokedex_entry, name, colour, description, image, type) VALUES (%s,%s,%s,%s,%s,%s)""",
                (pokemon.pokedex_entry, pokemon.name, pokemon.colour, pokemon.description, pokemon.image, pokemon.type))
                conn.commit()
        
def read_pokemon_query():
    pokemon_list = []
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT pokedex_entry, name, colour, description, image, type FROM pokemon")
            rows = cursor.fetchall()
            for row in rows:
                pokemon = Pokemon(row[1], row[2], row[3], row[0], row[4], row[5])
                pokemon_list.append(pokemon)
    return pokemon_list



def insert_items_query(lst):
    with connect_db() as conn:
        with conn.cursor() as cursor:
            for item in lst:
                cursor.execute("""INSERT IGNORE INTO items (item_id, name, description, image, effect, category) VALUES (%s,%s,%s,%s,%s,%s)""",
                (item.item_id, item.name, item.description, item.image, item.effect, item.category))
                conn.commit()

def read_items_query():
    item_list = []
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT item_id, name, description, image, effect, category FROM items")
            rows = cursor.fetchall()
            for row in rows:
                item = Item(row[0], row[1], row[2], row[3], row[4], row[5])
                item_list.append(item)
    return item_list



    
