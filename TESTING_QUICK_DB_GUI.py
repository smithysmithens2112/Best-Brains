import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import custom_widgets as ctk
import json, sys, os
from pprint import pprint

def sort_by(list_of_dicts, value):
    sorted_list_of_dicts = sorted(list_of_dicts,
                                  key= lambda d: d[f'{value}'])
    return sorted_list_of_dicts

with open('TEMP_DB.json', 'r') as f:
    db = json.load(f)
    students = [student for student in db['STUDENTS']]
    #students = sort_by(students, 'NAME')
    names = [student['NAME'] for student in db['STUDENTS']]
    #names.sort()

number_of_students = len(students)
images = []

def DB(master):

    root = ttk.Frame(master)
    style = ttk.Style('litera')
    style.configure('Treeview', borderwidth=0, font="-size 16", rowheight=20)
    style.configure('Label', font="-size 20")
    style.configure('TLabel', font="-size 18")
    style.configure('name.TLabel', font='-size 30')
    style.configure('name.TFrame')
    style.configure('title.TLabel', font='-size 20')
    style.configure('info.TLabel', font='-size 18')
    style.configure('img.TButton', borderwidth=0)
    style.map("img.TButton",
              background=[('!active', '#ffffff'),
                          ('pressed', '#ffffff'),
                          ('active', '#ffffff')])

    def populate_info(event):
        selection = ALL.selection()[0]
        id = ALL.index(selection)
        student = students[id]
        try:
            name_label.configure(text=f"{selection} {student['TEACHER']}")
        except Exception:
            print(Exception)
            print(selection)
        for widget in info_frame.winfo_children():
            widget.destroy()

        program_frame = ttk.Frame(info_frame)
        program_frame.grid(row=0, column=0, padx=10, pady=5)
        programs_label = ttk.Label(program_frame, text='Programs', style='title.TLabel')
        programs_label.pack(side=LEFT, expand=True, fill=X)

        row = 1
        for program in student['PROGRAMS']:
            student_book = student['PROGRAMS'][program]
            subject = ttk.Label(info_frame, text=f'{program.title()}: ')
            subject.grid(row=row, column=0, padx=(30, 0), pady=5, sticky=W)

            if len(student_book) == 0:
                book = ttk.Label(info_frame, text='-', style='info.TLabel')
                book.grid(row=row, column=1, padx=(30, 0), pady=5, sticky=W)
                row += 1
            else:
                book = ttk.Label(info_frame, text=student_book, style='info.TLabel')
                book.grid(row=row, column=1, padx=(30, 0), pady=5, sticky=W)
                row += 1

#        math_label = ttk.Label(info_frame, text=f'Math: {}', style='title.TLabel')

    bodyframe = ttk.Frame(root)
    bodyframe.pack(fill=BOTH, side=TOP, expand=True)

    lframe = ttk.Labelframe(bodyframe, text='Students', padding=18)
    lframe.pack(side=LEFT, fill=Y, expand=False, padx=(20, 10), pady=20)

    ALL = ttk.Treeview(lframe, show='tree', selectmode='browse', takefocus=False)

    for student in names:
        ALL.insert('', 'end', student, text=student)
    ALL.pack(side=LEFT, fill=BOTH, expand=True, anchor=NE)

    scroll = ttk.Scrollbar(lframe, orient='vertical', command=ALL.yview)
    scroll.pack(side=LEFT, fill=Y)
    ALL.configure(yscrollcommand=scroll.set)
    ALL.bind('<<TreeviewSelect>>', populate_info)

    rframe = ttk.Labelframe(bodyframe, text='Info')
    rframe.pack(side=LEFT, expand=True, fill=BOTH, padx=(10, 20), pady=20)

    name_frame = ttk.Frame(rframe, style='name.TFrame')
    name_frame.pack(side=TOP, expand=False, fill=Y)

    name_label = ttk.Label(name_frame, text=f"Student Records", style='name.TLabel')
    name_label.pack(side=LEFT, expand=True, fill=BOTH, padx=10)

    sep = ttk.Separator(rframe)
    sep.pack(side=TOP, expand=False, fill=X, padx=30, pady=5)


    info_frame = ttk.Frame(rframe)
    info_frame.pack(side=TOP, expand=True, fill=BOTH, padx=20, pady=10)

    return root

if __name__ == '__main__':
    app = ttk.Window('Baby Database')
    app.state('zoomed')

    bagel = DB(app)
    bagel.pack(fill=BOTH, expand=YES)

    app.mainloop()
