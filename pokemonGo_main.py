from pokemon import *
from player import *
from item import  *
import sqlite3
import database

def main_menu(player):
    menu_str="\nSelect an option below (input number 0~5):\n1: Catch pokemon\n"+\
             "2: Fight against another player\n"+\
             "3: Visit PokeStop\n"+\
             "4: View items in bag\n"+\
             "5: View pokemons in hand\n"+\
             "6: Find candies & stardut\n"+\
             "0: Save and Exit\n"
    print(menu_str)
    option=int(input())
    while (option!=0):
        if(option==1):
            player.enter_capture_module()
        elif(option==2):
            player.enter_battle_module()
        elif(option==3):
            player.visit_pokestop()
        elif(option==4):
            print(player.username+"'s bag:\n")
            print(player.bag)
        elif(option==5):
            player.list_pokemons_in_hand()
        elif(option==6):
            player.enter_fed_mode()    
        else:
            print("PLease only enter a number between 0~3.\n")
        option=int(input(menu_str))
    database.save_progress(player)
    print("Exiting....See you next time!\n")
    
    



def login_module():
    player_name=input("input your name:\n")
    user_exist=database.check_username_in_database(player_name)
    if(user_exist):
        user_name, user_password, level, experience = database.get_user_info(player_name)
        while(input("Please enter your password:")!=user_password):
            print("Wrong password! Please Try again!")
        player=Player(user_name,user_password,experience,level)
        database.sync_from_db(player)
        print("\nWelcome back! Login completed.\n") 
    else:
        password=input("Welcome new player! Please create your password:")
        player=Player(player_name,password,0,1)
        database.create_new_player(player)
        for i in range(10):
            player.bag.add_item(PokeBall("Poke Ball"))
            player.bag.add_item(Potion("Potion"))
        print("Welcome! You will start a new journey.")
        print("You are given 10 Poke Balls and 10 Potions as starting items.")
    return player    




        
new_player=login_module()            
main_menu(new_player)

"""            
player=Player(input("input your name:\n"),input("input password:\n"))

for i in range(5):
    player.bag.add_item(PokeBall("Ultra Ball"))
    player.bag.add_item(Potion("Potion"))
    player.bag.add_item(Revive("Revive"))
    player.bag.add_item(RazzBerry("Razz Berry"))
"""

'''
pokemon1=generate_pokemon(1)
player.pokemons_in_hand.append(pokemon1)
pokemon2=generate_pokemon(4)
player.pokemons_in_hand.append(pokemon2)
pokemon3=generate_pokemon_by_name("Pikachu")
player.encounter_pokemon(pokemon3)

print(pokemon1,"\n")
print(pokemon2,"\n")

pokemon3.attack(pokemon3.move, pokemon1)
pokemon2.current_hp=0

print(pokemon1,"\n")
print(pokemon2,"\n")


while(len(player.bag.inventory)>0):
    item_menu(player)
'''


