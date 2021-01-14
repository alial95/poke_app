import tkinter as tk
import pymysql
from random import choice, sample
from sql import connect_db, read_pokemon_query, read_items_query
import io
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
from tkinter import PhotoImage

pokemon = read_pokemon_query()
items = read_items_query()
def get_pokemon(poke):
    window = tk.Toplevel()
    text_frame = tk.Frame(window)
    text_frame.grid(row=0, column=0)
    label = tk.Label(text_frame, text=poke.name.title())
    label.pack()
    description = tk.Label(text_frame, text=poke.colour)
    description.pack()
    poke_image = Image.open(io.BytesIO(poke.image))
    new_image = poke_image.resize((100, 100), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(new_image)
    button = tk.Button(text_frame, image=ph)
    button.image = ph
    button.pack()
def get_item(item):
    window = tk.Toplevel()
    text_frame = tk.Frame(window)
    text_frame.grid(row=0, column=0)
    label = tk.Label(text_frame, text=item.name.title())
    label.pack()
    description = tk.Label(text_frame, text=item.description)
    description.pack()
    item_image = Image.open(io.BytesIO(item.image))
    new_image = item_image.resize((100, 100), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(new_image)
    button = tk.Button(text_frame, image=ph)
    button.image = ph
    button.pack()
def display_pokemon(pokemon):
    new_window = tk.Toplevel()
    counter = 1
    top_frame = tk.Canvas(new_window)
    top_frame.pack()
    label = tk.Label(top_frame, text='Click a pokemon to find out more information about them!')
    label.grid(row=0, column= 5,columnspan=5, sticky='NESW')
    for i in range(10):
        for j in range(15):
            frame = tk.Frame(
                master=top_frame,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i+1, column=j+1, sticky='NESW')
            poke_image = Image.open(io.BytesIO(pokemon[counter].image))
            new_image = poke_image.resize((55, 45), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(new_image)
            button = tk.Button(frame, image=ph, command= lambda name=pokemon[counter]: get_pokemon(name))
            label = tk.Label(frame, text=pokemon[counter].name.title())
            label.pack()
            button.image = ph
            button.pack()
            counter += 1
def display_congratulations(poke):
    window = tk.Toplevel()
    window.geometry("350x350")
    frame = tk.Frame(window)
    frame.pack()
    item_image = Image.open(io.BytesIO(poke.image))
    new_image = item_image.resize((300, 250), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(new_image)
    label_message = tk.Label(frame, text=f'Well done!!! You guessed correctly. The answer was {poke.name}!')
    label_message.pack()
    button = tk.Button(frame, image=ph)
    button.image = ph
    button.pack()

def pokemon_game(pokemon):
    window = tk.Toplevel()
    window.geometry("350x350")
    frame = tk.Frame(window)
    frame.pack()
    poke_answers = sample(pokemon, k=4)
    poke = choice(poke_answers)
    poke_answers.remove(poke)
    image = Image.open(io.BytesIO(poke.image)).convert('L').resize((200, 200), Image.ANTIALIAS)
    flipped = ImageOps.invert(image)
    filtered = flipped.filter(ImageFilter.GaussianBlur(radius=2))
    enhancer = ImageEnhance.Contrast(filtered)
    factor = 3.6
    output = enhancer.enhance(factor)
    ph = ImageTk.PhotoImage(output)
    label = tk.Label(frame, text='Whos that pokemon?')
    label.pack()
    label.config(image=ph, compound= tk.BOTTOM)
    label.image = ph
    button_frames = tk.Frame(window)
    button_frames.pack()
    button_positions = sample([1, 2, 3, 4], k=4)
    answer_button = tk.Button(button_frames, text=poke.name.title(), command= lambda: [display_congratulations(poke), window.destroy()])
    answer_button.grid(row=0, column=button_positions[0])
    button_1 = tk.Button(button_frames, text=poke_answers[0].name.title(), command= lambda: [window.destroy()])
    button_1.grid(row=0, column=button_positions[1])
    button_2 = tk.Button(button_frames, text=poke_answers[1].name.title(), command= lambda: [window.destroy()])
    button_2.grid(row=0, column=button_positions[2])
    button_3 = tk.Button(button_frames, text=poke_answers[2].name.title(), command= lambda: [window.destroy()])
    button_3.grid(row=0, column=button_positions[3])



def display_items(items):
    new_window = tk.Toplevel()
    counter = 1
    top_frame = tk.Canvas(new_window)
    top_frame.pack()
    label = tk.Label(top_frame, text='Click a item to find out more information about them!')
    label.grid(row=0, column= 5,columnspan=5, sticky='NESW')
    for i in range(10):
        for j in range(15):
            frame = tk.Frame(
                master=top_frame,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i+1, column=j+1, sticky='NESW')
            item_image = Image.open(io.BytesIO(items[counter].image))
            new_image = item_image.resize((55, 45), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(new_image)
            button = tk.Button(frame, image=ph, command= lambda name=items[counter]: get_item(name))
            label = tk.Label(frame, text=items[counter].name.title())
            label.pack()
            button.image = ph
            button.pack()
            counter += 1
new = tk.Tk()
new.title("ALI'S POKEDEX")
new.geometry('250x250')
text_frame = tk.Frame(new)
label = tk.Label(new, text='Welcome to Alis Pokedex!')
label.pack()
button_frame = tk.Frame(new)
button_frame.pack(fill=tk.BOTH)
button_1 = tk.Button(button_frame, text='View the Pokemon!', command = lambda: display_pokemon(pokemon), padx=40)
button_2 = tk.Button(button_frame,text='View some items', command=lambda: display_items(items), padx=40)
button_3 = tk.Button(button_frame,text='Play whose that pokemon', command=lambda: pokemon_game(pokemon), padx=40)
button_1.pack(fill=tk.BOTH)
button_2.pack(fill=tk.BOTH)
button_3.pack(fill=tk.BOTH)
new.mainloop()