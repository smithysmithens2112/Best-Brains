import datetime as dt
import gspread as gs
import gspread_formatting as gsf
from Google import Create_Service
import requests
import json
from datetime import timedelta, datetime

######################################## ESSENTIALS ########################################
Table = 4                                                                                  #
# Gets current date                                                                        #
date = dt.datetime.now()                                                                   #
# Formats date like Ram does                                                               #
date = f'{date.strftime("%a")} ({date.strftime("%m")}/{date.strftime("%d")}/{date.strftime("%Y")})'                                                          #
# Alphabet                                                                                 #
alpha = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'                              #
alpha = alpha.split()                                                                      #
############################################################################################

#################################### SETTING UP GSPREAD ####################################
# GSPREAD WILL MAINLY HANDLE MAKING ALL THE CELLS THE CORRECT SIZE, TEXT WRAPPING, ETC.    #
# testing@best-brains-schedule-builder.iam.gserviceaccount.com
                                                                                           #
# Setting up the service account, showing credentials, etc.                                #
sa = gs.service_account(filename='SCHEDULE_BUILDER_CREDENTIALS.json')                      #
# RECALL THAT EXCEL/GOOGLE SHEETS FILES CONTAIN MULTIPLE PAGES (AKA WORKSHEETS).           #
# WITHIN ONE FILE WE CAN HAVE MULTIPLE SHEETS. SHEET1 IS CONTAINED WITHIN "TEST".          #
# Opening up a file titled "TEST"                                                          #
sh = sa.open('TEST')                                                                       #
# Picking which worksheet to access within the "TEST" file                                 #
wks = sh.worksheet('Sheet1')                                                               #
id = sh.id                                                                                 #
############################################################################################

def reset_sheet():
    wks.clear()
    gsf.set_row_height(wks, '1:50', 10)
    gsf.set_column_width(wks, 'A:Z', 10)
    wks.format(f'A1:Z50', {'backgroundColor': {'red': 1, 'green': 1, 'blue': 1}})

reset_sheet()

################################### SETTING UP SHEETS API ##################################
# SHEETS WILL HANDLE ALL THE DATA. IT CAN UPLOAD LOTS OF DATA ALL AT ONCE,                 #
# RATHER THAN MANY SMALL UPLOAD, WHICH OVERWORK THE SERVER AND THROW ERRORS.               #
                                                                                           #
CLIENT_SECRET_FILE = 'sheets_credentials.json'                                             #
API_NAME = 'sheets'                                                                        #
API_VERSION = 'v4'                                                                         #
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']                                  #
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)                #
############################################################################################

##################################################### THE DATABASE #####################################################
# OPENS DB FILE
with open('BEST_BRAINS_DB.json', 'r') as f:
    db = json.load(f)
    # VERY IMPORTANT! SORTS STUDENTS BY TIME SO FIRST CLASS STARTS AT TOP LEFT!
    db = sorted(db['STUDENTS'], key=lambda student: student['TIME'])
# MAKES A LIST OF ALL THE TIME SLOTS
times = [student['TIME'] for student in db]
times = list(set(times))
times.sort()
# REMOVES ALL NON-UNIQUE VALUES
classes = list(set(times))
classes.sort()
# ENUMERATES LIST OF TIME SLOTS (STARTING FROM 1).
# THIS ALLOWS US TO CONVENIENTLY LINK THE TIME SLOT WITH THE CORRECT COLUMN
enum_classes = list(enumerate(classes, 1))
# ENUMERATE LEAVES US WITH A LIST OF TUPLES OF THE FORM (INDEX, TIME SLOT)
# SO WE JUST WANT THE INDEX OF THE LAST TIME SLOT.
# THIS VALUE IS THE TOTAL NUMBER OF CLASSES IN THE DAY.
num_classes = enum_classes[-1][0]
########################################################################################################################

############################ USING SHEETS API TO LOAD ALL THE TEXT ########################
# TELLING SHEETS WHICH SHEET TO WORK ON
worksheet_name = 'Sheet1!'
# WHICH CELL TO START ON
cell_range_insert = 'A1'
# SETTING UP MERGED CELLS
# Sheet ID (not the same as the entire file's key. Just the ID for the individual page.
gid = 0
# REQUEST
merge_date_cells_request = [
    {'mergeCells': {
        'mergeType': 'MERGE_ALL',
        'range': {
            'endColumnIndex': num_classes + 1,
            'endRowIndex': 1,
            'sheetId': gid,
            'startColumnIndex': 1,
            'startRowIndex': 0
        }
    }}
]

# Executing merge request
service.spreadsheets().batchUpdate(spreadsheetId=id,body={'requests': merge_date_cells_request}).execute()

# VALUES MUST BE A TUPLE OF TUPLES, BUT IT NEEDS TO BE CREATED DYNAMICALLY.
# STARTING WITH VALUES AS A LIST SO THAT WE CAN BUILD IT UP DYNAMICALLY,
# THEN WE CONVERT IT INTO A TUPLE.
values = []
head = ['', date]
for i in range(num_classes - 1):
    head.append('')
head.append('Notes')
values.append(tuple(head))
values.append([f"Table {Table}"])
for time in times:
    values[1].append(time)
################################################# PUTTING THIS ON HOLD #################################################
# THIS PART WORKS VERY WELL, BUT THE CHEAT SHEET STILL ISN'T IMPLEMENTED 100% CORRECTLY,
# SO THERE'S A LIMIT TO HOW WELL THE SCHEDULE CAN BE MADE.
# LET'S KEEP WORKING ON IMPLEMENTING THE CHEAT SHEET AND THEN COME BACK TO CHECK THIS PART LATER.

# PUTTING IN ALL OF THE NAMES AND BOOKS
row = 3
for student in db:
    NAME = student['NAME']
    if student['SLOT'] == "FIRST HALF":
      time = student['TIME'].split('-')
      start_time = time[0]
      start_time = datetime.strptime(start_time, '%H:%M')
      end_time = start_time + timedelta(hours=.5)
      TIME = f"{start_time.hour}:{start_time.minute}-{end_time.hour}:{end_time.minute}"
      if 'MATH' in student:
        NAME += f'\nMath Only {TIME}'
      if 'ENG' in student:
        NAME += f'\nEng Only {TIME}'
    if student['SLOT'] == "SECOND HALF":
      time = student['TIME'].split('-')
      start_time = time[0]
      start_time = datetime.strptime(start_time, '%H:%M')
      start_time = start_time + timedelta(hours=.5)
      end_time = datetime.strptime(time[1], '%H:%M')
      TIME = f"{start_time.hour}:{start_time.minute}-{end_time.hour}:{end_time.minute}"
      if 'MATH' in student:
        NAME += f'\nMath Only {TIME}'
      if 'ENG' in student:
        NAME += f'\nEng Only {TIME}'
    for enum in enum_classes:
        if enum[1] == student['TIME']:
            hour = enum[0]
    if 'MATH' in student:
        MATH = student['MATH']
    if 'ENG' in student:
        ENG = student['ENG']
    list = [NAME]
    for hour in range(hour - 1):
        list.append('')
    if 'MATH' in student and not 'ENG' in student:
        list.append(f"Math {MATH}")
    elif 'ENG' in student and not 'MATH' in student:
        list.append(f"Eng {ENG}")
    elif 'MATH' in student and 'ENG' in student:
        list.append(f"Math {MATH}\nEng {ENG}")
    values.append(tuple(list))
    row += 1
# Now add the Makeup Class row at the very bottom
values.append(tuple(['Makeup Classes:']))
# Convert the whole thing into a tuple
values = tuple(values)
# UPLOADING TO SHEET
value_range_body = {'majorDimension': 'ROWS', 'values': values}
service.spreadsheets().values().update(spreadsheetId=id, valueInputOption='USER_ENTERED',
                                       range = worksheet_name + cell_range_insert,
                                       body = value_range_body).execute()

# Number of Notes column, but we need to convert that to a letter.
notes_col_num = num_classes + 1
notes_col_alpha = alpha[notes_col_num]
# Color Notes row
wks.format(f'A1:{notes_col_alpha}1', {'backgroundColor': {'red': 1, 'green': .9, 'blue': .6}})
# Color Hours row
wks.format(f'A2:{notes_col_alpha}2', {'backgroundColor': {'red': .8, 'green': .8, 'blue': .8}})
# Color Makeup Classes row
wks.format(f'A{row}:{notes_col_alpha}{row}', {'backgroundColor': {'red': 0, 'green': 1, 'blue': 0}})
# Bold Table cell
wks.format('A2', {'textFormat': {'bold': True}})
# Center Date
wks.format('B1', {'horizontalAlignment': 'CENTER'})
# Center notes
wks.format(f'{notes_col_alpha}1', {'horizontalAlignment': 'CENTER'})
# Wrap text
wks.format('A1:Z50', {"wrapStrategy": "WRAP"})

# SIZING ROWS AND COLUMNS
# Sizing Notes and times rows
gsf.set_row_height(wks, f'1:2', 20)
# Sizing names and books rows
gsf.set_row_height(wks, f'3:{row}', 70)
# Sizing names and books columns
num_cols_no_notes = num_classes
gsf.set_column_width(wks, f'A:{alpha[num_cols_no_notes]}', 128)
# Sizing notes column
gsf.set_column_width(wks, notes_col_alpha, 250)

# Each border request is just requesting cell borders in different places
border_request1 = {
  "requests": [
    {
      "updateBorders": {
        "range": {
          "sheetId": gid,
          "startRowIndex": 1,
          "endRowIndex": row,
          "startColumnIndex": 0,
          "endColumnIndex": notes_col_num + 1
        },
        "top": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "bottom": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "right": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "left": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "innerHorizontal": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "innerVertical": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
      }
    }
  ]
}
border_request2 = {
  "requests": [
    {
      "updateBorders": {
        "range": {
          "sheetId": gid,
          "startRowIndex": 0,
          "endRowIndex": 1,
          "startColumnIndex": 0,
          "endColumnIndex": 1
        },
        "top": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "bottom": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "right": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "left": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "innerHorizontal": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "innerVertical": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
      }
    }
  ]
}
border_request3 = {
  "requests": [
    {
      "updateBorders": {
        "range": {
          "sheetId": gid,
          "startRowIndex": 0,
          "endRowIndex": 1,
          "startColumnIndex": notes_col_num,
          "endColumnIndex": notes_col_num + 1
        },
        "top": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "bottom": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "right": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "left": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "innerHorizontal": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "innerVertical": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
      }
    }
  ]
}
border_request4 = {
  "requests": [
    {
      "updateBorders": {
        "range": {
          "sheetId": gid,
          "startRowIndex": 0,
          "endRowIndex": 1,
          "startColumnIndex": 1,
          "endColumnIndex": notes_col_num
        },
        "top": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "bottom": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "right": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "left": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
        "innerHorizontal": {
          "style": "SOLID",
          "width": 1,
          "color": {
            "blue": 0.0
          },
        },
      }
    }
  ]
}

# Executing border requests
service.spreadsheets().batchUpdate(spreadsheetId=id, body=border_request1).execute()
service.spreadsheets().batchUpdate(spreadsheetId=id, body=border_request2).execute()
service.spreadsheets().batchUpdate(spreadsheetId=id, body=border_request3).execute()
service.spreadsheets().batchUpdate(spreadsheetId=id, body=border_request4).execute()

# DOWNLOADING THE PDF
url = (f'https://docs.google.com/spreadsheets/d/{id}/export?gid={gid}&format=pdf&fitw=true'
       f'&top_margin=.75&bottom_margin=.75&left_margin=0.70&right_margin=0.70'
       f'&horizontal_alignment=CENTER&scale=4&gridlines=false')
response = requests.get(url, stream=True)

with open('SCHEDPDF.pdf', 'wb') as f:
    f.write(response.content)

################################################## WORKS PERFECTLY!!! ##################################################
# NOW WE NEED THE DATABASE

# 3/1/2023: DATABASE IS WORKING WELL AND IS BEING FED BY THE CHEAT SHEET.
# THE ONLY THING BUGGING ME RIGHT NOW IS THAT THE PDF LOOKS A LITTLE STRANGE ON THE PAGE,
# BUT THAT MIGHT JUST BE THE WAY THINGS ACTUALLY ARE.
# AS OF NOW, MY EXPORTED PDFS ARE INDISTINGUISHABLE FROM THOSE EXPORTED DIRECTLY THROUGH GOOGLE SHEETS IN THE BROWSER.
# JUST NEED TO DOUBLE CHECK RAM'S MARGINS.

# ALSO NEED TO BRING IN NAME NOTES.

