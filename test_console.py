#!/usr/bin/python3
import inspect
import io
import sys
import cmd
import shutil
import os

# Cleanup file storage
file_path = "file.json"
if not os.path.exists(file_path):
    try:
        from models.engine.file_storage import FileStorage
        file_path = FileStorage._FileStorage__file_path
    except ImportError:
        pass

if os.path.exists(file_path):
    os.remove(file_path)

# Backup console file
if os.path.exists("tmp_console_main.py"):
    shutil.copy("tmp_console_main.py", "console.py")
shutil.copy("console.py", "tmp_console_main.py")

# Backup models/__init__.py file
if os.path.exists("models/tmp__init__.py"):
    shutil.copy("models/tmp__init__.py", "models/__init__.py")
shutil.copy("models/__init__.py", "models/tmp__init__.py")

# Overwrite models/__init__.py file with switch_to_file_storage.py
if os.path.exists("switch_to_file_storage.py"):
    shutil.copy("switch_to_file_storage.py", "models/__init__.py")

# Updating console to remove "__main__"
with open("tmp_console_main.py", "r") as file_i:
    console_lines = file_i.readlines()
    with open("console.py", "w") as file_o:
        in_main = False
        for line in console_lines:
            if "__main__" in line:
                in_main = True
            elif in_main:
                if "cmdloop" not in line:
                    file_o.write(line.lstrip("    ")) 
            else:
                file_o.write(line)

# Import console
import console

# Create console object
console_obj = "HBNBCommand"
for name, obj in inspect.getmembers(console):
    if inspect.isclass(obj) and issubclass(obj, cmd.Cmd):
        console_obj = obj

my_console = console_obj(stdout=io.StringIO(), stdin=io.StringIO())
my_console.use_rawinput = False

def exec_command(my_console, the_command, last_lines=1):
    """Execute a command on the console and return the output."""
    my_console.stdout = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = my_console.stdout
    my_console.onecmd(the_command)
    sys.stdout = real_stdout
    lines = my_console.stdout.getvalue().split("\n")
    return "\n".join(lines[(-1*(last_lines+1)):-1])

# Tests
state_name = "California"
result = exec_command(my_console, f'create State name="{state_name}"')
if result is None or result == "":
    print("FAIL: No ID retrieved")
state_id = result

city_name = "San Francisco is super cool"
result = exec_command(my_console, f'create City state_id="{state_id}" name="{city_name.replace(" ", "_")}"')
if result is None or result == "":
    print("FAIL: No ID retrieved")
city_id = result

user_email = "my@me.com"
user_pwd = "pwd"
user_fn = "FN"
user_ln = "LN"
result = exec_command(my_console, f'create User email="{user_email}" password="{user_pwd}" first_name="{user_fn}" last_name="{user_ln}"')
if result is None or result == "":
    print("FAIL: No ID retrieved")
user_id = result

place_name = "My house"
place_desc = "no description yet"
place_nb_rooms = 4
place_nb_bath = 0
place_max_guests = -3
place_price = 100
place_lat = -120.12
place_lon = 0.41921928
result = exec_command(my_console, f'create Place city_id="{city_id}" user_id="{user_id}" name="{place_name.replace(" ", "_")}" description="{place_desc.replace(" ", "_")}" number_rooms={place_nb_rooms} number_bathrooms={place_nb_bath} max_guest={place_max_guests} price_by_night={place_price} latitude={place_lat} longitude={place_lon}')
if result is None or result == "":
    print("FAIL: No ID retrieved")
place_id = result

result = exec_command(my_console, f"show Place {place_id}")
if result is None or result == "":
    print("FAIL: empty output")

# Verify output
required_fields = {
    "city_id": city_id,
    "user_id": user_id,
    "name": place_name,
    "description": place_desc,
    "number_rooms": str(place_nb_rooms),
    "number_bathrooms": str(place_nb_bath),
    "max_guest": str(place_max_guests),
    "price_by_night": str(place_price),
    "latitude": str(place_lat),
    "longitude": str(place_lon)
}

for field, value in required_fields.items():
    if field not in result or value not in result:
        print(f"FAIL: missing new information: \"{field} = {value}\"")

print("OK", end="\n")

# Restore original files
shutil.copy("tmp_console_main.py", "console.py")
shutil.copy("models/tmp__init__.py", "models/__init__.py")

