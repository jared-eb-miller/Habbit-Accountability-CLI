from resources import *
import os
from datetime import datetime

@pad_vertical
def new_category() -> Category:
    c = Category(input("Please enter the name for the category: "))
    print()
    print("Please enter the name of all the customm fields for your behavior category:")
    print("                          Enter 'DONE' to finsih")

    i = 0
    while True:
        i += 1
        f = input(f"field [{i}]: ")
        if f == "DONE":
            break
        c.add_custom_field(Field(f, Field.TYPE_DEFAULT))
    
    if bool_prompt("Would you like to change the type of any field?"):
        fields: list[Field] = list(c.custom_fields)
        while True:
            field = fields[which([str(f) for f in fields])]
            try:
                field.set_type(Field.TYPE_REPR_DICT[input("Enter the nwe field type: ")])
            except KeyError:
                print("Error. Given field type not supported.")
                break

    return c

def get_log_content(cat: Category) -> list[Field]:
    print(heading(f"New {cat.name} Entry"))
    print()

    content: list[Field] = []
    for i, field in enumerate(cat.fields):
        content.append(
            field.partial_copy().set_data(
                error_check(
                    _input=input(f"Field [{i}] {field.id} {repr(field.t)}: "),
                    _type=field.t,
                    err_msg=f"Invalid {repr(field.t)}."
                )
            )
        )
    
    # check if empty date
    if content[-1].data == "":
        content[-1].data = str(datetime.now())
    
    return content

def add_log():
    os.chdir(os.path.dirname(__file__) + "/resources/category-logs/")
    category_log_file_names: list[str] = os.listdir()
    category_names: list[str] = [fn[:fn.find('.')] for fn in category_log_file_names]
    options: list[str] = category_names + ["Create new category"]

    choice = which(
        options,
        title="Choose a Category to Log"
    )

    if choice == len(options)-1:
        c = new_category()
    else:
        with open(category_log_file_names[choice], 'r') as f:
            c = Category.from_json_file(f, category_names[choice])

    c.add_log_entry(LogEntry(
        date=str(datetime.now()),
        content=get_log_content(c)
    ))

    c.save()

add_log()