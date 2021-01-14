class Pokemon:
    def __init__(self, name, description, colour, pokedex_entry, image, _type):
        self.name = name
        self.description = description
        self.colour = colour
        self.pokedex_entry = int(pokedex_entry)
        self.image = image
        self.type = _type
    
class Item:
    def __init__(self, item_id, name, description, image, effect, category):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.image = image
        self.effect = effect
        self.category = category


  
        
