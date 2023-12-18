from resources import *
import os

def add_log_to(cat: Category):
    print(f"Adding log to category {cat}")

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
        c = Category.new()
    else:
        with open(category_log_file_names[choice], 'r') as f:
            c = Category.from_json_file(f)

    add_log_to(c)

add_log()