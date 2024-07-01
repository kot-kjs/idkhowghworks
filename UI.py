from tkinter import *
from customtkinter import *
from Habit import Habit


# custom "button" class that integrates the habit class and the ctk button (hopefully)


class HabitWidget(CTkButton):
    def __init__(self, db, habit_name, habit_tag, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habit_name = habit_name
        self.app = app
        self.db = db
        self.habit = Habit(db, habit_name)
        self.habit_tag = self.habit.tag
        if self.habit_tag == "":
            self.habit_tag = habit_tag

        if self.habit_tag == "test":
            self.configure(command=self.toggle)

        self.bind("<Button-3>", lambda event: self.right_btn_menu_popup(event))

    def toggle(self):  # rewrite it
        if self._state == "normal":
            self.configure(state="disabled")
            self.configure(fg_color="#144870")

    def right_btn_menu_popup(
        self, event
    ):  # maybe someday rewrite it so it does not look so shit
        context_menu = Menu(self, tearoff=0, font=("Arial", 18))
        context_menu.add_command(label="Notes", command=self.disp_notesmenu)
        context_menu.add_command(label="Modify", command=self.disp_modmenu)
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
        # self.destroy()
        self.app.refresh()

    def disp_modmenu(self):
        def save_click():
            u = entry_unit.get()
            q = entry_question.get()
            e = entry_tag.get()

            self.db.modify_habit_param(self.habit.name, "unit", u)
            self.db.modify_habit_param(self.habit.name, "question", q)
            self.db.modify_habit_param(self.habit.name, "tag", e)

            self.app.refresh()
            mod_win.destroy()

        mod_win = CTkToplevel(self.master)
        mod_win.geometry("600x800")
        mod_win.title(f"Modifying - {self.habit.name}")

        f1 = CTkFrame(mod_win, width=mod_win.winfo_width())
        f2 = CTkFrame(mod_win, width=mod_win.winfo_width())
        f3 = CTkFrame(mod_win, width=mod_win.winfo_width())

        entry_unit = CTkEntry(
            f1,
            width=mod_win.winfo_width(),
        )
        entry_question = CTkEntry(
            f2,
            width=mod_win.winfo_width(),
        )
        entry_tag = CTkEntry(
            f3,
            width=mod_win.winfo_width(),
        )

        entry_unit.insert(0, self.habit.unit)
        entry_question.insert(0, self.habit.question)
        entry_tag.insert(0, self.habit.tag)

        label_unit = CTkLabel(f1, text="unit:", font=("Arial", 24))
        label_question = CTkLabel(f2, text="question:", font=("Arial", 24))
        label_tag = CTkLabel(f3, text="tag:", font=("Arial", 24))

        label_unit.grid(row=0, column=0)
        entry_unit.grid(row=1, column=0)

        label_question.grid(row=0, column=0)
        entry_question.grid(row=1, column=0)

        label_tag.grid(row=0, column=0)
        entry_tag.grid(row=1, column=0)

        f1.grid(row=0, column=0)
        f2.grid(row=1, column=0)
        f3.grid(row=2, column=0)

        save_button = CTkButton(
            master=mod_win, text="Save", font=("Arial", 24), command=save_click
        )
        save_button.grid(row=4, column=0)
        mod_win.grab_set()
