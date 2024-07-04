from tkinter import Frame
from typing import Tuple
from customtkinter import *
from tkinter import *

from UI import *
from Habit import Habit
from DataBase import DataBase
from Utils import *

db = DataBase()


# Tworzenie głównego okna aplikacji


App = App_(db)
App._fg_color = "#2B2B2B"


def open_add_habit():
    def save_click():
        habit_name = name_frame.get()
        habit_tag = tag_frame.get()
        unit = unit_frame.get()
        question = question_frame.get()
        desc = desc_frame.get()

        positions = []
        for n in db.get_habits_aslist():
            positions.append(db.get_habit_pos(n))

        if max(positions) >= 9:  # max number of habits achieved
            return

        db.AddHabit(habit_name, unit, question, desc, habit_tag, pos=max(positions) + 1)
        App.refresh()
        win_add_habit.destroy()  # zamyka nowe okno

    win_add_habit = CTkToplevel(App)  # Tworzenie nowego okna
    win_add_habit.geometry("600x400")  # Ustawienie rozmiaru nowego okna
    win_add_habit.title("New Habit")  # Ustawienie tytułu nowego okna

    name_frame = LabelEntry(master=win_add_habit, text="Name")
    tag_frame = LabelEntry(master=win_add_habit, text="Tag")
    unit_frame = LabelEntry(
        master=win_add_habit, text="Unit (Input 'bool' to create a binary habit)"
    )
    question_frame = LabelEntry(master=win_add_habit, text="Question")
    desc_frame = LabelEntry(master=win_add_habit, text="Description/Notes")

    name_frame.grid(row=0, sticky="w")
    tag_frame.grid(row=1, sticky="w")
    unit_frame.grid(row=2, sticky="w")
    question_frame.grid(row=3, sticky="w")
    desc_frame.grid(row=4, sticky="w")

    # tworzy przycisk "Save" i umieszcza go w tym oknie

    save_button = CTkButton(
        master=win_add_habit, text="Save", font=("Arial", 18), command=save_click
    )
    save_button.grid(row=5, pady=10)  # Dodanie przycisku zapisu do nowego okna

    # ustawia to okno, jako pierwsze na wierzchu

    win_add_habit.grab_set()


# tworzenie przycisku "Add new habit"
buttonAddHabit = ControlButton(
    master=App.controlsFrame, label="Add habit", command=open_add_habit
)
buttonAddHabit.grid(row=0, column=0)


# loading habits from the db to the UI


App.refresh()
set_appearance_mode("dark")
App.mainloop()
