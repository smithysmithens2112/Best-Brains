import json
import os

db_name = 'TEMP_DB.json'

alpha = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
alpha = alpha.split()

MATH_LEVELS = '0a 0b 1 2 3 4 5a 5b 6a 6b 7 8'
MATH_LEVELS = MATH_LEVELS.split()
ENG_LEVELS = 'F1 G1 H1 I1 J1 K1 L1 M1 N1 O1'
ENG_LEVELS = ENG_LEVELS.split()

MATH_BOOKS = []
ENG_BOOKS = []

# MAKING REFERENCE LISTS OF ALL MATH AND ENGLISH LEVELS.
# INSTEAD OF EACH STUDENT HAVING A LIST, ADVANCING A STUDENT'S BOOKS
# WILL REQUIRE REFERENCING THESE TWO MASTER LISTS.
# THIS SHOULD SIGNIFICANTLY REDUCE THE PROCESSING LOAD.
for level in MATH_LEVELS:
    for book in alpha:
        if level == '0a':
            if book == 'H':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'I':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'N':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'O':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'S':
                MATH_BOOKS.append(f"{level} {book} (MDTRM3 NXT WK)")
            elif book == 'T':
                MATH_BOOKS.append(f"{level} MDTRM3 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '0b':
            if book == 'I':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'J':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'Q':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'R':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '1':
            if book == 'L':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'M':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '2':
            if book == 'I':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'J':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'R':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'S':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '3':
            if book == 'K':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'L':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '4':
            if book == 'K':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'L':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'R':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'S':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '5a':
            if book == 'I':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'J':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'R':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'S':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '5b':
            if book == 'F':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'G':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'K':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'L':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'P':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Q':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
                break
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '6a':
            if book == 'E':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'F':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'Q':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'R':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '6b':
            if book == 'H':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'I':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'O':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'P':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '7':
            if book == 'F':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'G':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'O':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'P':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'U':
                MATH_BOOKS.append(f"{level} {book} (MDTRM3 NXT WK)")
            elif book == 'V':
                MATH_BOOKS.append(f"{level} MDTRM3 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

        if level == '8':
            if book == 'E':
                MATH_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'F':
                MATH_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'J':
                MATH_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'K':
                MATH_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'R':
                MATH_BOOKS.append(f"{level} {book} (MDTRM3 NXT WK)")
            elif book == 'S':
                MATH_BOOKS.append(f"{level} MDTRM3 & {book} to home")
            elif book == 'Y':
                MATH_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                MATH_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                MATH_BOOKS.append(f"{level} {book}")

for level in ENG_LEVELS:
    for book in alpha:
        if level == 'F1' or level == 'G1' or level == 'H1' or level == 'I1' or level == 'J1'\
                or level == 'K1' or level == 'M1':
            if book == 'H':
                ENG_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'I':
                ENG_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'P':
                ENG_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'Q':
                ENG_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                ENG_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                ENG_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                ENG_BOOKS.append(f"{level} {book}")

        if level == 'L1':
            if book == 'E':
                ENG_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'F':
                ENG_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'K':
                ENG_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'L':
                ENG_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                ENG_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                ENG_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                ENG_BOOKS.append(f"{level} {book}")

        if level == 'N1':
            if book == 'O':
                ENG_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'P':
                ENG_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'Y':
                ENG_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                ENG_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                ENG_BOOKS.append(f"{level} {book}")

        if level == 'O1':
            if book == 'I':
                ENG_BOOKS.append(f"{level} {book} (MDTRM1 NXT WK)")
            elif book == 'J':
                ENG_BOOKS.append(f"{level} MDTRM1 & {book} to home")
            elif book == 'P':
                ENG_BOOKS.append(f"{level} {book} (MDTRM2 NXT WK)")
            elif book == 'Q':
                ENG_BOOKS.append(f"{level} MDTRM2 & {book} to home")
            elif book == 'Y':
                ENG_BOOKS.append(f"{level} {book} (FNL NXT WK)")
            elif book == 'Z':
                ENG_BOOKS.append(f"{level} FNL & {book} to home")
            else:
                ENG_BOOKS.append(f"{level} {book}")

def create_blank_json():
    # Create an empty dictionary to store the data
    db = {}
    db["STUDENTS"] = []
    db["STAFF"] = []
    # Create an empty JSON file
    with open(db_name, 'w') as f:
        json.dump(db, f, indent = 2)
if os.path.exists(db_name) == False:
    create_blank_json()
    print("CREATING NEW JSON")

with open(db_name, 'r') as f:
    db = json.load(f)
# USER-INPUT-BASED DELETE. NOT IN USE
def delete():
    # Getting first and last names
    FIRST = input('First name: ')
    LAST = input('Last name: ')
    # Combining them to make one full name. THIS is what goes into the dictionary.
    name = f"{FIRST.strip().title()} {LAST.strip().title()}"
    role = input("Role: ")
    if role.upper() == 'STUDENT':
        role = 'STUDENTS'
    if role.upper() == 'STAFF' or role.upper() == 'ADMIN' or role.upper() == 'TEACHER':
        role = 'STAFF'
    # Iterating through the list to check each individual entry, so starting with i = 0.
    i = 0
    for entry in db[role]:
        # If there's a match, delete person.
        if entry["NAME"][2] == name:
            del db[role][i]
            print(f"{name} deleted successfully.")
        i += 1
    # Dump updated db into json.
    with open(db_name, 'w') as f:
        json.dump(db, f, indent=2)
# USER-INPUT-BASED SEARCH. NOT IN USE
def search():
    FIRST = input('First name: ')
    LAST = input('Last name: ')
    name = f"{FIRST.strip().title()} {LAST.strip().title()}"
    role = input("Role: ")
    if role.upper() == 'STUDENT':
        role = 'STUDENTS'
    if role.upper() == 'STAFF' or role.upper() == 'ADMIN' or role.upper() == 'TEACHER':
        role = 'STAFF'
    i = 0
    # Making a list of all the matches, in case there are multiple.
    matches = []
    for entry in db[role]:
        if entry["NAME"] == name:
            matches.append(entry)
    # List the data of all matches
    for match in matches:
        for category, data in match.items():
            print(f"{category.title()}: {data.title()}")
    # If there aren't any matches, notify the user.
    if len(matches) == 0:
        print(f"No {role.lower()} named {name} exists.")
    i += 1
# CLASS-BASED DELETE. NOT IN USE
def ADD_OBJ(Person):
    if Person.role == 'Student':
        student = {
            "NAME": Person.name,
            "TIME SLOT": Person.time,
            "TEACHER": Person.teacher
        }
        if hasattr(Person, 'math'):
            student['MATH'] = Person.math
        if hasattr(Person, 'eng'):
            student['ENG'] = Person.eng
        db['STUDENTS'].append(student)
    if Person.role == 'Teacher' or Person.role == 'Admin' or Person.role == 'Staff':
        staff = {
            "NAME": Person.name,
            "ROLE": Person.role
        }
        db['STAFF'].append(staff)
    with open(db_name, 'w') as f:
        json.dump(db, f, indent=2)
# CLASS-BASED DUPLICATE CHECK. IN USE FOR TESTING.
# CAN PROBABLY BE DELETED AFTER FIRST GROUP OF TESTING STUDENTS ARE FINE-TUNED.
def STUDENT_OBJ_ALREADY_EXISTS(Person):
    NAME = Person.name
    FIRST = NAME.split()[0]
    LAST = NAME.split()[1]
    ROLE = Person.role.upper()
    if ROLE == 'STUDENT':
        ROLE = 'STUDENTS'
    if ROLE == 'STAFF' or ROLE == 'ADMIN' or ROLE == 'TEACHER':
        ROLE = 'STAFF'
    i = 0
    exists = False
    for entry in db[ROLE]:
        if entry["NAME"] == NAME:
            exists = True
    return exists

# CLASS BASED FUNCTIONS (USING THE PERSON OBJECT) SEEM TO BE A LITTLE CLUNKY.
# FROM HERE ON OUT I'LL USE STRAIGHTFORWARD (NAME, ROLE, **KWARGS)-BASED FUNCTIONS.
# MIGHT NEED TO REWRITE A COUPLE TO MAKE SURE THEY'RE ALL WORKING COHESIVELY.
def ADD(name, role, **kwargs):
    NAME = name.title()
    ROLE = role.upper()
    if ROLE == 'STUDENT':
        ROLE = 'STUDENTS'
        person = {
            "NAME": NAME
        }
        for key, value in kwargs.items():
            person[key] = value
        #db['STUDENTS'].append(student)
    if ROLE == 'STAFF' or ROLE == 'ADMIN' or ROLE == 'TEACHER':
        ROLE = 'STAFF'
        person = {
            "NAME": NAME
        }
        for key, value in kwargs.items():
            person[key] = value
        #db['STAFF'].append(person)
    if PERSON_ALREADY_EXISTS(NAME, ROLE):
        pass
    else:
        db[ROLE].append(person)
        with open(db_name, 'w') as f:
            json.dump(db, f, indent=2)

def EDIT(name, role, **kwargs):
    NAME = name.title()
    ROLE = role.upper()
    if ROLE == 'STUDENT':
        ROLE = 'STUDENTS'
    if ROLE == 'STAFF' or ROLE == 'ADMIN' or ROLE == 'TEACHER':
        ROLE = 'STAFF'
    FOUND = False
    for entry in db[ROLE]:
        if entry['NAME'] == NAME:
            FOUND = True
            for key, value in kwargs.items():
                if key in ['NAME', 'TIME_SLOT', 'TEACHER', 'DAY',
                            'PROGRAMS', 'LOCATION', 'NOTES', 'CONTACT', 'DOB']:
                    entry[key] = value
            break
    if FOUND == False:
        print(f'{ROLE} {NAME} NOT FOUND')

    with open(db_name, 'w') as f:
        json.dump(db, f, indent=2)

def DELETE(name, role):
    NAME = name.title()
    ROLE = role.upper()
    if ROLE == 'STUDENT':
        ROLE = 'STUDENTS'
    if ROLE == 'STAFF' or ROLE == 'ADMIN' or ROLE == 'TEACHER':
        ROLE = 'STAFF'
    # Iterating through the list to check each individual entry, so starting with i = 0.
    i = 0
    for entry in db[ROLE]:
        # If there's a match, delete person.
        if entry["NAME"] == NAME:
            del db[ROLE][i]
            #print(f"{name} deleted successfully.")
        i += 1
    # Dump updated db into json.
    with open(db_name, 'w') as f:
        json.dump(db, f, indent=2)

def SEARCH(name, role):
    NAME = name.title()
    ROLE = role.upper()
    if ROLE == 'STUDENT':
        ROLE = 'STUDENTS'
    if ROLE == 'STAFF' or ROLE == 'ADMIN' or ROLE == 'TEACHER':
        ROLE = 'STAFF'
    i = 0
    matches = []
    for entry in db[ROLE]:
        if entry["NAME"] == NAME:
            matches.append(entry)
    for match in matches:
        for category, data in match.items():
            print(f"{category.title()}: {data.title()}")
    if len(matches) == 0:
            print(f"No {ROLE.lower()} named {NAME} exists.")
    i += 1

def PERSON_ALREADY_EXISTS(name, role):
    NAME = name.title()
    ROLE = role.upper()
    if ROLE == 'STUDENT':
        ROLE = 'STUDENTS'
    if ROLE == 'STAFF' or ROLE == 'ADMIN' or ROLE == 'TEACHER':
        ROLE = 'STAFF'
    i = 0
    exists = False
    for entry in db[ROLE]:
        if entry["NAME"] == NAME:
            exists = True
    return exists

def ADVANCE_MATH(NAME):
    NAME = NAME.title()
    i = 0
    for entry in db['STUDENTS']:
        if entry['NAME'] == NAME:
            current_book = entry['MATH']
            loc = MATH_BOOKS.index(current_book)
            next_book = MATH_BOOKS[loc + 1]
            entry['MATH'] = next_book
            break
        i += 1
    with open(db_name, 'w') as f:
        json.dump(db, f, indent=2)

def ADVANCE_ENG(NAME):
    NAME = NAME.title()
    i = 0
    for entry in db['STUDENTS']:
        if entry['NAME'] == NAME:
            current_book = entry['ENG']
            loc = ENG_BOOKS.index(current_book)
            next_book = ENG_BOOKS[loc + 1]
            entry['ENG'] = next_book
            break
        i += 1
    with open(db_name, 'w') as f:
        json.dump(db, f, indent=2)

def ADD_BOOK(NAME, **kwargs):
    NAME = NAME.title()
    i = 0
    for entry in db['STUDENTS']:
        if entry['NAME'] == NAME:
            if 'MATH' in kwargs:
                entry['MATH'] = kwargs['MATH']
            if 'ENG' in kwargs:
                entry['ENG'] = kwargs['ENG']
            if 'GK' in kwargs:
                entry['GK'] = kwargs['GK']
            if 'CODING' in kwargs:
                entry['CODING'] = kwargs['CODING']
        i += 1
    with open(db_name, 'w') as f:
        json.dump(db, f, indent=2)
