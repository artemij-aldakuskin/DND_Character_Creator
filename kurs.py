import random
import pandas as pd
class Character:

    def __init__(self, name, race, dnd_class, lvl, ability_scores, current_hp):
        self.name = name
        self.race = race
        self.dnd_class = dnd_class
        self.ability_scores = ability_scores
        self.lvl = lvl
        self._hp_max = dnd_class.hit_die + ability_scores.mod['CON']
        if current_hp is None:
            self.current_hp = self.hp_max
        else:
            self.current_hp = current_hp

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
            gain = self.roll_hp_gain()
            self._hp_max = self._hp_max + gain + self.ability_scores.mod["CON"]
        else: 
            raise ValueError("LVL is already 20")
      
    @property
    def proficiency_bonus(self):
        return 2 + (self._lvl - 1) // 4
    
    @property
    def hp_max(self):
        return self._hp_max
        
    @property
    def ac(self):
        return 10 + self.ability_scores.mod['DEX']
    
    @property
    def current_hp(self):
        return self._current_hp
    
    @current_hp.setter
    def current_hp(self, value):
        if not isinstance(value, int):
            raise TypeError("HP must be a number")
        elif value > self._hp_max:
            raise ValueError("Curent HP can not be more than HP max")
        elif value < 0:
            raise ValueError("Curent HP can not be negative")
        self._current_hp = value
    
    def roll_hp_gain(self):
        return random.randint(1, self.dnd_class.hit_die)
    
    def take_damage(self, amount):
        self.current_hp -= amount

    def heal(self, amount):
        self.current_hp += amount

      
class ScoreGenerationMethod:
    def generate(self, scores, chosen_class):
        raise NotImplementedError("This method must be overridden")

class StandardArrayMethod(ScoreGenerationMethod):
    def generate(self, scores, chosen_class):
        array = [15, 14, 13, 12, 10, 8]
        return array
    
class DiceRollMethod(ScoreGenerationMethod):
    def generate(self, scores, chosen_class):
        array = [scores.dice_roll() for i in range(0,6)]
        return array
    
class AutoByClassMethod(ScoreGenerationMethod):
    def generate(self, scores, chosen_class):
        scores.auto_by_class(chosen_class)
        return None
    
def create_score_method(type_of_method):
    if type_of_method == "Standard Array":
        return StandardArrayMethod()
    elif type_of_method == "Dice Roll":
        return DiceRollMethod()
    elif type_of_method == "Auto By Class":
        return AutoByClassMethod()
    else:
        return None

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
            self.scores[chosen_class.abilities_prior[i]] = array[i]
    def race_bonus(self,chosen_race):
        for i in chosen_race.ability_bonus:
            self.scores[i] += chosen_race.ability_bonus[i]
     
    def modifier(self):
        abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for i in abilities:
            self.mod[i] = (self.scores[i] - 10) // 2


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

def save_hero(hero):
    data = [{
        "name" : hero.name,
        "display_name_race" : hero.race.display_name,
        "display_name_class" : hero.dnd_class.display_name,
        "lvl" : hero.lvl,
        "hp_max" : hero.hp_max,
        "current_hp" : hero.current_hp,
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