from Habit import Habit
from DataBase import DataBase
from Utils import *

from datetime import date

import matplotlib.pyplot as plt


from visualisation import *

# Anything below is for testing purposes and may or may not be of any use in the final build

# Dev version only
from Utils import _dev_PopulateHabit

#

db = DataBase()


def add_habit():
    print("Enter habit name: ")
    h_name = input()
    if h_name == None:
        raise ValueError("Habit name not provided")
    print("unit: ")
    h_unit = input()
    print("question/prompt: ")
    h_question = input()
    print("Description: ")
    h_desc = input()

    if db.AddTable(h_name, h_unit, h_question, h_desc):
        print(f"Created {h_name}")
    else:
        print(
            "Failed to create habit. There may already exist another one of such name"
        )


def add_entry():
    print("Enter h_name:")
    h_name = input()
    print("Date: (YYYY-MM-DD)(enter to save as today)")
    day = input()
    valiDate(day)

    if day == "":
        day = date.today()
    if db.has_table_value(f"{h_name}_logs", "day", day):
        print("There already exists an entry for that day.")
        return
    print("enter value:")
    val = input()
    print("Note: (enter empty to skip)")
    note = input()

    db.add_entry(h_name, val, note, day)


def main():

    # h_unit = "min"
    # h_name = "building"
    # h_question = "how much time have u invested in minecraft"
    # h_desc = ""
    # h_tag = "idk"
    # db.AddHabit(h_name, h_unit, h_question, h_desc, h_tag, )
    # _dev_PopulateHabit(db, h_name, "2024", "")
    # gen_db(
    #     db,
    #     [
    #         "building",
    #         "crying",
    #         "eating",
    #         "shitting",
    #         "swearing",
    #         "running",
    #         "writing",
    #         "meditating",
    #         "studying",
    #     ],
    #     "2024",
    # )

    # db.delete_habit("swearing")
    # db.modify_habit_param("writing", "description", "Only rhymed writing counts")

    # h = Habit(db, "crying")
    db.delete_entry("swearing", "2024-07-13")
    # add_heatmap(h, "2024")


main()
