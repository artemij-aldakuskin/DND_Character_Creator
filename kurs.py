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
    
    def display(self):
        print("-----General-----")
        print(f"Name: {self.name}")
        print(f"Class: {self.dnd_class.display_name}")
        print(f"Race: {self.race.display_name}")
        print(f"Level: {self.lvl}")
        print(f"HP: {self.dnd_class.hit_die + self.ability_scores._mod['CON']}")
        print(f"AC: {10 + self.ability_scores._mod['DEX']}")
        print(f"Proficiency Bonus: {self.proficiency_bonus}")
        print("\n-----Ability Scores-----")
        for ability, score in self.ability_scores._scores.items():
            print(f"{ability}: {score} (Modifier: {self.ability_scores._mod[ability]:+d})")
      

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
    
    def assign_score(self, value, i):
        self._scores[value] = i
    
    def dice_roll(self):
        dices = []
        for i in range(4):
            dice = random.randint(1,6)
            dices.append(dice)
        dices.remove(min(dices))
        return sum(dices)
     
    def auto_by_class(self,chosen_class):
        array = [15, 14, 13, 12, 10, 8]
        for i in range(6):
            self._scores[chosen_class.abilities_prior[i]] = array[i]
    def race_bonus(self,chosen_race):
        for i in chosen_race.ability_bonus:
            self._scores[i] += chosen_race.ability_bonus[i]
     
    def modifier(self):
        abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for i in abilities:
            self._mod[i] = (self._scores[i] - 10) // 2


class DndClass():
   
    def __init__ (self, key, display_name, description, role, difficulty, abilities_prior, hit_die):
        self._key = key
        self._display_name = display_name
        self._description = description
        self._role = role
        self._difficulty = difficulty
        self._abilities_prior = abilities_prior
        self._hit_die = hit_die

    @property
    def abilities_prior(self):
        return self._abilities_prior
    
    @property
    def display_name(self):
        return self._display_name
    
    @property
    def hit_die(self):
        return self._hit_die
        
    @property
    def description(self):
        return self._description

df_classes = pd.read_excel("game_data.xlsx", sheet_name = "CLASS" )

ALL_CLASS = []
for _, row in df_classes.iterrows():
    prior = []
    for x in row["abilities_prior"].split(","):
        prior.append(x.strip())
    ALL_CLASS.append(DndClass(key = row["key"],
                        display_name = row["display_name"],
                        description = row["description"],
                        role = row["role"],
                        difficulty = row["difficulty"],
                        abilities_prior = prior,
                        hit_die = row["hit_die"]
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
    
    @property
    def display_name(self):
        return self._display_name
    
    @property
    def description(self):
        return self._description
    
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
        print(f"{i}. {variants.display_name}\n{variants.description}")
        i += 1
    while True:
        try:
            value = int(input_value("Choose your options: ", False))
        except ValueError:
            print("Must be a number")
            continue
        if 1 <= value <= len(options):
            return options[value-1]
        else:
            print(f"Must be one of the options")

def character_creator():
    name = input_value("Enter character name:", False)
    chosen_class = choose_from_list(ALL_CLASS, "classes")
    scores = AbilityScores()
    chosen_race = choose_from_list(ALL_RACES, "races")
    choose_score_generation_method(scores,chosen_class)
    scores.race_bonus(chosen_race)
    scores.modifier()
    hero = Character(name, chosen_race, chosen_class, scores)
    return hero

def input_value(prompt, up):
    if up:
        return input(prompt).strip().upper()
    else: 
        return input(prompt).strip()
    
def choose_score_generation_method(scores,chosen_class):
    array = [15, 14, 13, 12, 10, 8]
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    while True:
        try:
            type_method = int(input_value("What way do you want to choose?\n"
            "1 - Standard Array\n"
            "2 - Dice Roll\n"
            "3 - Auto\n", False))
        except ValueError:
            print("Must be a number")
            continue
        if type_method not in [1,2,3]:
            print("Choose one way from available")
        elif type_method == 1:
            for i in array:
                print("Available:", abilities)
                while True:
                    value = input_value(f"For what characteristic {i} Abilities=", True)
                    if value in abilities:
                        scores.assign_score(value, i)
                        abilities.remove(value)
                        break
                    else:
                        print("MUST BE FROM AVAILABLE!")
            break
        elif type_method == 2:
            dice_rolls = []
            dice_rolls_show = []
            for i in range(6):
                dice_rolls.append(scores.dice_roll())
            for i in range(6):
                dice_rolls_show.append(dice_rolls[i])
            for i in dice_rolls:
                print("Available characteristics:", abilities)
                print("Available dice rolls:", dice_rolls_show)
                while True:
                    value = input_value(f"For what characteristic {i} Abilities=", True)
                    if value in abilities:
                        scores.assign_score(value, i)
                        abilities.remove(value)
                        dice_rolls_show.remove(i)
                        break
                    else:
                        print("MUST BE FROM AVAILABLE!")  
            break
        elif type_method == 3:
            scores.auto_by_class(chosen_class)
            break
hero = character_creator()
hero.display()