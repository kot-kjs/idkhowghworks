from DataBase import DataBase
from Day import Day


class Habit:
    def __init__(self, db, name) -> None:
        self.name = name
        self.unit = ""
        self.question = ""
        self.desc = ""
        self.created = ""
        self.data = []  # Array of Day objects
        self.tag = ""
        self.pos = 0

        self.load_from_db(db)

    # DEBUG
    def _dev_disp_params(self) -> None:
        print(
            f"created({self.created})\n{self.name}:\nunit:{self.unit}\nquestion:{self.question}({self.unit})"
        )

    # DEBUG
    def _dev_disp_data(self) -> None:
        print("DATE \t\t\t COUNT \t\t NOTE")
        print("---- \t\t\t ------ \t -----")
        for entry in self.data:
            print(
                f"{entry.year}-{entry.month}-{entry.day}\t\t {entry.val}[{self.unit}] \t\t {entry.note}"
            )

    # returns false if failed to parse the data
    def load_from_db(self, db: DataBase) -> bool:
        if not db.habit_exists(self.name):

            raise ValueError("Habit does not exist (somehow)")

        db.c.execute(f"""SELECT * FROM '{self.name}'""")
        data = db.c.fetchall()[0]
        self.tag = data[1]
        self.unit = data[2]
        self.question = data[3]
        self.desc = data[4]
        self.pos = data[5]
        self.goal = data[6]
        self.created = data[7]

        db.c.execute(f"""SELECT * FROM '{self.name}_logs'""")
        data = db.c.fetchall()

        self.data = []
        for entry in data:
            self.data.append(Day(_date=entry[0], _value=entry[1], _note=entry[2]))

        return True

    # Returns an array of values of entries from a particular month, where:
    # Each index holds a value of a corresponding day
    # Non existent entries will remain as None
    def get_month(self, month: str, year: str):
        vals = [None] * 31

        for entry in self.data:
            if entry.month == month and entry.year == year:
                vals[int(entry.day) - 1] = entry.val

        return vals
