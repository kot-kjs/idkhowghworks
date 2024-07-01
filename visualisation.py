import matplotlib.pyplot as plt

from Habit import Habit

import pandas as pd
import seaborn as sns
import numpy as np


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


def v_habit_plot(
    habits_to_plot: list,
    month: str,
    year: str,
):

    if type(habits_to_plot) is not list:
        habits_to_plot = [habits_to_plot]

    day_nums = list(range(1, 31 + 1))

    for h in habits_to_plot:
        day_vals = h.get_month(month, year)
        plt.plot(day_nums, day_vals, marker="o", linestyle="-", label=h.name)

    plt.legend(loc="upper left")

    if len(habits_to_plot) > 1:
        plt.title(f"Comparison of {len(habits_to_plot)} habits - {month}/{year}")
    else:
        plt.title(habits_to_plot[0].name + f" {month}/{year}")


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

    fig, ax = plt.subplots(figsize=(10, 3))

    # plt.figure(figsize=(6, 2))
    sns.heatmap(data, linewidth=1, cmap="summer_r", square=True, ax=ax)
    plt.title(f"{h.name}-{year}")
