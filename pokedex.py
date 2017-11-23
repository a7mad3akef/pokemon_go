from pokemon import *
from move import Move

#Use file to read in pokedex:
pokemon_entries ={}

my_file=open("pokedex.csv","r")
my_file.readline() # skip the first line
for line in my_file:
    pokedex_id, name, type1, type2, weight, height, move_name, move_power,evolve_to, catch_chance = line.strip().split(",")
    move=Move(move_name,float(move_power))
    pokemon_entry={}
    pokemon_entry["pokedex_ID"]=int(pokedex_id)
    pokemon_entry["name"]=name
    pokemon_entry["type1"]=type1
    pokemon_entry["type2"]=type2
    pokemon_entry["weight"]=float(weight)
    pokemon_entry["height"]=float(height)
    pokemon_entry["move"]=move
    pokemon_entry["evolve_to"]=evolve_to
    pokemon_entry["catch_chance"]=float(catch_chance)
    
    pokemon_entries[int(pokedex_id)]=pokemon_entry
    
my_file.close()
    
    

