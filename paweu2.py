from tkinter import Frame
from typing import Tuple
from customtkinter import *
from tkinter import *

from UI import HabitWidget
from Habit import Habit
from DataBase import DataBase

db = DataBase()


global habit_counter
habit_counter = 0


# Tworzenie głównego okna aplikacji


class App_(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")

        self.habitFrame = CTkFrame(self, width=900, height=800)
        self.controlsFrame = CTkFrame(self, width=300, height=800)
        self.habitFrame.grid(row=0, column=0)
        self.controlsFrame.grid(row=0, column=1)

        self.habitFrame.rowconfigure((0, 1, 2), weight=0, minsize=200)
        self.habitFrame.columnconfigure((0, 1, 2), weight=0, minsize=300)

        self.controlsFrame.rowconfigure((0, 1, 2), weight=0, minsize=200)
        self.controlsFrame.columnconfigure(0, weight=0, minsize=300)

    def refresh(self):
        self.unload_habits()
        self.shift_habits()
        self.load_habits()

    def load_habits(self):
        for h_name in db.get_habits_aslist():
            new_habit(h_name)

    def unload_habits(self):
        for habit in App.habitFrame.grid_slaves():
            habit.destroy()

    def shift_habits(self):

        positions = {}
        for habit_name in db.get_habits_aslist():
            h_pos = db.get_habit_pos(habit_name)
            positions[habit_name] = h_pos

        for i, (h_name, val) in enumerate(
            sorted(positions.items(), key=lambda item: item[1])
        ):
            if val != i:
                db.modify_habit_param(h_name, "pos", i)


App = App_()


def int_to_pos(int_) -> tuple:  # for easier widget grid management
    x = int_ % 3
    y = int(int_ / 3)
    return (x, y)


def open_new_window():
    def save_click():
        global habit_counter
        habit_name = entry1.get()
        habit_tag = entry2.get()
        new_habit(habit_name, habit_tag)
        new_window.destroy()  # zamyka nowe okno
        habit_counter = habit_counter + 1

    new_window = CTkToplevel(App)  # Tworzenie nowego okna
    new_window.geometry("600x400")  # Ustawienie rozmiaru nowego okna
    new_window.title("New Habit")  # Ustawienie tytułu nowego okna

    label = CTkLabel(master=new_window, text="New Habit", font=("Arial", 24))
    label.pack(pady=20)  # Dodanie etykiety do nowego okna

    label_name = CTkLabel(master=new_window, text="Name", font=("Arial", 16))
    label_name.pack()

    # tworzenie labela do którego wpisujemy nazwe habitu

    entry1 = CTkEntry(master=new_window, width=300, font=("Arial", 18))
    entry1.pack(pady=10)  # Dodanie pola tekstowego do nowego okna

    label_tag = CTkLabel(master=new_window, text="Tag", font=("Arial", 16))
    label_tag.pack()

    entry2 = CTkEntry(master=new_window, width=300, font=("Arial", 18))
    entry2.pack(pady=10)  # Dodanie pola tekstowego do nowego okna

    # tworzy przycisk "Save" i umieszcza go w tym oknie

    save_button = CTkButton(
        master=new_window, text="Save", font=("Arial", 18), command=save_click
    )
    save_button.pack(pady=10)  # Dodanie przycisku zapisu do nowego okna

    # ustawia to okno, jako pierwsze na wierzchu

    new_window.grab_set()


def open_move_habit():
    def swap_two_habits():
        habit1_pos = int(entry_1.get()) - 1
        habit2_pos = int(entry_2.get()) - 1
        habit_window.destroy()

        # note the positions of habit1 in the grid
        h1_name = list(habit_widgets.keys())[
            list(habit_widgets.values()).index(habit1_pos)
        ]
        h2_name = list(habit_widgets.keys())[
            list(habit_widgets.values()).index(habit2_pos)
        ]

        db.modify_habit_param(h1_name, "pos", habit2_pos)
        db.modify_habit_param(h2_name, "pos", habit1_pos)
        App.refresh()

    habit_window = CTkToplevel(App)  # Tworzenie nowego okna
    habit_window.geometry("600x400")  # Ustawienie rozmiaru nowego okna
    habit_window.title("Move Habits")  # Ustawienie tytułu nowego okna

    label1 = CTkLabel(
        master=habit_window, text="Choose which habits to move:", font=("Arial", 24)
    )
    label1.pack(pady=20)  # Dodanie etykiety do nowego okna

    label2 = CTkLabel(
        master=habit_window, text="1st habit block number:", font=("Arial", 18)
    )
    label2.pack(pady=20)  # Dodanie etykiety do nowego okna

    entry_1 = CTkEntry(master=habit_window, width=50, font=("Arial", 18))
    entry_1.pack(pady=10)  # Dodanie pola tekstowego do nowego okna)

    label3 = CTkLabel(
        master=habit_window, text="2st habit block number:", font=("Arial", 18)
    )
    label3.pack(pady=20)  # Dodanie etykiety do nowego okna

    entry_2 = CTkEntry(master=habit_window, width=50, font=("Arial", 18))
    entry_2.pack(pady=10)  # Dodanie pola tekstowego do nowego okna)

    move_button = CTkButton(
        master=habit_window, text="Save", font=("Arial", 18), command=swap_two_habits
    )
    move_button.pack(pady=10)  # Dodanie przycisku zapisu do nowego okna

    habit_window.grab_set()


def delete_habit():
    def del_btn():
        habit_index = int(entry.get()) - 1

        h_name = list(habit_widgets.keys())[
            list(habit_widgets.values()).index(habit_index)
        ]
        db.delete_habit(h_name)
        del habit_widgets[h_name]

        App.refresh()

        del_win.destroy()

    del_win = CTkToplevel(App)
    del_win.geometry("600x400")
    del_win.title("Delete a habit")

    label1 = CTkLabel(
        master=del_win,
        text="Choose which habits to delete (permanently):",
        font=("Arial", 24),
    )
    label1.pack(pady=20)

    entry = CTkEntry(master=del_win, width=50, font=("Arial", 18))
    entry.pack(pady=10)

    delete_button = CTkButton(
        master=del_win, text="Delete", font=("Arial", 18), command=del_btn
    )
    delete_button.pack(pady=10)

    del_win.grab_set()


def open_notes_win():
    def send_notes_todb():
        note_index = int(entry_id.get()) - 1
        note_content = entry_note.get()

        h_name = list(habit_widgets.keys())[
            list(habit_widgets.values()).index(note_index)
        ]
        print(h_name)
        write_notes_window.destroy()

        db.modify_habit_param(h_name, "desc", note_content)

    write_notes_window = CTkToplevel(App)
    write_notes_window.geometry("600x600")
    write_notes_window.title("Write Notes")

    # Tworzymy etykietę i pole Entry do wprowadzania notatki
    label_note = CTkLabel(
        master=write_notes_window, text="Write your note:", font=("Arial", 24)
    )
    label_note.pack(pady=20)

    entry_note = CTkEntry(
        master=write_notes_window, font=("Arial", 18), height=200, width=200
    )
    entry_note.pack(pady=10)

    label1 = CTkLabel(
        master=write_notes_window, text="Notes to which habit?:", font=("Arial", 24)
    )
    label1.pack(pady=20)

    entry_id = CTkEntry(master=write_notes_window, width=50, font=("Arial", 18))
    entry_id.pack(pady=10)

    # Tworzymy przycisk "Save" do zapisania notatki
    save_button = CTkButton(
        master=write_notes_window,
        text="Save",
        font=("Arial", 18),
        command=send_notes_todb,
    )
    save_button.pack(pady=10)

    # Ustawiamy okno write_notes_window jako aktywne
    write_notes_window.grab_set()


# def open_notes():
#     def write_notes():
#         note_index = int(entry1.get()) - 1  # Pobieramy indeks habitu

#         notes_win.destroy()  # Zamykamy okno notes_win

#         # Funkcja write_notes_win
#         def write_notes_win():
#             note = entry_note.get()  # Pobieramy notatkę z pola Entry
#             notes[note_index] = (
#                 note  # Zapisujemy notatkę do odpowiedniego indeksu w tablicy notes
#             )
#             write_notes_window.destroy()  # Zamykamy okno write_notes_window

#         # Tworzymy okno write_notes_win
#         write_notes_window = CTkToplevel(App)
#         write_notes_window.geometry("600x400")
#         write_notes_window.title("Write Notes")

#         # Tworzymy etykietę i pole Entry do wprowadzania notatki
#         label_note = CTkLabel(
#             master=write_notes_window, text="Write your note:", font=("Arial", 24)
#         )
#         label_note.pack(pady=20)

#         entry_note = CTkEntry(
#             master=write_notes_window, font=("Arial", 18), height=200, width=200
#         )
#         entry_note.pack(pady=10)
#         if notes[note_index] != None:
#             entry_note.insert(0, notes[note_index])  # Insert pre-written text

#         # Tworzymy przycisk "Save" do zapisania notatki
#         save_button = CTkButton(
#             master=write_notes_window,
#             text="Save",
#             font=("Arial", 18),
#             command=write_notes_win,
#         )
#         save_button.pack(pady=10)

#         # Ustawiamy okno write_notes_window jako aktywne
#         write_notes_window.grab_set()

#     notes_win = CTkToplevel(App)
#     notes_win.geometry("600x400")
#     notes_win.title("Notes")

#     label1 = CTkLabel(
#         master=notes_win, text="Notes to which habit?:", font=("Arial", 24)
#     )
#     label1.pack(pady=20)

#     entry1 = CTkEntry(master=notes_win, width=50, font=("Arial", 18))
#     entry1.pack(pady=10)

#     ok_button = CTkButton(
#         master=notes_win, text="Ok", font=("Arial", 18), command=write_notes
#     )
#     ok_button.pack(pady=10)

#     notes_win.grab_set()


# tworzenie przycisku "Add new habit"

btn_add = CTkButton(
    master=App.controlsFrame,
    text="Add new habit",
    font=("Arial", 28),
    width=300,
    height=80,
    fg_color="#4158D0",  # Kolor tekstu
    hover_color="#C850C0",  # Zmiana koloru po najechaniu myszką
    border_color="#FFCC70",
    border_width=2,
    command=open_new_window,
)  # Przypisanie funkcji do przycisku
btn_add.grid(row=0, column=0)
# umieszczanie go w głównym oknie

# btn_add.place(relx=0.84, rely=0.1, anchor="center")

# tworzenie przycisku "Delete habits"

btn_del = CTkButton(
    master=App.controlsFrame,
    text="Delete habit",
    font=("Arial", 28),
    width=300,
    height=80,
    fg_color="#4158D0",  # Kolor tekstu
    hover_color="#C850C0",  # Zmiana koloru po najechaniu myszką
    border_color="#FFCC70",
    border_width=2,
    command=delete_habit,
)

btn_del.grid(row=1, column=0)

# umieszczanie go w głównym oknie

# btn_del.place(relx=0.84, rely=0.3, anchor="center")

# tworzenie przycisku "Move habit blocks"

btn_move = CTkButton(
    master=App.controlsFrame,
    text="Move habit blocks",
    font=("Arial", 28),
    width=300,
    height=80,
    fg_color="#4158D0",  # Kolor tekstu
    hover_color="#C850C0",  # Zmiana koloru po najechaniu myszką
    border_color="#FFCC70",
    border_width=2,
    command=open_move_habit,
)
btn_move.grid(row=2, column=0)
# umieszczanie go w głównym oknie

# btn_move.place(relx=0.84, rely=0.5, anchor="center")

# tworzenie przycisku "Notes"

btn_note = CTkButton(
    master=App.controlsFrame,
    text="Notes",
    font=("Arial", 28),
    width=300,
    height=80,
    fg_color="#4158D0",  # Kolor tekstu
    hover_color="#C850C0",  # Zmiana koloru po najechaniu myszką
    border_color="#FFCC70",
    border_width=2,
    command=open_notes_win,
)
btn_note.grid(row=3, column=0)
# umieszczanie go w głównym oknie

# btn_move.place(relx=0.84, rely=0.7, anchor="center")


habit_widgets = {}
lblhm_list = []
lbltg_list = []


def new_habit(habit_name, habit_tag=""):
    button = HabitWidget(
        master=App.habitFrame,
        text="",
        font=("Arial", 28),
        width=200,
        height=200,
        border_color="#FFCC70",
        border_width=2,
        habit_name=habit_name,
        habit_tag=habit_tag,
        db=db,
        app=App,
    )

    # button.place(x=pxb[button.pos], y=pyb[button.pos])
    (x, y) = int_to_pos(button.habit.pos)
    button.grid(row=y, column=x, pady=20)
    habit_widgets[button.habit.name] = button.habit.pos

    label_hm = CTkLabel(
        master=button,
        text=f"{str(button.habit.pos+1)}. {button.habit_name}",
        font=CTkFont("Arial", 24),
        bg_color="transparent",
    )
    # label_hm.pack()
    label_hm.place(rely=0.01, relwidth=0.9, anchor="n", relx=0.5)
    # label_hm.place(x=pxl[button.pos], y=pyl[button.pos])
    lblhm_list.append(label_hm)

    label_tag = CTkLabel(master=button, text="#" + button.habit_tag, font=("Arial", 24))
    # label_tag.pack()
    label_tag.place(rely=0.8, x=2)
    # lbltg_list.append(label_tag)


# loading habits from the db to the UI


App.refresh()

App.shift_habits()

set_appearance_mode("dark")
App.mainloop()
