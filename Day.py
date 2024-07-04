from Utils import *


class Day:
    def __init__(self, _date: str, _value: int, _note: str):
        if valiDate(_date):
            y, m, d = _date.split("-")
        else:
            raise ValueError("Improper data format provided. Failed to initialize")

        self.year: str = y
        self.month: str = m
        self.day: str = d
        self.val: int = _value
        self.note: str = _note
