from __future__ import annotations
from dataclasses import dataclass
from math import floor, ceil
from json import load, dump
from datetime import datetime


INDENT_WIDTH: int = 3
INDENT_STR: str = " "*INDENT_WIDTH

class ChoiceError(ValueError): pass

@dataclass
class BassField:
    id: str
    t: type
    data = None

class Field(BassField):
    TYPE_DEFAULT: type = str
    SUPPORTED_TYPES = (str, int, float)
    TYPE_REPR_DICT = {}
    for t in SUPPORTED_TYPES:
        TYPE_REPR_DICT.update({ str(repr(t)): t })

    def __repr__(self):
        return f"<Field {repr(self.t)} '{self.id}'>"
    
    def set_type(self, t: type) -> None:
        self.t = t

    def set_data(self, data) -> Field:
        self.data = data
        return self

    def get_data(self):
        return self.data
    
    def partial_copy(self):
        return Field(self.id, self.t)

    def full_copy(self):
        c = Field(self.id, self.t)
        return c.set_data(self.data)
    
@dataclass
class LogEntry:
    date: datetime
    content: list[Field]

class Category:
    BASE_FILEDS: tuple[Field] = (Field("description", str), Field("date", str))

    def __init__(self, name: str, custom_fields: tuple[Field] = ()):
        self.name = name

        self.custom_fields = custom_fields
        self._base_fields = Category.BASE_FILEDS
        self.fields: tuple[Field] = custom_fields + Category.BASE_FILEDS

        self.entries: dict = {}

    def __add_field(self, field: Field) -> None:
        self.fields = (field,) + self.fields

    def add_custom_field(self, field: Field) -> None:
        self.custom_fields += (field,)
        self.__add_field(field)

    def add_log_entry(self, log_entry: LogEntry) -> None:
        content: dict = {}
        for field in log_entry.content:
            content.update({ field.id: field.data })
        self.entries.update({ log_entry.date: content })

    def save(self) -> None:
        with open(f"{self.name}.json", 'w') as f:
            dump(self.entries, f, indent=4)

    def __repr__(self):
        return f"<Category '{self.name}' with fields {self.fields}>"
    
    def from_json_file(fs, name: str) -> Category:
        _dict: dict = load(fs)
        c = Category(name)
        c.entries = _dict
        field_name_strs: list[str]= _dict[tuple(_dict.keys())[0]].keys()
        c.fields: tuple[Field] = ()
        for field_name_str in field_name_strs:
            c.fields += (Field(field_name_str, str),)
        return c
    
def repr(t: type):
    ts = str(t)
    return "({})".format(ts[ts[:-3].rfind("'")+1:-2])

def pad_vertical(fn: function):
    def wrapper(*args, **kwargs):
        print()
        return fn(*args, **kwargs)
    return wrapper

CHAR = "*"
BAR_LEN = 58
BAR = CHAR*BAR_LEN

def heading(title: str | None = None) -> str:
    if title is None:
        return BAR
    
    sidebars_len = (BAR_LEN - len(title) - 2) / 2
    s = CHAR*floor(sidebars_len)
    s += " " + title + " "
    s += CHAR*ceil(sidebars_len)
    
    return s

def options_menu(title: str, options: list[str]) -> None:
    indent_level = \
        2 if max([len(s.strip()) for s in options]) <= (BAR_LEN - INDENT_WIDTH*2 - 3) \
        else 1
    
    s = heading(title) + "\n\n"
    for i, o in enumerate(options, 1):
        s += INDENT_STR*indent_level + str(i) + ") " + o + "\n"
    s += "\n" + BAR
    print(s)

NONE = lambda *args: True
def error_check(
        _input: str, 
        _type: type, 
        condition: function = NONE, 
        err_msg: str = "Invalid response."
        ):
    try:
        x = _type(_input)
        if condition(x):
            return x
    except ValueError:
        pass

    return error_check(
        input("ERROR. " + err_msg + " "), 
        _type, 
        condition,
        err_msg
    )

def bool_prompt(prompt: str) -> bool:
    ans = input(prompt + " (Y/N) ")
    ans = ans.strip()[0].upper()
    if ans == "Y":
        return True
    elif ans == "N":
        return False
    return bool_prompt("ERROR. Invalid response.")

def which(options: list[str], title: str = "Which?") -> int:
    options_menu(title=title, options=options)
    return error_check(
        input("Please enter your choice: "),
        int,
        lambda x: x > 0 and x <= len(options),
        "Invalid chioce."
    ) - 1
