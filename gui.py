from tkinter import * 
from tkinter import ttk
import kurs
root = Tk()
root.title("DND character creator")
root.geometry("300x250")

def open_character_window(hero):
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
    window.protocol("WM_DELETE_WINDOW", root.destroy)

def open_class_window():
    window = Toplevel(root)
    window.title("Info About Class")
    window.geometry("250x250")

def open_race_window():
    window = Toplevel(root)
    window.title("Info About Race")
    window.geometry("250x250")

def open_characteristic_window(hero_name, chosen_race, chosen_class, scores, array):
    window = Toplevel(root)
    window.title("Choose characteristic")
    window.geometry("290x200")
    ttk.Label(window, text = "Characteristic:").grid(row=0,column=0)
    ttk.Label(window, text = "Value:").grid(row=0,column=1)
    characteristic_boxes = []
    value_boxes = []
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for i in range(1,7):
        ttk.Label(window, text=f"{abilities[i-1]}").grid(row=i, column=0)
        val_box = ttk.Combobox(window, values= array)
        val_box.grid(row = i, column = 1)
        value_boxes.append(val_box)
    create_button = ttk.Button(window, text="Apply", command=lambda:applying(hero_name, chosen_race, chosen_class,scores, value_boxes, window))
    create_button.grid(row = 8, columnspan= 2)
    window.grab_set()

def applying(hero_name, chosen_race, chosen_class,scores, value_boxes,window):
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for c in range(6):
        value = int(value_boxes[c].get())
        scores.assign_score(abilities[c],value)
    scores.race_bonus(chosen_race)
    scores.modifier()
    hero = kurs.Character(hero_name, chosen_race, chosen_class, scores)
    window.destroy()
    root.withdraw()
    open_character_window(hero)



def character_creator_gui():
    hero_name = entry.get()
    hero_class = classs.get()
    chosen_class = finding(kurs.ALL_CLASS,hero_class)
    hero_race = race.get()
    chosen_race = finding(kurs.ALL_RACES,hero_race)
    type_of_method = type_method.get()
    scores = kurs.AbilityScores()
    if type_of_method == "Standard Array":
        open_characteristic_window(hero_name, chosen_race, chosen_class, scores,[15, 14, 13, 12, 10, 8])
    elif type_of_method == "Dice Roll":
        open_characteristic_window(hero_name, chosen_race, chosen_class, scores,[scores.dice_roll() for c in range(6)])
    elif type_of_method == "Auto By Class":
        scores.auto_by_class(chosen_class)
        scores.race_bonus(chosen_race)
        scores.modifier()
        hero = kurs.Character(hero_name, chosen_race, chosen_class, scores)
        root.withdraw()
        open_character_window(hero)

    

def finding(options,what):
    i=0
    for variants in options:
        i += 1
        if variants.display_name == what:
            return options[i-1]
        
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
classs = ttk.Combobox(race_class_frame, values=[variants.display_name for variants in kurs.ALL_CLASS])
classs.grid(row = 4, column = 0)
classs_button = ttk.Button(race_class_frame, text="CLASS INFO", command=open_class_window)
classs_button.grid(row = 5, column = 0)
label = ttk.Label(race_class_frame, text = "RACE:")
label.grid(row = 3, column = 1)
race = ttk.Combobox(race_class_frame, values=[variants.display_name for variants in kurs.ALL_RACES])
race.grid(row = 4, column = 1)
race_button = ttk.Button(race_class_frame, text="RACE INFO", command=open_race_window)
race_button.grid(row = 5, column = 1)
label = ttk.Label(method_choice_frame, text = "Method:")
label.grid(row = 3, column = 0)
type_method = ttk.Combobox(method_choice_frame, values=["Standard Array", "Dice Roll", "Auto By Class"])
type_method.grid(row = 4, column = 0)
create_button = ttk.Button(method_choice_frame, text="CREATE", command=character_creator_gui)
create_button.grid(row = 5, column = 0)
root.mainloop()