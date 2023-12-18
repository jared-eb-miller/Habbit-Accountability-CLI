from __future__ import annotations
from dataclasses import dataclass
from math import floor, ceil

INDENT_WIDTH: int = 3
INDENT_STR: str = " "*INDENT_WIDTH


@dataclass
class Field:
    id: str
    _type: type

    def __repr__(self):
        type_str = str(self._type)
        type_str = type_str[type_str[:-3].rfind("'")+1:-2]
        return f"<Field {type_str} '{self.id}'>"

class Category:
    BASE_FILEDS: tuple[Field] = (Field("date", str), Field("description", str))

    def __init__(self, name: str, custom_fields: tuple[Field] = ()):
        self.name = name

        self._custom_fields = custom_fields
        self._base_fields = Category.BASE_FILEDS
        self.fields: tuple[Field] = custom_fields + Category.BASE_FILEDS

    def __add_field(self, field: Field) -> None:
        self.fields += (field,)

    def add_custom_field(self, field: Field) -> None:
        self._custom_fields += (field,)
        self.__add_field(field)

    def __repr__(self):
        return f"<Category '{self.name}' with fields {self.fields}>"
    
    def new() -> Category:
        c = Category(input("Please enter the name of your behavior category: "))
        print("Please enter the name of all the customm fields for your behavior category:")
        print("                          Enter 'DONE' to finsih")
        i = 0
        while True:
            i += 1
            f = input(f"field [{i}]: ")
            if f == "DONE":
                break
            c.add_custom_field(Field(f, str))
        
        return c
    

def options_menu(title: str, options: list[str]) -> None:
    CHAR = "*"
    BAR_LEN = 58
    BAR = CHAR*BAR_LEN
    indent_level = \
        2 if max([len(s.strip()) for s in options]) <= (BAR_LEN - INDENT_WIDTH*2 - 3) \
        else 1
    sidebars_len = (BAR_LEN - len(title) - 2) / 2
    s =  CHAR*floor(sidebars_len)
    s += " " + title + " "
    s += CHAR*ceil(sidebars_len)
    s += "\n\n"
    for i, o in enumerate(options, 1):
        s += INDENT_STR*indent_level + str(i) + ") " + o + "\n"
    s += "\n" + BAR
    print(s)