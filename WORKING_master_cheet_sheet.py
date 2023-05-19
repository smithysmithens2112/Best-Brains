import json
import gspread as gs
import gspread_formatting as gsf
from Google import Create_Service
from WORKING_database_code import *
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
from time import time
from pprint import pprint
import os

# MAKING A SPREADSHEET ALPHABET THAT EXTENDS BEYOND Z.
# EX. A-Z, AA, AB, AC, AD...CZ
# THIS WILL BE USED TO ITERATE THROUGH ROWS OF THE SPREAD SHEET

def check_for_list_of_empty_strings(args):
    empty = True
    for arg in args:
        if arg != '':
            empty = False
            break
    return empty

def class_is_empty(MASTER, location, day, teacher):
    empty_class = True
    for hour in MASTER[location][day][teacher]:
        empty = check_for_list_of_empty_strings(MASTER[location][day][teacher][hour])
        if empty == False:
            empty_class = False
            break
    return empty_class

def get_cheatsheet():
    alpha_extended = alpha
    alpha_list = []
    for ALPHA in alpha[:3]:
        for extension in alpha_extended:
            txt = f"{ALPHA}{extension}"
            alpha_list.append(txt)
    alpha_extended += alpha_list

    def get_size(range):
        range = range.split(':')
        start = range[0]
        end = range[1]
        start_col = alpha.index(start[0])
        end_col = alpha.index(end[0])
        width = end_col - start_col + 1

        start_row = int(start[1:])
        end_row = int(end[1:])
        height = end_row - start_row + 1
        return width, height

    def sort_time(times):
        temp = []
        time_zero = datetime(1900, 1, 1)
        for time in times:
            first, second = time.split('-')
            first = datetime.strptime(first, '%H:%M')
            minutes = (first - time_zero).total_seconds()/60
            thing = (minutes, time)
            temp.append(thing)
        temp.sort()
        sorted_times = [time[1] for time in temp]
        return sorted_times

    CLIENT_SECRET_FILE = 'sheets_credentials.json'
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    MASTER = {}

    locations = ['Leander', 'Avery Ranch']
    for location in locations:
        #try:
            sheet = f"In-Person {location}"
            sa = gs.service_account(filename='SCHEDULE_BUILDER_CREDENTIALS.json')
            sh = sa.open(f"Latest Copy of {location} Cheat Sheet")
            wks = sh.worksheet(sheet)
            id = sh.id

            sheet_metadata = service.spreadsheets().get(spreadsheetId=id).execute()
            sheets = sheet_metadata.get('sheets', '')
            title = sheets[4].get("properties", {}).get("title", "Sheet1")
            sheet_id = sheets[4].get("properties", {}).get("sheetId", 0)

            ########################################### STUFF THAT APPLIES TO ALL CLASSES ##########################################
            range_name = '1:70'
            result = service.spreadsheets().values().get(
                        spreadsheetId=id, range=f"{sheet}!{range_name}").execute()
            rows = result.get('values', [])
            result = service.spreadsheets().values().get(
                        spreadsheetId=id, range=f"{sheet}!{range_name}", majorDimension='COLUMNS').execute()
            columns = result.get('values', [])
            info = service.spreadsheets().get(spreadsheetId=id, ranges=f"{sheet}!{range_name}", includeGridData=True).execute()
            info = info['sheets'][0]
            color = info['data'][0]['rowData'][0]['values'][0]['effectiveFormat']['backgroundColor']
            merge_data = info['merges']

            max_length = max([len(col) for col in columns])
            for col in columns:
                while len(col) < max_length:
                    col.append("")

            # GENERATES A LIST OF TUPLES OF ALL THE MERGED CELLS
            # FIRST VALUE IS STARTING CELL, SECOND VALUE IS ENDING CELL, THIRD VALUE IS WIDTH OF MERGED CELL.
            merged_cells = [(cell['startRowIndex'], cell['startColumnIndex'],
                             cell['endColumnIndex'] - cell['startColumnIndex']) for cell in merge_data]

            # FINDING CELLS I ACTUALLY WANT TO USE.
            accessible_cells = []
            width, height = len(columns), len(rows)
            # FIRST WE MAKE A LIST OF ALL CELLS IN THE RANGE
            for row in range(len(rows)):
                for col in range(len(columns)):
                    accessible_cells.append((row, col))
            # NEXT WE PICK THROUGH THE CELLS AND MAKE A LIST OF WHAT SHOULD BE REMOVED.
            remove = []
            # GOING THROUGH ALL OF THE MERGED CELLS
            for merged_cell in merged_cells:
                # IF THE MERGED CELL INDEX IS IN THE LIST OF ALL CELLS...
                if (merged_cell[0], merged_cell[1]) in accessible_cells:
                    # THEN MAKE ANOTHER LIST OF ALL OF THE CELLS EATEN UP BY THE MERGE
                    # AND PUT THEM INTO THE remove LIST.
                    # FOR EXAMPLE, A2 IS MERGED WITH A3-A6, SO WE NEED TO LIST A3, A4, A5 AND A6 AND REMOVE THEM
                    # BECAUSE, AS FAR AS THE GOOGLE SHEETS API IS CONCERNED, THOSE CELLS DON'T EXIST IN THE FIRST PLACE.
                    for col in range(merged_cell[1] + 1, merged_cell[1] + merged_cell[2]):
                        remove.append((merged_cell[0], col))

            # REMOVING THE CELLS
            accessible_cells = [cell for cell in accessible_cells if cell not in remove]

            # GETTING COLOR DATA TO IDENTIFY OPEN SLOTS.
            open_slots = []

            # GOING THROUGH ALL THE CELLS...
            for cell in accessible_cells:
                row = cell[0]
                col = cell[1]
                # AND GETTING THEIR COLOR INFORMATION.
                if 'effectiveFormat' in info['data'][0]['rowData'][row]['values'][col] and col != 0:
                    color_data = info['data'][0]['rowData'][row]['values'][col]['effectiveFormat']['backgroundColor']
                    # IF THEY'RE GREEN, PUT THEM IN open_slots
                    if color_data == {'green': 1}:
                        open_slots.append((row, col))
                        #open_slots['OPEN'].append(f"{alpha[col]}{row + 1}")
                else:
                    pass

            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            '''
            def categorize_students_by_time_slot():
                student_id = 0
                for x in range(len(columns)):
                    for y in range(len(columns[x])):
                        # SETTING THE TIME FOR THE COLUMN
                        if y == 1:
                            TIME = columns[x][y]
                        # GETTING THE KID'S NAME
                        else:
                            kid = columns[x][y]
                            name = kid.split('/n')
                            name = name[0].split()
                            # CHECKS IF name IS EMPTY USING THE INHERENT "BOOLEANESS" OF LISTS.
                            # EMPTY LISTS HAVE BOOLEAN VALUES OF FALSE
                            if name:
                                first = name[0].title()
                                if len(name) > 1:
                                    possible_last = name[1].title()
                                    if possible_last in ['Dropping', 'Resume', 'Vacation',
                                                         'Break', 'Math', 'Eng', 'M&E']:
                                        name = first
                                    else:
                                        name = f"{first} {possible_last}"
                                else:
                                    name = first

                        # MARKING OPEN SLOTS AS (OPEN)
                        if (y, x) in open_slots and kid == "":
                            columns[x][y] = '(OPEN)'
                        # IF KID IS IN A MERGED CELL, LABEL AS FULL HOUR AND ADD TO DATABASE
                        if (y, x) in [(cell[0], cell[1]) for cell in merged_cells if cell[1] > 0]\
                                and kid not in days and kid != '' and kid != '(OPEN)':
                            TIME = TIME.split('-')
                            start_time = TIME[0]
                            start_time = datetime.strptime(start_time, '%H:%M')
                            end_time = start_time + timedelta(hours=1)
                            TIME = f"{start_time.hour}:{start_time.minute}-{end_time.hour}:{end_time.minute}"
                            ADD(name, 'student', TIME=TIME, SLOT='FULL HOUR', ID=str(student_id).zfill(4))
                            student_id = int(student_id) + 1
                        # OTHERWISE...
                        elif kid not in days and kid != '' and kid != '(OPEN)' \
                                and 'Mr' not in name.title() and 'Ms' not in name.title() \
                                and 'Mrs' not in name.title() and x > 0:
                            # IF KID IS IN ODD COLUMN, LABEL AS FIRST HALF HOUR AND ADD TO DATABASE
                            if x % 2 == 1:
                                ADD(name, 'student', TIME=TIME, SLOT='FIRST HALF', ID=str(student_id).zfill(4))
                                student_id = int(student_id) + 1
                            # OR IF KID IS IN EVEN COLUMN, LABEL AS SECOND HALF HOUR AND ADD TO DATABASE
                            if x % 2 == 0:
                                ADD(name, 'student', TIME=TIME, SLOT='SECOND HALF', ID=str(student_id).zfill(4))
                                student_id = int(student_id) + 1
            '''

            #def assign_time_slot():
                # I THINK THIS FUNCTION SHOULD GO IN THE ELSE CLAUSE
                # WHERE STUDENTS ARE APPENDED TO CHEATSHEET (LINE 320).
                # FULL HOUR STUDENTS CAN BE FOUND BY LOOKING AT THE CELL TO THEIR RIGHT.
                # IF kid IS IN ODD ROW AND NEIGHBORING SLOT IS (OPEN), kid IS FULL HOUR.
                # IF kid IS IN ODD ROW AND NEIGHBORING SLOT IS NOT (OPEN), kid IS FIRST HALF.
                # IF kid IS IN EVEN ROW, SECOND HALF.

            #categorize_students_by_time_slot()

            ######################################## END STUFF THAT APPLIES TO ALL CLASSES #########################################

            ############################### FINDING AND LOOPING THROUGH EACH CLASS FOR EACH TEACHER ################################

            # SETTING UP A LIST OF EACH DAY FOR A GIVEN TEACHER
            sched_days = [day for day in rows[0] if day != '']

            teacher_index = []
            for row_index, row in enumerate(rows):
                for col_index, item in enumerate(row):
                    if ('Mr.' in item.title() or 'Ms.' in item.title() or 'Mrs.' in item.title()) \
                            and '\n' not in item and item != row[0] and ([row_index - 1, col_index], item) not in teacher_index:
                        teacher_index.append(([row_index - 1, col_index], item))
            day_cols = list(set([teacher[0][-1] for teacher in teacher_index]))
            day_cols.sort()

            for teacher in teacher_index:
                if teacher[0][-1] in day_cols:
                    teacher[0].append(teacher[0][-1] + 1)
                    while teacher[0][-1] + 1 not in day_cols and teacher[0][-1] + 1 < width:
                        teacher[0].append(teacher[0][-1] + 1)

            # LET'S TRY THIS LAST PART FROM SCRATCH BUT WITH A SLIGHT MODIFICATION:
            # LET'S BUILD UP EACH TEACHER ONE COLUMN AT A TIME.
            # ONCE WE SEE A VALUE CONTAINING 'Mr.', 'Ms.', 'Mrs.', WE'LL CHANGE TEACHER.
            # WE CAN THEN RECORD THE ROW INDEX OF THAT CHANGE (OR REFER TO name_rows)
            # AND SWITCH TEACHER WHENEVER A VALUE CONTAINING 'Mr.', 'Ms.', 'Mrs.' IS FOUND
            # OR WHENEVER A CERTAIN ROW IS REACHED.
            # MIGHT BE A PROBLEM THOUGH WITH HANDLING KUMBA.
            # IF HER VALUE IS FOUND BUT SHE IS IN ALISHMA'S ROW, THINGS MIGHT GET TRICKY.
            day = {}
            col_lengths = []
            for col in columns[1:]:
                column = []
                for kid in col:
                    if ('Mr.' in kid.title() or 'Ms.' in kid.title() or 'Mrs.' in kid.title())\
                            and '\n' not in kid and len(kid) < 20:
                        TEACHER = kid
                        column.append(kid)
                    elif ':' in kid and '\n' not in kid and len(kid) < 12:
                        TIME = kid
                    elif kid.title() in days:
                        DAY = kid
                    elif kid == '':
                        column.append(kid)
                    else:
                        name = kid.split('\n')
                        name = name[0].strip().split()
                        name = ' '.join(name[:2])
                        column.append(name)
                        if 'Seoyul' in kid or 'Shruti' in kid or 'Shrey' in kid or 'Anshul' in kid:
                            print(kid)
                            print()
                            print(name)
                            print('####################################################################')
                if DAY not in day:
                    if column[0] == '':
                        day[DAY] = {TIME: column[1:]}
                    else:
                        day[DAY] = {TIME: column}
                if DAY in day:
                    if column[0] == '':
                        day[DAY][TIME] = column[1:]
                    else:
                        day[DAY][TIME] = column
                col_lengths.append(len(column))

            # EQUALIZES ALL COLUMNS LENGTHS
            max_col_length = max(col_lengths)
            for DAY in day.keys():
                for slot in day[DAY].keys():
                    while len(day[DAY][slot]) + 1< max_col_length:
                        day[DAY][slot].append('')

            teacher = {}
            CHEATSHEET = {}
            COL = 1

            for DAY in day.keys():
                teacher = {}
                for time in day[DAY].keys():
                    rev_kids = list(reversed(day[DAY][time]))
                    students = []
                    ROW = max_col_length - 1
                    for kid in rev_kids:
                        # IF LOOKING IN A TEACHER'S ROW...
                        if ROW in set([row[0][0] for row in teacher_index]):
                            # IF LOOKING AT TEACHER
                            if 'Mr' in kid.title() or 'Ms' in kid.title() or 'Mrs' in kid.title():
                                # SET TEACHER
                                TEACHER = kid
                            elif kid == '':
                                possible_teachers = [teacher for teacher in teacher_index if ROW == teacher[0][0]
                                                     and COL in teacher[0][1:]]
                                TEACHER = possible_teachers[0][1]
                            # IF TEACHER ISN'T ALREADY ENTERED INTO THE teacher DICTIONARY...
                            if TEACHER not in teacher:
                                # MAKE A NEW ENTRY
                                teacher[TEACHER] = {time: list(reversed(students))}
                            # IF TEACHER IS ALREADY ENTERED...
                            elif TEACHER in teacher:
                                teacher[TEACHER][time] = list(reversed(students))
                            # EITHER WAY, CLEAR THE LIST OF STUDENTS TO MAKE ROOM FOR A NEW TEACHER'S CLASS
                            students = []
                        else:
                            students.append(kid)

                        ROW -= 1
                    COL += 1
                CHEATSHEET[DAY] = teacher

            for DAY in CHEATSHEET.keys():
                for TEACHER in CHEATSHEET[DAY].keys():
                    for TIME in CHEATSHEET[DAY][TEACHER].keys():
                        for KID in CHEATSHEET[DAY][TEACHER][TIME]:
                            if KID not in ['', '(OPEN)']:
                                EDIT(KID,
                                     'student',
                                     DAY=DAY,
                                     TEACHER=TEACHER,
                                     LOCATION=location,
                                     PROGRAMS={
                                         'MATH': [],
                                         'ENG': [],
                                         'ABACUS': [],
                                         'CODING': []
                                     })
            MASTER[location] = CHEATSHEET

        #except Exception as e:
        #    print(f"Problem with {location}")
        #    print(e)
        #    continue

    CLEAN_MASTER = {}
    remove = []
    for location in MASTER:
        for day in MASTER[location]:
            for teacher in MASTER[location][day]:
                if class_is_empty(MASTER, location, day, teacher):
                    remove.append((location, day, teacher))
    for location, day, teacher in remove:
        del MASTER[location][day][teacher]

    # SHOULD REALLY FIND A WAY TO REMOVE/SKIP OVER EMPTY CLASSES.
    # RIGHT NOW THESE ARE BEING SKIPPED OVER IN THE TREEVIEW,
    # BUT IT WOULD BE MORE EFFICIENT TO JUST NEVER RECORD THEM AT ALL,
    # OR AT LEAST DELETE THEM BEFORE THEY'RE SHIPPED OFF TO OTHER PARTS OF THE PROGRAM.

    if not os.path.exists('MASTER_CHEATSHEET.json'):
        with open('MASTER_CHEATSHEET.json', 'w') as f:
            json.dump(MASTER, f, indent=3)

get_cheatsheet()

# WORKS GREAT!!!