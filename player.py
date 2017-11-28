import string
import random
import database
from item import *
from pokemon import *

def validated(password_str):
    
    result=True
    num_of_lowercase=0
    num_of_uppercase=0
    num_of_symbols=0
    num_of_digits=0
    unpermitted_symbols=""
    
    for char in password_str:
        if(char in string.ascii_lowercase):
            num_of_lowercase+=1
        elif(char in string.ascii_uppercase):
            num_of_uppercase+=1
        elif(char in string.punctuation):
            num_of_symbols+=1
        elif(char in string.digits):
            num_of_digits+=1
        else:
            unpermitted_symbols+=char
    
    if(len(unpermitted_symbols)>0):
        print("Password cannot contain the following symbols:",unpermitted_symbols.replace(" ", "(whitespace)"))
        result=False
        
    if(num_of_uppercase==0):
        print("Password must contain at least one uppercase letter!")
        result=False
    
    if(num_of_symbols==0):
        print("Password must contain at least one symbol!")
        result=False
        
    if(num_of_digits==0):
        print("Password must contain at least one digit!")
        result=False
        
    if(len(password_str)<8):
        print("Password must contain at least 8 letters!")
        result=False
        
    return result
    

class Player(object):
    
    """Attribute List
    username             : (string)            unique account name of player
    __password           : (string)            private password for user to login
    level                : (int)               a number that reflects how much in-game experience the player has gained. 100 max.
    experience           : (int)               a number that a user accumulates for leveling up.
    bag                  : (Bag)               a bag containg a list of items owned by the player.
    pokemons_in_hand     : (List<Pokemon)      a list of pokemons caught by the player
    encountering_pokemon : (List<Pokemon)      a list of one pokemon that is being encountered.
    """
    
    # a list of constant numbers that represent how much experience is needed for levelling up. 
    # For example EXPERIENCE_CAP_AT_LEVEL[2] = 2000. When a player's experience reaches 2000, the player
    # level changes from Lv 2 to  Lv 3
    
    EXPERIENCE_CAP_AT_LEVEL=range(0,100000,1000)
    
    
            
    def __init__(self, username_str="-", password_str="",experience_int=0, level_int=1):
                 
        while (not validated(password_str)):
            password_str=input("Password is too simple. Please try again:")
        self.username=username_str
        self.__password=password_str
        self.experience=experience_int
        self.level=level_int
        self.bag=Bag(self)
        self.pokemons_in_hand=[]   
        self.encountering_pokemon=[]
         

                     
    def __str__(self):
        output_str="\nPlayer Status: "+str(self.username)+"     Level= "+str(self.level)+\
                   "     experience= "+str(self.experience)
        return output_str
    
    # def __repr__(self):
    #     return str(self)

    def get_password(self):
        return self.__password
    
    def change_password(self,old_password):
        MAX_TRIAL=3
        num_of_fails=0
        while(old_password!=self.__password):
            num_of_fails+=1
            if(num_of_fails<MAX_TRIAL):
                old_password=input("The current password is not entered correctly. \
                Please try again:  (You can still try "+str(MAX_TRIAL-num_of_fails)+" times)")
            else:
                print("You failed too many times. Your account is temporarily locked.")
                break
                
        if(num_of_fails<MAX_TRIAL):
            new_password=input("Please enter new password: Your password must:\n\
             1. Contain at least 8 letters.\n\
             2. Contain at least one uppercase letter, at least one symbol, and at least one digit.\n\
             3. The symbol only allows: !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n")
            
            while(not validated(new_password)):
                new_password=input("The new password is too simple. Please try a new password:")
                
            self.__password=new_password
            print("Password has been successfully changed!")
             
    def increase_experience(self, amount):
        self.experience+=int(amount)
        print(self.username,"has gained experience", amount)
        if(self.experience>=self.EXPERIENCE_CAP_AT_LEVEL[self.level]):
            while(self.experience>=self.EXPERIENCE_CAP_AT_LEVEL[self.level]):
                self.level_up()
                print(self.username,"has reached LV"+str(self.level)+"!")
                 
    def level_up(self):
        self.level+=1
        item_list=[]
        if(self.level<10):
            item_list=[PokeBall("Poke Ball"),Potion("Potion"),RazzBerry("Razz Berry"),Revive("Revive")]
        elif(self.level<20):
            item_list=[PokeBall("Great Ball"),Potion("Super Potion"),RazzBerry("Razz Berry"),Revive("Revive")]
        else:
            item_list=[PokeBall("Ultra Ball"),Potion("Hyper Potion"),RazzBerry("Great Razz Berry"),Revive("Revive")]
        for i in range(0,5):
            self.bag.add_item(random.choice(item_list))
                    
    def use_item(self,item):
        item.invoked(self)
        
    def encounter_pokemon(self,pokemon):
        self.encountering_pokemon.append(pokemon)
        print("A wild",pokemon.name,"has appeared!\n")
        print(pokemon,"\n")
    
    def enter_capture_module(self):
        
        #Randomize a pokemon object from pokemon_meta table:
        pokemon=database.get_pokemon()
        self.encounter_pokemon(pokemon)
        while(len(self.encountering_pokemon)>0):
            self.invoke_capture_menu()
        
    def invoke_capture_menu(self):
        pokemon = self.encountering_pokemon[0]
        item_option_table={0:"Escape"}
        i=1
        item_menu_str="Choose an option below (input number):\n"
        for item_name,quantity in self.bag.item_dict.items():
            item_menu_str+=str(i)+": "+item_name+" ("+str(quantity)+") "
            item_option_table[i]=item_name
            i+=1
        item_menu_str+="0:Escape from Pokemon"
        
        if("Poke Ball" not in self.bag.item_dict.keys() and\
           "Great Ball" not in self.bag.item_dict.keys() and
           "PoUltra Ball" not in self.bag.item_dict.keys()):
            print("You have no Pokeballs left! Please get some first! \n")
        
        print(item_menu_str)
        user_command=int(input())
        if(user_command in item_option_table.keys()):
            item_found=False
            for item in self.bag.inventory:
                if (item_option_table[user_command]==item.name):
                    self.use_item(item)
                    item_found=True
                    break
            if(not item_found):
                if (user_command==0):
                    print("Escaping from",pokemon.name,"....Success!") 
                    self.encountering_pokemon.remove(pokemon) 
                else:
                    print("There's no",item_option_table[user_command],"left! Choose other items")
                  
        else:
             print("You entered a wrong number! Please try again.")     
    
    def choose_player(self):
        print('\nThese are the available users to to play against:')
        persons = database.get_users()
       
        for i,person in enumerate(persons):
            if (self.username == str(person[0])):
                # print('your info is removed')
                del persons[i]
       
        for i,person in enumerate(persons):
            print(i,person[0])
        
        user_selection = int(input("\nPlease choose a user to play against:"))    
       
        if(user_selection!=0):
            person = persons[user_selection];
            print('\nYou choosed this person : '+person[0])
        return person  

    def user_choose_pokemon(self):
        person = self.choose_player()    
        pokemons = database.get_user_pokemons(person[0])
        # target_pokemon = database.get_pokemon() 
            
        if(len(pokemons) > 0):
            print('\nHere are the player pokemons:')
            
            for i, pokemon in enumerate(pokemons):
                print('(name: ' +str(pokemon.name)+', cp: '+ str(pokemon.cp)+'),( default hp: '+ str(pokemon.hp)+', current hp: '+str(pokemon.current_hp)+'),( fast move: '+str(pokemon.fast_move)+ ', power: '+str(pokemon.fast_move.power) +'),( special move: ' +  str(pokemon.special_move)+',power: '+ str(pokemon.special_move.power)+')' )
            
            num = random.randint(0,len(pokemons)-1)
            player_pokemon = pokemons[num]
        
        else:
            print( person[0]+' has no pokemons, please choose another player')
            person = self.choose_player()

        num_move = random.randint(0,1)
        
        if(num_move == 0):
            player_move = pokemon.fast_move
        elif(num_move == 1):
            player_move = pokemon.special_move
        
        return player_pokemon, player_move        

    def i_choose_pokemon(self):
        prompt_message=""
        i=1
        
        for pokemon in self.pokemons_in_hand:
            prompt_message+=str(i)+":"+pokemon.name+" (HP: "+str(pokemon.current_hp)+"/"+str(pokemon.hp)+") "
            i+=1
        
        user_selection = int(input("\nPlease choose a pokemon to use against this (enter number, 0 to go back): \n"+prompt_message+"\n"))
        
        if(user_selection!=0):
            pokemon=self.pokemons_in_hand[user_selection-1]
            print('\nYou choosed this pokemon :')
            print(pokemon) 
        
        user_selection = int(input("\nPlease choose the type of the move ( 0 to fast 1 to special ) :\n"))
        
        if(user_selection == 0):
            move = pokemon.fast_move
        elif(user_selection == 1):
            move = pokemon.special_move

        return pokemon, move    



    def enter_battle_module(self):
        # pass
        result = 0
        player_pokemon, player_move = self.user_choose_pokemon()
        
        print('\nThe player choosed this pokemon :')
        print(player_pokemon)
        # print(self.pokemons_in_hand)
        pokemon, move = self.i_choose_pokemon()      
        winner = pokemon
        # result = pokemon.attack(move,player_pokemon) 
        # result = player_pokemon.attack(player_move,pokemon) 
        while(result == 0):
            winner = pokemon
            result = pokemon.attack(move,player_pokemon)
            winner = player_pokemon
            result = player_pokemon.attack(player_move,pokemon)

        winner.new_cp = str(1.1 * winner.cp)
        winner.cp = str(winner.cp)
        winner.hp = str(winner.hp)
        database.update_cp(winner)
        print(result, winner.name,' became with cp of ' , winner.new_cp)     

    def find_candies_stardust(self):
        cp = 0
        prompt_message="\n1: Candy\n2: Star dust"
        user_selection = int(input("\nPlease choose the feed way"+prompt_message+"\n"))
        if(user_selection!=0):
            if (user_selection == 1):
                cp = random.randint(2,20)
                print('Candy is found with cp: ', str(cp) )
            elif (user_selection == 2 ):
                cp = random.randint(1,10)
                print('Star Dust is found with cp: ', str(cp) )
        return cp

    def enter_fed_mode(self):
        cp = self.find_candies_stardust()
        prompt_message=""
        i=1
        
        for pokemon in self.pokemons_in_hand:
            prompt_message+=str(i)+":"+pokemon.name+" (HP: "+str(pokemon.current_hp)+"/"+str(pokemon.hp)+") "
            i+=1
        
        user_selection = int(input("\nPlease choose a pokemon to feed (enter number, 0 to go back): \n"+prompt_message+"\n"))
        
        if(user_selection!=0):
            pokemon=self.pokemons_in_hand[user_selection-1]
            print('\nYou choosed this pokemon :')
            print(pokemon)    
            print('With cp of: ',pokemon.cp)  
        choosed_pokemon = pokemon
        choosed_pokemon.new_cp = str(choosed_pokemon.cp + cp )
        choosed_pokemon.cp = str(choosed_pokemon.cp)
        choosed_pokemon.hp = str(choosed_pokemon.hp)
        database.update_cp(choosed_pokemon)
        print('Your pokemon became with cp of ' , choosed_pokemon.new_cp)


    
    def visit_pokestop(self):
        pass                   
    
    def list_pokemons_in_hand(self):
        i=1
        option_table={}
        for pokemon in self.pokemons_in_hand:
            #print(str(i)+": "+pokemon.name,"     CP:"+str(pokemon.cp))
            print("%d: %-10s    CP: %d" % (i, pokemon.name, pokemon.cp))
            option_table[i]=pokemon
            i+=1
        
        print("\nSelect a pokemon to show details (enter number, 0 to go back):")
        user_selection=int(input())
        while(user_selection!=0):
            print(option_table[user_selection],"\n")
            user_selection=int(input("\nSelect a pokemon to show details (enter number, 0 to go back):"))
        
                                            
class Bag(object):
    
    """Attribute List
    inventory     : (dict<Item:quantity>)   An inventory of items with Item as keys and its quantity as values.
    """ 
    
    def __init__(self,owner):
        self.inventory=[]
        self.item_dict={}
        self.owner=owner
            
    def __str__(self):
          
        output_str=""
        for name,quantity in self.item_dict.items():
            output_str+=name+"("+str(quantity)+") "
        return output_str
            
    def add_item(self,item):
         # Creating a set of item names
        self.inventory.append(item)
            
        #Update a dictionary of items with item name as keys and quantity as values.
        if (item.name in self.item_dict.keys()):
            self.item_dict[item.name]+=1
        else:
            self.item_dict[item.name]=1
            
        database.update_player_item(self.owner,item,1) 
    
    
    
    def sync_items_by_name(self,item_name,quantity=1):
        item=Item()
        for i in range(quantity):
            if(item_name.find("Ball")!=-1):
                item=PokeBall(item_name)
            elif(item_name.find("Potion")!=-1):
                item=Potion(item_name)
            elif(item_name.find("Razz")!=-1):
                item=RazzBerry(item_name)
            elif(item_name.find("Revive")!=-1):
                item=Revive(item_name)
            
            # Creating a set of item names
            self.inventory.append(item)
            
            #Update a dictionary of items with item name as keys and quantity as values.
            if (item.name in self.item_dict.keys()):
                self.item_dict[item.name]+=1
            else:
                self.item_dict[item.name]=1
                      
              
    
                            
    def remove_item(self, item):
        if item.name in self.item_dict.keys():
            self.item_dict[item.name]-=1
            self.inventory.remove(item)
            
            database.update_player_item(self.owner,item,-1) 
          
                
