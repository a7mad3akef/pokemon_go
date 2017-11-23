import random
import database

class Item(object):
    
    """Attribute List
    name         : (string)  name of item
    We are gonna add more later on
    """
    
    def __init__(self, name_str="-"):
        self.name=name_str
        

    def __repr__(self):
        return self.name

    def invoked(self,player):
        pass
    
    def perish_from(self,player):
        player.bag.remove_item(self)
        
    
class Potion(Item):
    
    def __init__(self,name):
        self.restore_amount = 0
        super(self.__class__, self).__init__(name)
        if(self.name == "Potion"):
            self.restore_amount = 20
        elif(self.name == "Super Potion"):
            self.restore_amount = 50
        elif(self.name == "Hyper Potion"):
            self.restore_amount = 200
        else:
            self.restore_amount = 0
            
    def invoked(self,player):
        
        prompt_message=""
        i=1
        for pokemon in player.pokemons_in_hand:
            prompt_message+=str(i)+":"+pokemon.name+" (HP: "+str(pokemon.current_hp)+"/"+str(pokemon.hp)+") "
            i+=1
        user_selection = int(input("Please choose a pokemon to use "+self.name+"(enter number, 0 to go back): \n"+prompt_message+"\n"))
        if(user_selection!=0):
            pokemon=player.pokemons_in_hand[user_selection-1]
            
            if(pokemon.current_hp>0):
                actually_restored_amount=min(pokemon.hp-pokemon.current_hp,self.restore_amount)
                pokemon.current_hp+=actually_restored_amount
                print(pokemon.name, "restored", actually_restored_amount, "HP!\n")
            else:
                print(self.name, "cannot be used on a pokemon with HP 0. Please use Revive!")
            self.perish_from(player)
        

class Revive(Item):
    
    def __init__(self,name):
        super(self.__class__, self).__init__(name)
        
                   
    def invoked(self,player):
        prompt_message=""
        i=1
        for pokemon in player.pokemons_in_hand:
            prompt_message+=str(i)+":"+pokemon.name+" (HP: "+str(pokemon.current_hp)+"/"+str(pokemon.hp)+") "
            i+=1
        user_selection = input("Please choose a pokemon to use "+self.name+": (1~6)\n"+prompt_message+"\n")        
        pokemon=player.pokemons_in_hand[int(user_selection)-1]
        
        if(pokemon.current_hp==0):
            pokemon.current_hp=int(pokemon.hp/2)
            print(pokemon.name, "restored", pokemon.current_hp, "HP!\n")
        else:
            print("The selected pokemon is alive. You cannot use "+self.name+" on it")
        self.perish_from(player)

class PokeBall(Item):
    
    def __init__(self,name):
        self.catch_rate = 0.50
        super(self.__class__, self).__init__(name)
        if(self.name == "Poke Ball"):
            self.catch_rate = 0.50
        elif(self.name == "Great Ball"):
            self.catch_rate = 0.70
        elif(self.name == "Ultra Ball"):
            self.catch_rate = 0.85
        else:
            self.catch_rate = 0.50
            
    def invoked(self,player):
        pokemon=player.encountering_pokemon[0]
        print("~~~~~~~~~~~~~~~~~~~~~O~~~~~~~~~~~~~~")
        catch=random.uniform(0,1)
        if(catch<self.catch_rate*pokemon.catch_chance):
            print(pokemon.name,"has been successfully captured!")
            player.pokemons_in_hand.append(pokemon)
            database.insert_player_pokemon(player,pokemon)
            player.encountering_pokemon.remove(pokemon)
        else:
            print("Oops! The",pokemon.name,"could not be caught!")
        self.perish_from(player)


class RazzBerry(Item):
    
    def __init__(self,name):
        self.catch_chance_modifier = 1.00
        super(self.__class__, self).__init__(name)
        if(self.name == "Razz Berry"):
            self.catch_chance_modifier = 1.10
        elif(self.name == "Great Razz Berry") :
            self.catch_chance_modifier = 1.20     
        else:
            self.catch_chance_modifier = 1.00
            
    def invoked(self,player):
        pokemon=player.encountering_pokemon[0]
        print(pokemon.name, "is eating the", self.name)
        pokemon.catch_chance*=self.catch_chance_modifier
        self.perish_from(player)                