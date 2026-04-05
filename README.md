# DnD Character Creator

A Python-based Dungeons & Dragons character creator with a graphical user interface.

## Features

- Character creation (name, race, class)
- Ability score generation:
  - Standard Array
  - Dice Roll
  - Auto assignment based on class
- Automatic race bonuses
- Character sheet display (HP, AC, modifiers, etc.)
- Data loaded from Excel (classes and races)
- Simple GUI built with Tkinter

## Technologies

- Python
- Tkinter (GUI)
- Pandas (Excel data handling)
- OpenPyXL

## How to run

1. Install dependencies:
pip install pandas openpyxl

2. Make sure `game_data.xlsx` is in the project folder

3. Run the GUI:
python gui.py

## Project structure

- `kurs.py` — core logic (Character, AbilityScores, Race, Class)
- `gui.py` — graphical interface
- `game_data.xlsx` — data for classes and races

## Project goal

This project was created as part of an OOP course to practice:

- Object-Oriented Programming
- Working with external data (Excel)
- Building a simple GUI application
- Structuring a real-world project

## Status

Work in progress