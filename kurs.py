import random
import pandas as pd
class Character:

    def __init__(self, name, race, dnd_class, lvl, ability_scores):
        self.name = name
        self.race = race
        self.dnd_class = dnd_class
        self.ability_scores = ability_scores
        self.lvl = lvl

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
    
    @property
    def hit_dies(self):
        return self.dnd_class.hit_die + self.ability_scores.mod['CON']
        
    @property
    def ac(self):
        return 10 + self.ability_scores.mod['DEX']
    def display(self):
        print("-----General-----")
        print(f"Name: {self.name}")
        print(f"Class: {self.dnd_class.display_name}")
        print(f"Race: {self.race.display_name}")
        print(f"Level: {self.lvl}")
        print(f"HP: {self.hit_dies}")
        print(f"AC: {self.ac}")
        print(f"Proficiency Bonus: {self.proficiency_bonus}")
        print("\n-----Ability Scores-----")
        for ability, score in self.ability_scores.scores.items():
            print(f"{ability}: {score} (Modifier: {self.ability_scores.mod[ability]:+d})")
      

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
    
    @property
    def scores(self):
        return self._scores
    
    @property
    def mod(self):
        return self._mod
    
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
    
    @property
    def role(self):
        return self._role
    
    @property
    def difficulty(self):
        return self._difficulty

try:
    df_classes = pd.read_excel("game_data.xlsx", sheet_name = "CLASS" )
except Exception as e:
    print("Something went wrong:", e)
    raise

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

try:
    df_races = pd.read_excel("game_data.xlsx", sheet_name = "RACE" )
except Exception as e:
    print("Something went wrong:", e)
    raise

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

def input_value(prompt, up):
    if up:
        return input(prompt).strip().upper()
    else: 
        return input(prompt).strip()
    
def choose_score_generation_method(scores,chosen_class,type_method):
    array = [15, 14, 13, 12, 10, 8]
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    if type_method not in ["Standard Array", "Dice Roll", "Auto By Class"]:
        print("Choose one way from available")
    elif type_method == "Standard Array":
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
    elif type_method == "Dice Roll":
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
    elif type_method == "Auto By Class":
        scores.auto_by_class(chosen_class)

def save_hero(hero):
    data = [{
        "name" : hero.name,
        "display_name_race" : hero.race.display_name,
        "display_name_class" : hero.dnd_class.display_name,
        "lvl" : hero.lvl,
        "hit_die" : hero.hit_dies,
        "ac" : hero.ac,
        "proficiency_bonus" : hero.proficiency_bonus,
        "STR" : hero.ability_scores.scores["STR"],
        "DEX" : hero.ability_scores.scores["DEX"],
        "CON" : hero.ability_scores.scores["CON"],
        "INT" : hero.ability_scores.scores["INT"],
        "WIS" : hero.ability_scores.scores["WIS"],
        "CHA" : hero.ability_scores.scores["CHA"],
    }]
    df_hero = pd.DataFrame(data)
    with pd.ExcelWriter("game_data.xlsx", engine= "openpyxl", mode = "a", if_sheet_exists="replace") as writer: df_hero.to_excel(writer, sheet_name = "HERO", index = False)
if __name__ == "__main__":
    pass