from tkinter import * 
from tkinter import ttk
from collections import Counter
import kurs
import pandas as pd
root = Tk()
root.title("DND character creator")
root.geometry("300x250")

#ERROR window
def error_window(message):
    error_popup = Toplevel(root)
    error_popup.title("ERROR")
    error_popup.geometry("200x50")
    error_frame = ttk.Frame(error_popup)
    error_frame.place(relx=0.5,anchor="n")
    ttk.Label(error_frame, text="ERROR").grid(row=0, column=0)
    ttk.Label(error_frame, text=message).grid(row=1, column=0)
    error_popup.grab_set()

# Window setup
def load_hero_window():
    try: 
        df_hero = pd.read_excel("game_data.xlsx", sheet_name = "HERO" )
    except Exception as e:
        error_window(e)
        return
    if df_hero.empty:
        error_window("No saved hero found")
    else:
        load_hero(df_hero)

# Hero loading
def load_hero(df_hero):
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    hero_row = df_hero.iloc[-1]
    scores = kurs.AbilityScores()
    for ability in abilities:
        scores.assign_score(ability, int(hero_row[ability]))
    saved_class = finding(kurs.ALL_CLASS, hero_row["display_name_class"])
    if saved_class is None:
        error_window("Saved class was not found")
        return
    saved_race = finding(kurs.ALL_RACES, hero_row["display_name_race"])
    if saved_race is None:
        error_window("Saved race was not found")
        return
    scores.modifier()
    hero = kurs.Character(name = hero_row["name"],
                    race = saved_race,
                    dnd_class = saved_class,
                    lvl = int(hero_row["lvl"]),
                    ability_scores = scores,
                    current_hp = int(hero_row["current_hp"]))
    open_character_window(hero)

# Hero showing       
def open_character_window(hero):
    root.withdraw()
    character_window = Toplevel(root)
    character_window.title("Your Character")
    character_window.geometry("300x300")
    character_frame = ttk.Frame(character_window)
    character_frame.place(relx=0.5,anchor="n")
    ttk.Label(character_frame, text=f"Name: {hero.name}").grid(row=0, column=0)
    ttk.Label(character_frame, text=f"Race: {hero.race.display_name}").grid(row=1, column=0)
    ttk.Label(character_frame, text=f"Class: {hero.dnd_class.display_name}").grid(row=2, column=0)
    ttk.Label(character_frame, text=f"Level: {hero.lvl}").grid(row=3, column=0)
    ttk.Label(character_frame, text=f"HP: {hero.current_hp} / {hero.hp_max}").grid(row=4, column=0)
    ttk.Label(character_frame, text=f"AC: {hero.ac}").grid(row=5, column=0)
    ttk.Label(character_frame, text=f"Proficiency Bonus: {hero.proficiency_bonus}").grid(row=6, column=0)
    ttk.Label(character_frame, text="-----Ability Scores-----").grid(row=7, column=0)
    row = 8
    for ability, score in hero.ability_scores.scores.items():
        ttk.Label(character_frame, text=f"{ability}: {score} (Modifier: {hero.ability_scores.mod[ability]:+d})").grid(row=row, column=0)
        row += 1

    def close_character_window():
        character_window.destroy()
        root.deiconify() 

    character_window.protocol("WM_DELETE_WINDOW", close_character_window)

# Window setup
def open_class_info():
    if class_box.get() == "":
        error_window("Please select a class first")
        return
    open_class_window()

# Info windows   
def open_class_window():
    class_window = Toplevel(root)
    class_window.title("Info About Class")
    class_window.geometry("350x290")
    chosen_class = finding(kurs.ALL_CLASS,class_box.get())
    class_frame = ttk.Frame(class_window)
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

# Window setup
def open_race_info():
    if race_box.get() == "":
        error_window("Please select a race first")
        return
    open_race_window()

# Info windows
def open_race_window():
    race_window = Toplevel(root)
    race_window.title("Info About Race")
    race_window.geometry("300x250")
    chosen_race = finding(kurs.ALL_RACES,race_box.get())
    race_frame = ttk.Frame(race_window)
    race_frame.place(relx=0.5,anchor="n")
    ttk.Label(race_frame,text = f"{chosen_race.display_name}").grid(row = 0, column = 0,pady = 2)
    ttk.Label(race_frame, text = "Description:").grid(row = 1, column = 0, pady = 2)
    ttk.Label(race_frame, text = f"{chosen_race.description}").grid(row = 2, column = 0, pady = 2)
    ttk.Label(race_frame, text = "Ability:").grid(row = 3, column = 0, pady = 2) 
    i = 4
    for ability,bonus in chosen_race.ability_bonus.items():
        ttk.Label(race_frame, text = f"{ability} (+ {bonus})").grid(row = i, column = 0, pady = 1)
        i += 1

#Score selection window 
def open_score_window(hero_name, chosen_race, chosen_class, scores, array):
    score_window = Toplevel(root)
    score_window.title("Choose characteristic")
    score_window.geometry("290x200")
    ttk.Label(score_window, text = "Characteristic:").grid(row=0,column=0)
    ttk.Label(score_window, text = "Value:").grid(row=0,column=1)
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
        ttk.Label(score_window, text=f"{abilities[i-1]}").grid(row=i, column=0)
        val_box = ttk.Combobox(score_window, values= array, state="readonly")
        val_box.grid(row = i, column = 1)
        val_box.bind("<<ComboboxSelected>>", update_value_options)
        value_boxes.append(val_box)
    create_button = ttk.Button(score_window, text="Apply", command=lambda:apply_scores(hero_name, chosen_race, chosen_class,scores, value_boxes, score_window))
    create_button.grid(row = 8, columnspan= 2)
    score_window.grab_set()

#Window to aplyy score
def apply_scores(hero_name, chosen_race, chosen_class,scores, value_boxes,window):
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for box,ability in zip(value_boxes,abilities):
        if box.get() == "-" or box.get() == "":
            error_window("All values must be selected")
            return
        value = int(box.get())
        scores.assign_score(ability,value)
    scores.race_bonus(chosen_race)
    scores.modifier()
    hero = kurs.Character(hero_name, chosen_race, chosen_class, 1, scores, None)
    kurs.save_hero(hero)
    window.destroy()
    open_character_window(hero)

# Character creation windows
def character_creator_gui():
    hero_name = entry.get()
    selected_class = class_box.get()
    chosen_class = finding(kurs.ALL_CLASS,selected_class)
    if chosen_class is None:
        error_window("Class not found")
        return
    selected_race = race_box.get()
    chosen_race = finding(kurs.ALL_RACES,selected_race)
    if chosen_race is None:
        error_window("Race not found")
        return
    selected_method = method_box.get()
    if hero_name == "" or selected_class == "" or selected_race == "" or selected_method == "":
        error_window("One of the fields is empty")
        return
    scores = kurs.AbilityScores()
    score_method = kurs.create_score_method(selected_method)
    if score_method is None:
        error_window("Method not found")
        return
    generated_array = score_method.generate(scores, chosen_class)
    if generated_array is None:
        scores.race_bonus(chosen_race)
        scores.modifier()
        hero = kurs.Character(hero_name, chosen_race, chosen_class, 1, scores, None)
        kurs.save_hero(hero)
        open_character_window(hero)
    else:
        open_score_window(hero_name, chosen_race, chosen_class, scores,generated_array)
 
# Utility functions
def finding(options,display_name):
    for option in options:
        if option.display_name == display_name:
            return option
    return None

# Main layout    
main_frame = ttk.Frame(root)
main_frame.place(relx=0.5, anchor="n")
race_class_frame = ttk.Frame(root)
race_class_frame.place(relx=0.5,rely=0.2,anchor="n")
method_choice_frame = ttk.Frame(root)
method_choice_frame.place(relx=0.5,rely=0.5,anchor="n")
ttk.Label(main_frame, text = "Entry name:").grid(row = 0, columnspan= 2)
entry = ttk.Entry(main_frame)
entry.grid(row = 1, columnspan= 2)
ttk.Label(race_class_frame, text = "CLASS:").grid(row = 3, column = 0)
class_box = ttk.Combobox(race_class_frame, values=[variants.display_name for variants in kurs.ALL_CLASS], state="readonly",)
class_box.grid(row = 4, column = 0, padx = 2)
class_button = ttk.Button(race_class_frame, text="CLASS INFO", command=open_class_info)
class_button.grid(row = 5, column = 0)
ttk.Label(race_class_frame, text = "RACE:").grid(row = 3, column = 1)
race_box = ttk.Combobox(race_class_frame, values=[variants.display_name for variants in kurs.ALL_RACES], state="readonly")
race_box.grid(row = 4, column = 1)
race_button = ttk.Button(race_class_frame, text="RACE INFO", command=open_race_info)
race_button.grid(row = 5, column = 1)
ttk.Label(method_choice_frame, text = "Method:").grid(row = 3, column = 0)
method_box = ttk.Combobox(method_choice_frame, values=["Standard Array", "Dice Roll", "Auto By Class"], state="readonly")
method_box.grid(row = 4, column = 0)
create_button = ttk.Button(method_choice_frame, text="CREATE", command=character_creator_gui)
create_button.grid(row = 5, column = 0)
load_button = ttk.Button(method_choice_frame, text="SHOW LAST HERO", command=load_hero_window)
load_button.grid(row = 6, column = 0)
root.mainloop()