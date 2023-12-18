from resources import *
import os

def add_log_to(cat: Category):
    print(f"Adding log to category {cat}")

def create_category():
    c = Category.new()
    add_log_to(c)

def add_log():
    os.chdir(os.path.dirname(__file__) + "/resources/category-logs/")
    category_log_file_names: list[str] = os.listdir()
    category_names: list[str] = [fn[:fn.find('.')] for fn in category_log_file_names]
    options: list[str] = category_names + ["Create new category"]

    options_menu(
        title="Choose a Category to Log",
        options=options
    )

    choice = int(input("Please enter your choice: "))

    if choice == len(options):
        create_category()
    else:
        if choice < 0:
            raise ValueError("Invalid choice.")
        
        chosen_category_log_file_name = category_log_file_names[choice-1]

        with open(chosen_category_log_file_name, 'r') as f:
            c = Category.from_json_file(f)
        add_log_to(c)

add_log()