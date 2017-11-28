import random
from move import *
from pokedex import pokemon_entries


              
class Pokemon(object):
 
    """Attribute List
    pokedex_id   : (int)     ID of pokemon in Pokedex
    name         : (string)  name of the pokemon
    hp           : (int)     max hit point of the pokemon
    current_hp   : (int)     current hit point of the pokemon
    cp           : (int)     combat power of the pokemon
    type1        : (string)  first type of the pokemon
    type2        : (string)  second type of the pokemon
    fast_move    : (Move)    a move object that a pokemon has
    special_move : (Move)    a special move object that a pokemon has, requires to use gauge.
    weight       : (float)   how heavy a pokemon is in (kg)
    height       : (float)   how tall a pokemon is in (m)
    sex          : (string)  gender of the pokemon. M, F, or Unknown
    catch_chance : (float)     a number 0~1 representing the difficulty of capturing. 1 is easy to catch.
    """
    
    def __init__(self, id_int=0, name_str="", hp_int=1, cp_int=1, type1_str="normal",\
                  type2_str="None", fast_move=Move(), special_move=Move(), weight_float=0.0, \
                  height_float=0.0, sex_str="Unknown",catch_chance_float=1.0):
        """
        Return a Pokemon object whose name is name_str, HP is hp_int, CP is cp_int, type1 is 
        type1_str, type2 is type2_str, moves are Move objects, weight is weight_float, height is height_float, 
        gender is sex_str, chance to catch is catch_chance_float
        """
        if(hp_int>=0 and cp_int>0 and weight_float>=0.0 and height_float>=0.0 \
           and (sex_str=="M" or sex_str=="F" or sex_str=="Unknown")  \
           and 0<catch_chance_float<=1):
            self.pokedex_id  = id_int
            self.name        = name_str   
            self.hp          = hp_int
            self.current_hp  = self.hp
            self.cp          = cp_int
            self.type1       = type1_str
            self.type2       = type2_str
            self.fast_move   = fast_move
            self.special_move= special_move
            self.weight      = weight_float
            self.height      = height_float
            self.sex         = sex_str
            self.catch_chance=catch_chance_float
        else:
            print("The initialization values contain unpermitted values or strings.\
            A default instance has been created instead.")
            self.pokedex_id  = 0
            self.name        = ""   
            self.hp          = 1
            self.current_hp  = self.hp
            self.cp          = 1
            self.type1       = "normal"
            self.type2       = "None"
            self.fast_move   = Move()
            self.special_move= Move()
            self.weight      = 0.0
            self.height      = 0.0
            self.sex         = "Unknown"
            self.catch_chance= 1.0
        
    def __str__(self):
        return self.name+":"+\
               "\nSex: "+self.sex+\
               "\nCP: "+str(self.cp)+\
               "\nHP: "+str(self.current_hp)+"/"+str(self.hp)+\
               "\nType: "+self.type1+", "+self.type2+\
               "\nFast Move: "+str(self.fast_move)+"( power: "+str(self.fast_move.power)+")"+\
               "\nSpecial Move: "+str(self.special_move)+"( power: "+str(self.special_move.power)+")"+\
               "\nWeight: "+str(self.weight)+" kg"+\
               "\nHeight: "+str(self.height)+" m"
                 

    def change_name(self, new_name):
        """Change the name of the pokemon with new_name"""
        self.name=new_name

    def attack(self, move, target_pokemon):
        """The pokemon performs an attack against target_pokemon with move"""
        damage_dealt=max(1, int(move.power*(self.cp/target_pokemon.cp)))
        result = 0
        if (self.type1 == "fire" or self.type2 == "fire" ):
            if (target_pokemon.type1 == "grass" or target_pokemon.type2 == "grass" ):
                damage_dealt = 2 * damage_dealt
                print ('damage is doubled due to the type!\n')
            if (target_pokemon.type1 == "water" or target_pokemon.type2 == "water" ):
                damage_dealt = .5 * damage_dealt
                print ('damage is halved due to the type!\n')

        if (self.type1 == "water" or self.type2 == "water" ):
            if (target_pokemon.type1 == "fire" or target_pokemon.type2 == "fire" ):
                damage_dealt = 2 * damage_dealt
                print ('damage is doubled due to the type!\n')
            if (target_pokemon.type1 == "grass" or target_pokemon.type2 == "grass" ):
                damage_dealt = .5 * damage_dealt        
                print ('damage is halved due to the type!\n')

        if (self.type1 == "grass" or self.type2 == "grass" ):
            if (target_pokemon.type1 == "water" or target_pokemon.type2 == "water" ):
                damage_dealt = 2 * damage_dealt
                print ('damage is doubled due to the type!\n')
            if (target_pokemon.type1 == "fire" or target_pokemon.type2 == "fire" ):
                damage_dealt = .5 * damage_dealt
                print ('damage is halved due to the type!\n')                    

        target_pokemon.current_hp-=damage_dealt
       
        print(self.name,"used",move,"against",target_pokemon.name+"!")
        print(self.name,"dealt",str(damage_dealt),"damage to",target_pokemon.name+"!\n")
        
        if(target_pokemon.current_hp<0):
            target_pokemon.current_hp=0
            print(target_pokemon.name, "has been defeated!")
            result = 1

        return result
             
    def randomize_status(self):
        """Randomize the HP and CP of the pokemon"""
        self.cp=random.randint(10,500)
        
        self.hp=random.randint(10, max(10,1.5*self.cp//10))
        self.current_hp=self.hp
        
        self.sex=random.choice(["M","F"])

        


    def is_evolvable(self):
        return self.__class__==EvolvablePokemon


class EvolvablePokemon(Pokemon):
    
    def __init__(self, id_int, name_str, hp_int, cp_int, type1_str,\
                  type2_str, fast_move, special_move, weight_float, height_float, \
                  sex_str, catch_chance_float, evolve_to_str):
        super(self.__class__, self).__init__(id_int, name_str, hp_int, cp_int, type1_str,type2_str,\
                                             fast_move, special_move, weight_float, height_float, sex_str, catch_chance_float)
        self.evolve_to=evolve_to_str
        
    def __str__(self):
        return super(self.__class__,self).__str__()+"\nEvolve To: "+self.evolve_to
    
    def evolve(self):
        scaling_ratio=1.2
        print (self.name,"has evolved into",self.evolve_to,"!")
        pokemon_after_evolution=generate_pokemon_by_name(self.evolve_to)
        
        #Update species-based attributes
        self.pokedex_id=pokemon_after_evolution.pokedex_id
        self.name=pokemon_after_evolution.name
        self.type1=pokemon_after_evolution.type1
        self.type2=pokemon_after_evolution.type2
        self.fast_move=pokemon_after_evolution.fast_move
        self.special_move=pokemon_after_evolution.special_move
        self.height=pokemon_after_evolution.height
        self.weight=pokemon_after_evolution.weight

        #Update scaling attributes
        self.hp=int(self.hp*scaling_ratio)
        self.cp=int(self.cp*scaling_ratio)
        
        #Update current_hp
        self.current_hp=self.hp
        
        # Change the evolve_to attribute, and adjust the class when necessary.
        if(pokemon_after_evolution.is_evolvable()):
            self.evolve_to=pokemon_after_evolution.evolve_to
        else:
            self.__class__=Pokemon
            self.evolve_to=""
        
def generate_pokemon(id):
    
    """
    generate a random instance of ID id pokemon. Fixed attributes of the pokemon will be retrieved from pokedex.
    If entered ID does not exist in pokedex, return a default pokemon.
    """
    
    #Initialize a default pokemon. This will be returned at last if name is not found.
    pokemon=Pokemon()
    
    if (id in pokemon_entries.keys()):
        
        #Species-based Fixed attributes:
        name=pokemon_entries[id]["name"]
        type1=pokemon_entries[id]["type1"]
        type2=pokemon_entries[id]["type2"]
        fast_move=pokemon_entries[id]["fast_move"]
        special_move=pokemon_entries[id]["special_move"]
        catch_chance=pokemon_entries[id]["catch_chance"]
          
        #Random attributes:
        cp=random.randint(10,500)    
        hp=random.randint(10, max(10,1.5*cp//10))
        weight=round(pokemon_entries[id]["weight"]*(1+0.5*random.uniform(-1,1)),2)
        height=round(pokemon_entries[id]["height"]*(1+0.5*random.uniform(-1,1)),2)
        sex=random.choice(["M","F"])
        
        #Check whether the pokemon is evolvable.
        evolvable=pokemon_entries[id]["evolve_to"]!="None"
        
        #Instantiation of pokemon object:
        if(evolvable):
            evolve_to=pokemon_entries[id]["evolve_to"]
            pokemon=EvolvablePokemon(id,name,hp,cp,type1,type2,fast_move,special_move,weight,height,sex,catch_chance,evolve_to)
        else:
            pokemon=Pokemon(id,name,hp,cp,type1,type2,fast_move,special_move,weight,height,sex,catch_chance)
        
    else:
        print("Entered ID does not exist in Pokedex! A default pokemon will be created.")
    
    return pokemon
    
    
    
def generate_pokemon_by_name(name_str):
    """
    generate a random instance of pokemon with the given name_str. Case is insensitive.
    Fixed attributes of the pokemon will be retrieved from pokedex.
    If entered name does not exist in pokedex, return a default pokemon.
    """
    
    #Initialize a default pokemon. This will be returned at last if name is not found.
    pokemon=Pokemon()
    
    for id,pokemon_candidate in pokemon_entries.items():
        if(pokemon_candidate["name"].lower()==name_str.lower()):
            
            #Species-based Fixed attributes:
            name=pokemon_entries[id]["name"]
            type1=pokemon_entries[id]["type1"]
            type2=pokemon_entries[id]["type2"]
            fast_move=pokemon_entries[id]["fast_move"]
            special_move=pokemon_entries[id]["special_move"]
            catch_chance=pokemon_entries[id]["catch_chance"]
                
            #random attributes:
            cp=random.randint(10,500)    
            hp=random.randint(10, max(10,1.5*cp//10))
            weight=round(pokemon_entries[id]["weight"]*(1+0.5*random.uniform(-1,1)),2)
            height=round(pokemon_entries[id]["height"]*(1+0.5*random.uniform(-1,1)),2)
            sex=random.choice(["M","F"])
            
            #Check whether the pokemon is evolvable.
            evolvable=pokemon_entries[id]["evolve_to"]!="None"
                
            #Instantiation of pokemon object:
            if(evolvable):
                evolve_to=pokemon_entries[id]["evolve_to"]
                pokemon=EvolvablePokemon(id,name,hp,cp,type1,type2,fast_move,special_move,weight,height,sex,catch_chance, evolve_to)
            else:
                pokemon=Pokemon(id,name,hp,cp,type1,type2,fast_move,special_move,weight,height,sex,catch_chance)
                
    return pokemon        