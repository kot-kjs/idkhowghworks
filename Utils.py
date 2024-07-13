import datetime
import random


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from DataBase import DataBase


def valiDate(day: str) -> bool:
    try:
        datetime.date.fromisoformat(day)
    except ValueError:
        return False
    finally:
        return True


# Dev Tool to generate random data
def _dev_PopulateHabit(db, h_name: str, year: str, month: str):
    if month:
        m_len = month_length(month, year)

        populated_Days = 0
        seed = random.randrange(0, 50)
        try:
            for d in range(1, m_len + 1):

                # conversion to ISO format
                d = str(d) if d >= 10 else "0" + str(d)

                val = random.randrange(0, 20) + seed
                if db.add_entry(
                    habit_name=h_name, value=val, note="", day=f"{year}-{month}-{d}"
                ):
                    populated_Days += 1

        except Exception as e:
            print(e)

    else:
        for m in range(1, 13):
            if m < 10:
                m = "0" + str(m)
            else:
                m = str(m)
            _dev_PopulateHabit(db, h_name, year, m)


def gen_db(db: DataBase, hnames: list, year):
    for i, name in enumerate(hnames):
        db.AddHabit(name, "", "", "", "", i, 0)

    for hname in db.get_habits_aslist():
        _dev_PopulateHabit(db, hname, year, "")


def add_heatmap(h, year: str):

    mon_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sept",
        "Oct",
        "Nov",
        "Dec",
    ]
    day_nums = list(range(1, 31 + 1))

    # Make a 2D array from the values from a year
    vals = []
    for i in range(1, 13):
        if i < 10:
            mon = "0" + str(i)
        else:
            mon = str(i)

        vals.append(h.get_month(month=mon, year=year))

    data = pd.DataFrame(data=vals, index=mon_names, columns=day_nums)

    plt.figure(figsize=(6, 5))
    sns.heatmap(data, linewidth=1, cmap="summer_r", square=True)
    plt.title(f"{h.name}-{year}")


def month_length(month: str, year: str):
    month = int(month)
    if int(month) >= 10:
        month = str(month)
    else:
        month = "0" + str(month)

    if (int(month) not in range(1, 13)) or (len(str(year)) != 4):
        raise ValueError(
            f"Incorrect month or year provided. Should be MM and YYYY, instead got {month} and {year}"
        )

    month_len = 31
    if month == "02":
        if int(year) % 4 == 0:
            month_len = 29
        else:
            month_len = 28
    elif month in ("04", "06", "09", "11"):
        month_len = 30

    return month_len


def int_to_pos(int_) -> tuple:  # for easier widget grid management
    x = int_ % 3
    y = int(int_ / 3)
    return (x, y)
