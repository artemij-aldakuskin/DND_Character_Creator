import random
import pandas as pd
class Character:

    def __init__(self, name, race, dnd_class, ability_scores):
        self.name = name
        self.race = race
        self.dnd_class = dnd_class
        self.ability_scores = ability_scores
        self._lvl = 1

    @property
    def name(self):
        return self._name
   
    @name.setter
    def name(self,value):
        value = str(value).strip()
        if not value:
            raise ValueError("Name can not be empty")
        self._name = value.title()

    @property
    def lvl(self):
        return self._lvl
   
    @lvl.setter
    def lvl(self,value):
        if not isinstance(value, int):
            raise TypeError("LVL must be number")
        if not  1 <= value <= 20:
            raise ValueError("Lvl must be between 1 and 20")
        self._lvl = value
   
    def lvl_up(self):
        if self._lvl < 20:
            self._lvl = self._lvl + 1
        else: 
            raise ValueError("LVL is already 20")
      
    @property
    def proficiency_bonus(self):
        return 2 + (self._lvl - 1) // 4
      

class AbilityScores:

    def __init__(self):
        self._scores = {
            "STR": 0,
            "DEX": 0,
            "CON": 0,
            "INT": 0,
            "WIS": 0,
            "CHA": 0
       }
        self._mod = {
            "STR": 0,
            "DEX": 0,
            "CON": 0,
            "INT": 0,
            "WIS": 0,
            "CHA": 0
       } 
    
    def standard_array(self):
        array = [15, 14, 13, 12, 10, 8]
        abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for i in array:
            print("Available:", abilities)
            while True:
                value = input(f"For what characteristic {i}").upper()
                if value in abilities:
                    self._scores[value] = i
                    abilities.remove(value)
                    break
                else:
                    print("MUST BE FROM AVAILABLE!")

    def dice_roll(self):
        dices = []
        for i in range(4):
            dice = random.randint(1,6)
            dices.append(dice)
        dices.remove(min(dices))
        return sum(dices)
     
    def dice_roll_method(self):
        dice_rolls = []
        for i in range(6):
            dice_rolls.append(self.dice_roll())
        abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for i in dice_rolls:
            print("Available:", abilities)
            while True:
                value = input(f"For what characteristic {i}").upper()
                if value in abilities:
                    self._scores[value] = i
                    abilities.remove(value)
                    break
                else:
                    print("MUST BE FROM AVAILABLE!")

    def auto_by_class(self,chosen_class):
        array = [15, 14, 13, 12, 10, 8]
        for i in range(6):
            self._scores[chosen_class.abilities_prior[i]] = array[i]
    def race_bonus(self,chosen_race):
        for i in chosen_race.ability_bonus:
            self._scores[i] += chosen_race.ability_bonus[i]
           
    def modifier(self):
        for i in self._mod:
            self._mod[i] = (self._scores[i] - 10) // 2
        
     
    def choose_score_generation_method(self,chosen_class):
        while True:
            try:
                value = int(input("What way do you want to choose?\n"
                "1 - Standard Array\n"
                "2 - Dice Roll\n"
                "3 - Auto\n"))
            except ValueError:
                print("Must be a number")
                continue
            if value not in [1,2,3]:
                print("Choose one way from available")
            elif value == 1:
                self.standard_array()
                break
            elif value == 2:
                self.dice_roll_method()
                break
            elif value == 3:
                self.auto_by_class(chosen_class)
                break

            
class DndClass():
   
    def __init__ (self, key, display_name, description, role, difficulty,abilities_prior):
        self._key = key
        self._display_name = display_name
        self._description = description
        self._role = role
        self._difficulty = difficulty
        self._abilities_prior = abilities_prior

    @property
    def abilities_prior(self):
        return self._abilities_prior

df_classes = pd.read_excel("game_data.xlsx", sheet_name = "CLASS" )

ALL_CLASS = []
for _, row in df_classes.iterrows():
    prior = []
    for x in row["abilities_prior"].split(","):
        prior.append(x.strip())
    ALL_CLASS.append(DndClass(key = row["key"],
                        display_name = row["display_name"],
                        description=row["description"],
                        role = row["role"],
                        difficulty = row["difficulty"],
                        abilities_prior = prior
                        ))

class Race:
    def __init__(self, key, display_name, description, ability_bonus):
        self._key = key
        self._display_name = display_name
        self._description = description
        self._ability_bonus = ability_bonus  # dict {"STR":2, "CON":1}

    @property
    def ability_bonus(self):
        return self._ability_bonus
    
def parse_ability_bonus(text):
    result = {}
    parts = str(text).split(",")
    for part in parts:
        key,value = part.split(":")
        result[key.strip()] = int(value.strip())
    return result
      

ALL_RACES = []

df_races = pd.read_excel("game_data.xlsx", sheet_name = "RACE")
for _, row in df_races.iterrows(): #man nereikalingas _ - index 
    ALL_RACES.append(Race(key = row["key"],
                          display_name = row["display_name"],
                          description = row["description"],
                          ability_bonus = parse_ability_bonus(row["ability_bonus"])))

def choose_from_list(options, title):
    i=1
    print (f"All {title}:")
    for variants in options:
        print(f"{i}. {variants._display_name}")
        i += 1
    while True:
        try:
            value = int(input(f"Choose your options: "))
        except ValueError:
            print("Must be a number")
            continue
        if 1 <= value <= len(options):
            return options[value-1]
        else:
            print(f"Must be one of the options")

def character_creator():
    name = input("Enter character name:")
    chosen_class = choose_from_list(ALL_CLASS, "classes")
    scores = AbilityScores()
    chosen_race = choose_from_list(ALL_RACES, "races")
    scores.choose_score_generation_method(chosen_class)
    scores.race_bonus(chosen_race)
    hero = Character(name, chosen_race, chosen_class, scores)
    return hero

hero = character_creator()
def display():
    print(f"Name: {hero.name}")
    print(f"Class: {hero.dnd_class._display_name}")
    print(f"Race: {hero.race._display_name}")
    print(f"Level: {hero.lvl}")
    print(f"Proficiency Bonus: {hero.proficiency_bonus}")

display()