import sqlite3
from datetime import date


class DataBase:
    def __init__(self, path="data.db"):
        self.db = sqlite3.connect(path)
        self.c = self.db.cursor()

    # To make the habit boolean just set unit to "bool"
    def AddHabit(
        self,
        table_name: str,
        unit: str,
        question: str,
        desc: str,
        tag: str,
        pos: int,
        daily_goal: int,
    ) -> bool:
        if self.habit_exists(table_name):
            return False

        try:
            self.c.execute(
                f"""CREATE TABLE IF NOT EXISTS '{table_name}'(
                    name VARCHAR (255),
                    tag VARCHAR (255),
                    unit VARCHAR (255),
                    question VARCHAR(255),
                    description TEXT,
                    pos INT,
                    daily_goal INT,
                    created DATE)
                    
                    """
            )
            self.c.execute(
                f"""CREATE TABLE IF NOT EXISTS '{table_name}_logs' (
                    day DATE,
                    value INT,
                    note TEXT
                    )"""
            )
        except Exception as e:
            print(e)
            return False

        # Inserting habit parameters into the first table
        try:
            self.c.execute(
                f"""INSERT INTO '{table_name}' VALUES ('{table_name}','{tag}', '{unit}', '{question}', '{desc}', '{pos}','{daily_goal}', CURRENT_DATE)"""
            )
        except Exception as e:
            print(e)
            return False
        finally:
            self.db.commit()
            return True

    # Update any table, first finding one with the name 'tableName',
    # then finding a record where the value 'identifierName' has a value 'identifierValue'
    # finally replacing the old valName with valReplacement
    # Note: identifierValue should be unique, like the val of "date" in tableName_logs

    def _update_table(
        self,
        tableName: str,
        identifierName: str,
        identifierValue: str,
        valName: str,
        valReplacement: str,
    ):
        if not self.habit_exists(table_name=tableName):
            raise ValueError(f"Table {tableName} not found in the database")

        if not self._has_table_value(tableName, identifierName, identifierValue):
            raise ValueError(
                f"entry with value {identifierName}={identifierValue} not found in the table {tableName}"
            )

        try:
            self.c.execute(
                f"""UPDATE '{tableName}' SET {valName} = '{valReplacement}'
                                WHERE {identifierName} = '{identifierValue}'
                            """
            )
            self.db.commit()
        except Exception as e:
            raise e

    def modify_habit_param(self, h_name, param_to_mod, new_val):
        if param_to_mod == "name":
            raise ValueError("Parameter 'name' cannot be modified.")

        self._update_table(h_name, "name", h_name, param_to_mod, new_val)

    def modify_habit_entry(self, h_name, entry_date, key_to_mod, new_val):
        if key_to_mod == "day" and self.habit_has_entry("day", new_val):
            raise ValueError("There cannot exist 2 entries for the same day")

        self._update_table(f"{h_name}_logs", "day", entry_date, key_to_mod, new_val)

    # Checks if there's any place where {key_name} has a {key_value}, returning True if there is
    # Eg. checking if k_name "day" has a value of "2001-09-11"
    def _has_table_value(self, table, k_name, k_val) -> bool:
        # returning a boolean depending if it found that value or not
        self.c.execute(
            f"""SELECT EXISTS(SELECT 1 FROM '{table}' WHERE {k_name}=?)""",
            (k_val,),
        )
        record = self.c.fetchone()

        if record[0] == 0:
            return False
        else:
            return True

    def habit_exists(self, table_name: str) -> bool:

        self.c.execute(
            """SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name=?)""",
            (table_name,),
        )
        found = self.c.fetchone()[0]

        return found == 1

    def habit_has_param(self, h_name, param_name, param_val) -> bool:
        # h_name the same
        return self._has_table_value(h_name, param_name, param_val)

    # MIGHT BE USELESS
    def get_habit_pos(self, h_name):
        self.c.execute(f"""SELECT pos FROM '{h_name}'""")
        xd = self.c.fetchone()[0]
        return xd

    def get_habit_entry_value(self, h_name, entry_date):
        self.c.execute(
            f"""SELECT value FROM '{h_name}_logs' WHERE day=?""",
            (entry_date,),
        )
        xd = self.c.fetchone()[0]
        return xd

    def habit_has_entry(self, h_name, entry_name, entry_val) -> bool:
        # append _logs to reference the table in which entries for the habit are stored
        h_name = f"{h_name}_logs"
        return self._has_table_value(h_name, entry_name, entry_val)

    def add_entry(
        self, habit_name: str, value: int, note: str, day: str = date.today()
    ) -> bool:

        # if there already is an entry for a given day, don't add it
        if self.habit_has_entry(habit_name, "day", day):
            raise ValueError("Entry already exists for that day")

        if self.habit_has_param(habit_name, "unit", "bool"):
            if value != 0:
                value == 1

        self.c.execute(
            f"""INSERT INTO '{habit_name}_logs' VALUES ('{day}', {value}, '{note}')"""
        )

        self.db.commit()
        return True

    # should return a list all of user's habit names

    def get_habits_aslist(self):
        self.c.execute(
            """SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_logs' """
        )
        res = self.c.fetchall()
        habit_list = []
        for elem in res:
            habit_list.append(elem[0])

        return habit_list

    def delete_habit(self, h_name):
        try:
            self.c.execute(f"""DROP TABLE IF EXISTS '{h_name}'""")
            self.c.execute(f"""DROP TABLE IF EXISTS '{h_name}_logs'""")
        except Exception as e:
            print(e)
        finally:
            # print("did well i guess")
            self.db.commit()

    def delete_entry(self, h_name, date):
        try:
            self.c.execute(f"DELETE FROM '{h_name}_logs' WHERE day = ?", (date,))
        except Exception as e:
            print(e)
        finally:
            self.db.commit()
