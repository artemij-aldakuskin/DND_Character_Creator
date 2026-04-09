from tkinter import * 
from tkinter import ttk
from collections import Counter
import kurs
import pandas as pd
root = Tk()
root.title("DND character creator")
root.geometry("300x250")
def error_window(message):
    window = Toplevel(root)
    window.title("ERROR")
    window.geometry("200x50")
    frame = ttk.Frame(window)
    frame.place(relx=0.5,anchor="n")
    ttk.Label(frame, text="ERROR").grid(row=0, column=0)
    ttk.Label(frame, text=message).grid(row=1, column=0)
    window.grab_set()

def load_hero_window():
    try: 
        df_hero = pd.read_excel("game_data.xlsx", sheet_name = "HERO" )
    except Exception as e:
        error_window(e)
        raise
    if df_hero.empty:
        error_window("No saved hero found")
    else:
        load_hero(df_hero)

def load_hero(df_hero):
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    row = df_hero.iloc[-1]
    scores = kurs.AbilityScores()
    for ability in abilities:
        scores.assign_score(ability, int(row[ability]))
    dnd_class_from_ex = finding(kurs.ALL_CLASS, row["display_name_class"])
    if dnd_class_from_ex is None:
        error_window("Saved class was not found")
        return
    race_from_ex = finding(kurs.ALL_RACES, row["display_name_race"])
    if race_from_ex is None:
        error_window("Saved race was not found")
        return
    scores.modifier()
    hero = kurs.Character(name = row["name"],
                    race = race_from_ex,
                    dnd_class = dnd_class_from_ex,
                    lvl = int(row["lvl"]),
                    ability_scores= scores)
    open_character_window(hero)
       
def open_character_window(hero):
    root.withdraw()
    window = Toplevel(root)
    window.title("Your Character")
    window.geometry("300x300")
    character_frame = ttk.Frame(window)
    character_frame.place(relx=0.5,anchor="n")
    ttk.Label(character_frame, text=f"Name: {hero.name}").grid(row=0, column=0)
    ttk.Label(character_frame, text=f"Race: {hero.race.display_name}").grid(row=1, column=0)
    ttk.Label(character_frame, text=f"Class: {hero.dnd_class.display_name}").grid(row=2, column=0)
    ttk.Label(character_frame, text=f"Level: {hero.lvl}").grid(row=3, column=0)
    ttk.Label(character_frame, text=f"HP: {hero.hit_dies}").grid(row=4, column=0)
    ttk.Label(character_frame, text=f"AC: {hero.ac}").grid(row=5, column=0)
    ttk.Label(character_frame, text=f"Proficiency Bonus: {hero.proficiency_bonus}").grid(row=6, column=0)
    ttk.Label(character_frame, text="-----Ability Scores-----").grid(row=7, column=0)
    row = 8
    for ability, score in hero.ability_scores.scores.items():
        ttk.Label(character_frame, text=f"{ability}: {score} (Modifier: {hero.ability_scores.mod[ability]:+d})").grid(row=row, column=0)
        row += 1

    def close_character_window():
        window.destroy()
        root.deiconify() 

    window.protocol("WM_DELETE_WINDOW", close_character_window)

def open_class_info():
    if classs.get() == "":
        error_window("Please select a class first")
        return
    open_class_window()

def open_class_window():
    window = Toplevel(root)
    window.title("Info About Class")
    window.geometry("350x290")
    chosen_class = finding(kurs.ALL_CLASS,classs.get())
    class_frame = ttk.Frame(window)
    class_frame.place(relx=0.5,anchor="n")
    ttk.Label(class_frame,text = f"{chosen_class.display_name}").grid(row = 0, column = 0)
    ttk.Label(class_frame, text = f"HP: {chosen_class.hit_die}").grid(row = 1, column = 0, pady=2)
    ttk.Label(class_frame, text = f"Role: {chosen_class.role}").grid(row = 2, column = 0, pady=2)
    ttk.Label(class_frame, text = "Description:").grid(row = 3, column = 0,pady = 2)
    ttk.Label(class_frame, text = f"{chosen_class.description}").grid(row = 4, column = 0,pady = 2)
    ttk.Label(class_frame, text = f"Difficulty: {chosen_class.difficulty}").grid(row = 5, column = 0, pady = 2)
    ttk.Label(class_frame, text = "Abilities Priority:").grid(row = 6, column = 0, pady = 2)
    i = 7
    for ability in chosen_class.abilities_prior:
        ttk.Label(class_frame, text = f"{ability}").grid(row = i, column = 0, pady = 1)
        i += 1

def open_race_info():
    if race.get() == "":
        error_window("Please select a race first")
        return
    open_race_window()

def open_race_window():
    window = Toplevel(root)
    window.title("Info About Race")
    window.geometry("300x250")
    chosen_race = finding(kurs.ALL_RACES,race.get())
    race_frame = ttk.Frame(window)
    race_frame.place(relx=0.5,anchor="n")
    ttk.Label(race_frame,text = f"{chosen_race.display_name}").grid(row = 0, column = 0,pady = 2)
    ttk.Label(race_frame, text = "Description:").grid(row = 1, column = 0, pady = 2)
    ttk.Label(race_frame, text = f"{chosen_race.description}").grid(row = 2, column = 0, pady = 2)
    ttk.Label(race_frame, text = "Ability:").grid(row = 3, column = 0, pady = 2) 
    i = 4
    for ability,bonus in chosen_race.ability_bonus.items():
        ttk.Label(race_frame, text = f"{ability} (+ {bonus})").grid(row = i, column = 0, pady = 1)
        i += 1

def open_characteristic_window(hero_name, chosen_race, chosen_class, scores, array):
    window = Toplevel(root)
    window.title("Choose characteristic")
    window.geometry("290x200")
    ttk.Label(window, text = "Characteristic:").grid(row=0,column=0)
    ttk.Label(window, text = "Value:").grid(row=0,column=1)
    value_boxes = []
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    array = sorted(array)
    def update_value_options(event=None):
        total_counts = Counter(str(v) for v in array)
        for box in value_boxes:
            selected = [b.get() for b in value_boxes if b != box and b.get() != ""]
            selected_counts = Counter(selected)
            available = []
            for v in sorted(array):
                v_str = str(v)
                if selected_counts[v_str] < total_counts[v_str]:
                    available.append(v)
            box["values"] =["-"]+ available  

    for i in range(1,7):
        ttk.Label(window, text=f"{abilities[i-1]}").grid(row=i, column=0)
        val_box = ttk.Combobox(window, values= array, state="readonly")
        val_box.grid(row = i, column = 1)
        val_box.bind("<<ComboboxSelected>>", update_value_options)
        value_boxes.append(val_box)
    create_button = ttk.Button(window, text="Apply", command=lambda:applying(hero_name, chosen_race, chosen_class,scores, value_boxes, window))
    create_button.grid(row = 8, columnspan= 2)
    window.grab_set()

def applying(hero_name, chosen_race, chosen_class,scores, value_boxes,window):
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for box,ability in zip(value_boxes,abilities):
        if box.get() == "-" or box.get() == "":
            error_window("All values must be selected")
            return
        value = int(box.get())
        scores.assign_score(ability,value)
    scores.race_bonus(chosen_race)
    scores.modifier()
    hero = kurs.Character(hero_name, chosen_race, chosen_class, 1, scores)
    kurs.save_hero(hero)
    window.destroy()
    open_character_window(hero)



def character_creator_gui():
    hero_name = entry.get()
    hero_class = classs.get()
    chosen_class = finding(kurs.ALL_CLASS,hero_class)
    if chosen_class == None:
        error_window("Class not found")
        return
    hero_race = race.get()
    chosen_race = finding(kurs.ALL_RACES,hero_race)
    if chosen_race == None:
        error_window("Race not found")
        return
    type_of_method = type_method.get()
    if hero_name == "" or hero_class == "" or hero_race == "" or type_of_method == "":
        error_window("One of the fields is empty")
        return
    scores = kurs.AbilityScores()
    if type_of_method == "Standard Array":
        open_characteristic_window(hero_name, chosen_race, chosen_class, scores,[15, 14, 13, 12, 10, 8])
    elif type_of_method == "Dice Roll":
            open_characteristic_window(hero_name, chosen_race, chosen_class, scores,[scores.dice_roll() for c in range(6)])
    elif type_of_method == "Auto By Class":
        scores.auto_by_class(chosen_class)
        scores.race_bonus(chosen_race)
        scores.modifier()
        hero = kurs.Character(hero_name, chosen_race, chosen_class, 1, scores)
        kurs.save_hero(hero)
        open_character_window(hero)

    

def finding(options,what):
    i=0
    for variants in options:
        i += 1
        if variants.display_name == what:
            return options[i-1]
    return None
        
frame = ttk.Frame(root)
frame.place(relx=0.5, anchor="n")
race_class_frame = ttk.Frame(root)
race_class_frame.place(relx=0.5,rely=0.2,anchor="n")
method_choice_frame = ttk.Frame(root)
method_choice_frame.place(relx=0.5,rely=0.5,anchor="n")
label = ttk.Label(frame, text = "Entry name:")
label.grid(row = 0, columnspan= 2)
entry = ttk.Entry(frame)
entry.grid(row = 1, columnspan= 2)
label = ttk.Label(race_class_frame, text = "CLASS:")
label.grid(row = 3, column = 0)
classs = ttk.Combobox(race_class_frame, values=[variants.display_name for variants in kurs.ALL_CLASS], state="readonly",)
classs.grid(row = 4, column = 0, padx = 2)
classs_button = ttk.Button(race_class_frame, text="CLASS INFO", command=open_class_info)
classs_button.grid(row = 5, column = 0)
label = ttk.Label(race_class_frame, text = "RACE:")
label.grid(row = 3, column = 1)
race = ttk.Combobox(race_class_frame, values=[variants.display_name for variants in kurs.ALL_RACES], state="readonly")
race.grid(row = 4, column = 1)
race_button = ttk.Button(race_class_frame, text="RACE INFO", command=open_race_info)
race_button.grid(row = 5, column = 1)
label = ttk.Label(method_choice_frame, text = "Method:")
label.grid(row = 3, column = 0)
type_method = ttk.Combobox(method_choice_frame, values=["Standard Array", "Dice Roll", "Auto By Class"], state="readonly")
type_method.grid(row = 4, column = 0)
create_button = ttk.Button(method_choice_frame, text="CREATE", command=character_creator_gui)
create_button.grid(row = 5, column = 0)
create_button = ttk.Button(method_choice_frame, text="SHOW LAST HERO", command=load_hero_window)
create_button.grid(row = 6, column = 0)
root.mainloop()