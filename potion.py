from item import Item

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
            prompt_message+=str(i)+":"+pokemon.name
            i+=1
        user_selecition = input("Please choose a pokemon to use: (1~6)\n"+prompt_message+"\n")
        
           
        pokemon=player.pokemons_in_hand[int(user_selecition)-1]
        actually_restored_amount=min(pokemon.hp-pokemon.current_hp,self.restore_amount)
        pokemon.current_hp+=actually_restored_amount
        print(pokemon.name, "restored", actually_restored_amount, "HP!\n")
    
    