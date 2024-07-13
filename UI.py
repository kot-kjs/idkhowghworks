from tkinter import *
from customtkinter import *
from Habit import Habit

from Utils import *
from DataBase import DataBase
from datetime import date


# custom "button" class that integrates the habit class and the ctk button (hopefully)


class HabitWidget(CTkButton):
    def __init__(self, db: DataBase, habit_name, habit_tag, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habit_name = habit_name
        self.app = app
        self.db = db
        self.habit = Habit(db, habit_name)
        self.habit_tag = self.habit.tag
        if self.habit_tag == "":
            self.habit_tag = habit_tag

        if self.habit_tag in ("varied", "daily", "repeating"):
            self.configure(command=self.toggle)
            if self.habit_tag in ("daily", "varied") and self.db.habit_has_entry(
                self.habit_name, "day", date.today()
            ):
                self.configure(state="disabled")
                self.configure(fg_color="#144870")

        self.bind("<Button-3>", lambda event: self.right_btn_menu_popup(event))

    def toggle(self):  # rewrite it
        if self._state == "normal":
            if self.habit_tag == "daily":
                self.configure(state="disabled")
                self.configure(fg_color="#144870")
                self.db.add_entry(self.habit_name, self.habit.goal, "")

            elif self.habit.tag == "repeating":
                date_ = date.today()
                if self.db.habit_has_entry(self.habit_name, "day", date_):
                    old_val = self.db.get_habit_entry_value(self.habit_name, date_)
                    print(old_val)
                    self.db.modify_habit_entry(
                        self.habit_name, date_, "value", old_val + self.habit.goal
                    )
                    self.habit.load_from_db(self.db)
                    self.app.refresh()

            elif self.habit.tag == "varied":
                date_ = date.today()

                def today_save_click():
                    val = entry_today.get()
                    self.db.add_entry(
                        habit_name=self.habit_name, value=val, note="", day=date_
                    )
                    self.configure(state="disabled")
                    entry_win.destroy()

                entry_win = CTkToplevel()
                entry_win.geometry("400x400")
                entry_win.title(f"{self.habit_name} - {date_}")
                entry_win.grab_set()

                entry_today = LabelEntry(
                    master=entry_win, text="Enter today's value:", sticky="w"
                )

                save_btn = CTkButton(
                    master=entry_win, text="Save", command=today_save_click
                )

                entry_today.grid(column=0, row=0)
                save_btn.grid(column=0, row=1)

    def load_habit(self):
        self.habit = Habit(self.db, self.habit_name)

    def right_btn_menu_popup(
        self, event
    ):  # maybe someday rewrite it so it does not look so shit
        context_menu = Menu(self, tearoff=0, font=("Arial", 18))
        context_menu.add_command(label="Notes", command=self.disp_notesmenu)
        context_menu.add_command(label="Modify", command=self.disp_modmenu)
        context_menu.add_command(label="Move habits", command=self.disp_move_habit)
        context_menu.add_command(label="Stats", command=self.disp_graphsmenu)
        context_menu.add_separator()
        context_menu.add_command(label="Delete habit", command=self.delete_habit)
        context_menu.post(event.x_root, event.y_root)

    def disp_notesmenu(self):
        notes_win = CTkToplevel(self.master)
        notes_win.geometry("600x600")
        notes_win.title(f"Notes - {self.habit.name}")

        text_box = CTkEntry(
            notes_win,
            width=notes_win.winfo_width(),
            height=notes_win.winfo_height(),
        )
        text_box.insert(0, string=self.habit.desc)
        text_box.pack()

        def save_click():
            payload = text_box.get()
            self.db.modify_habit_param(self.habit.name, "description", payload)
            self.app.refresh()
            notes_win.destroy()

        save_button = CTkButton(
            master=notes_win, text="Save", font=("Arial", 24), command=save_click
        )
        save_button.pack()

        notes_win.grab_set()

    def disp_graphsmenu(self):
        pass

    def delete_habit(self):
        self.db.delete_habit(self.habit.name)
        self.app.refresh()

    def disp_modmenu(self):
        def save_click():
            u = label_unit.get()
            q = label_question.get()
            t = label_tag.get()
            g = label_goal.get()

            self.db.modify_habit_param(self.habit.name, "unit", u)
            self.db.modify_habit_param(self.habit.name, "question", q)
            self.db.modify_habit_param(self.habit.name, "tag", t)
            self.db.modify_habit_param(self.habit.name, "daily_goal", g)

            self.app.refresh()
            mod_win.destroy()

        def mod_click():
            def mod_entry_click():
                day = day_entry.get()
                year = year_entry.get()
                month = month_entry.get()
                if int(day) < 10 and day[0] != 0:
                    day = "0" + day
                if int(month) < 10 and month[0] != 0:
                    month = "0" + month
                date = f"{year}-{month}-{day}"
                val = val_entry.get()
                self.db.modify_habit_entry(
                    self.habit_name, entry_date=date, key_to_mod="value", new_val=val
                )
                self.habit.load_from_db(self.db)
                scrollFrame.reload(self.habit)
                mod_entry_win.destroy()

            mod_entry_win = CTkToplevel()
            mod_entry_win.geometry("400x400")
            day_entry = LabelEntry(mod_entry_win, text="day")
            month_entry = LabelEntry(mod_entry_win, text="month")
            year_entry = LabelEntry(mod_entry_win, text="year")
            val_entry = LabelEntry(mod_entry_win, text="new value")

            day_entry.grid(column=0, row=0)
            month_entry.grid(column=0, row=1)
            year_entry.grid(column=0, row=2)
            val_entry.grid(column=0, row=3)

            mod_entry_save_btn = CTkButton(
                master=mod_entry_win, text="Save", command=mod_entry_click
            )
            mod_entry_save_btn.grid(column=0, row=4)

            mod_entry_win.grab_set()

        mod_win = CTkToplevel(self.app)
        mod_win.geometry("600x400")
        mod_win.title(f"Modifying - {self.habit.name}")

        mod_win.columnconfigure(1, weight=1)
        mod_win.columnconfigure(0, weight=1)
        mod_win_F1 = CTkFrame(master=mod_win)
        mod_win_F2 = CTkFrame(master=mod_win)
        mod_win_F1.grid(column=0, row=0, sticky="nw")
        mod_win_F2.grid(column=1, row=0, sticky="ne")

        # F1_width = mod_win_F1.winfo_width()
        # F1_width = 300

        label_unit = LabelEntry(mod_win_F1, text="unit:", font=("Arial", 24))
        label_question = LabelEntry(mod_win_F1, text="question:", font=("Arial", 24))
        label_tag = LabelEntry(mod_win_F1, text="tag:", font=("Arial", 24))
        label_goal = LabelEntry(mod_win_F1, text="daily goal", font=("Arial", 24))

        label_unit.insert(0, self.habit.unit)
        label_question.insert(0, self.habit.question)
        label_tag.insert(0, self.habit.tag)
        label_goal.insert(0, self.habit.goal)

        label_unit.grid(row=0, column=0)
        label_question.grid(row=1, column=0)
        label_tag.grid(row=2, column=0)
        label_goal.grid(row=3, column=0)

        # daily entries
        scrollFrame = ScrollFrame(
            master=mod_win, title="Daily entries", habit=self.habit
        )
        scrollFrame.grid(column=1, row=0)

        mod_button = CTkButton(
            master=mod_win, text="Modify entry", font=("Arial", 24), command=mod_click
        )
        mod_button.grid(row=1, column=1, pady=10)

        save_button = CTkButton(
            master=mod_win, text="Save", font=("Arial", 24), command=save_click
        )
        save_button.grid(row=2, column=1, pady=10)
        mod_win.grab_set()

    def disp_move_habit(self):
        def swap_two_habits():
            habit1_pos = int(entry_1.get()) - 1
            habit2_pos = int(entry_2.get()) - 1
            if habit1_pos > 8 or habit2_pos > 8 or habit1_pos < 0 or habit2_pos < 0:
                return

            # note the positions of habit1 in the grid
            h1_name = list(self.app.habit_widgets.keys())[
                list(self.app.habit_widgets.values()).index(habit1_pos)
            ]
            h2_name = list(self.app.habit_widgets.keys())[
                list(self.app.habit_widgets.values()).index(habit2_pos)
            ]

            self.db.modify_habit_param(h1_name, "pos", habit2_pos)
            self.db.modify_habit_param(h2_name, "pos", habit1_pos)
            self.app.refresh()
            win_move_habit.destroy()

        win_move_habit = CTkToplevel(self.app)  # Tworzenie nowego okna
        win_move_habit._fg_color = "#2B2B2B"
        win_move_habit.geometry("600x400")  # Ustawienie rozmiaru nowego okna
        win_move_habit.title("Move Habits")  # Ustawienie tytułu nowego okna

        CTkLabel(master=win_move_habit, text="Choose which habits to move:").grid(
            column=0, row=0
        )
        entry_1 = LabelEntry(master=win_move_habit, text="1st habit number:")
        entry_1.entry.insert(0, self.habit.pos + 1)
        entry_2 = LabelEntry(master=win_move_habit, text="2nd habit number:")

        entry_1.grid(column=0, row=1)
        entry_2.grid(column=0, row=2)

        button = CTkButton(
            master=win_move_habit,
            text="Save",
            font=("Arial", 18),
            command=swap_two_habits,
        )
        button.grid(column=0, row=3)  # Dodanie przycisku zapisu do nowego okna

        win_move_habit.grab_set()


class ScrollFrame(CTkScrollableFrame):
    def __init__(self, master, title, habit):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.habit = habit
        self.unit = self.habit.unit
        self.values = []

        for entry in self.habit.data:
            self.values.append(f"{entry.day}.{entry.month}.{entry.year} - {entry.val}")
        self.load()

    def load(self):
        for i, value in enumerate(self.values):
            label = CTkLabel(self, text=str(value) + self.unit)
            label.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")

    def reload(self, habit):
        self.habit = habit
        for entry_label in self.winfo_children():
            entry_label.destroy()

        self.values = []
        for entry in self.habit.data:
            self.values.append(f"{entry.day}.{entry.month}.{entry.year} - {entry.val}")

        self.load()


class ControlButton(CTkButton):
    def __init__(self, master, label, command):
        super().__init__(
            master=master,
            text=label,
            font=("Arial", 28),
            width=300,
            height=80,
            fg_color="#4158D0",  # Kolor tekstu
            hover_color="#C850C0",  # Zmiana koloru po najechaniu myszką
            border_color="#FFCC70",
            border_width=2,
            command=command,
        )


class App_(CTk):
    def __init__(self, db):
        super().__init__()
        self.geometry("1200x800")
        self.db = db
        self.habit_widgets = {}

        self.habitFrame = CTkFrame(self, width=900, height=800)
        self.controlsFrame = CTkFrame(self, width=300, height=800)
        self.habitFrame.grid(row=0, column=0)
        self.controlsFrame.grid(row=0, column=1, sticky="n")

        self.habitFrame.rowconfigure((0, 1, 2), weight=0, minsize=200)
        self.habitFrame.columnconfigure((0, 1, 2), weight=0, minsize=300)
        self.habitFrame.grid_propagate(False)

        self.controlsFrame.rowconfigure((0, 1), weight=0, minsize=200)
        self.controlsFrame.columnconfigure(0, weight=0, minsize=300)
        self.controlsFrame.grid_propagate(False)

    def refresh(self):
        self.unload_habits()
        self.shift_habits()
        self.load_habits()

    def load_habits(self):
        for h_name in self.db.get_habits_aslist():
            self.load_habit_widget(h_name)

    def unload_habits(self):
        for habit in self.habitFrame.grid_slaves():
            habit.destroy()

    def shift_habits(self):
        positions = {}
        for habit_name in self.db.get_habits_aslist():
            h_pos = self.db.get_habit_pos(habit_name)
            positions[habit_name] = h_pos

        for i, (h_name, val) in enumerate(
            sorted(positions.items(), key=lambda item: item[1])
        ):
            if val != i:
                self.db.modify_habit_param(h_name, "pos", i)

    def load_habit_widget(self, habit_name, habit_tag=""):
        button = HabitWidget(
            master=self.habitFrame,
            text="",
            font=("Arial", 28),
            width=200,
            height=200,
            border_color="#FFCC70",
            border_width=2,
            habit_name=habit_name,
            habit_tag=habit_tag,
            db=self.db,
            app=self,
        )

        (x, y) = int_to_pos(button.habit.pos)
        button.grid(row=y, column=x, pady=20)
        self.habit_widgets[button.habit.name] = button.habit.pos

        label_hm = CTkLabel(
            master=button,
            text=f"{str(button.habit.pos+1)}. {button.habit_name}",
            font=CTkFont("Arial", 24),
            bg_color="transparent",
        )

        label_hm.place(rely=0.01, relwidth=0.9, anchor="n", relx=0.5)

        label_tag = CTkLabel(
            master=button, text="#" + button.habit_tag, font=("Arial", 24)
        )
        label_tag.place(rely=0.8, x=2)


class LabelEntry(CTkFrame):
    def __init__(self, master, text, sticky="", font=("Arial", 16)):
        super().__init__(master, bg_color="transparent")
        self.label = CTkLabel(master=self, text=text, font=font, bg_color="transparent")
        self.entry = CTkEntry(master=self)

        self.label.grid(row=0, column=0, sticky=sticky)
        self.entry.grid(row=1, column=0, sticky=sticky)

    def get(self):
        return self.entry.get()

    def insert(self, index: int, text: str):
        self.entry.insert(index, text)
