import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import custom_widgets as ctk
import json, sys, os
from WORKING_master_cheet_sheet import get_cheatsheet

script_dir = os.path.dirname(sys.argv[0])

with open(os.path.join(script_dir, 'TEMP_DB.json'), 'r') as f:
    db = json.load(f)
    students = [student['NAME'] for student in db['STUDENTS']]
    students.sort()
with open(os.path.join(script_dir,'MASTER_CHEATSHEET.json'), 'r') as f:
    CHEATSHEET = json.load(f)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def Main(master):

    root = ttk.Frame(master, padding=10)
    style = ttk.Style('litera')
    style.configure('Treeview', borderwidth=0, font="-size 16", rowheight=20)
    style.configure('TLabel', font="-size 18")
    style.configure('Label', font="-size 20")
    style.configure('Header.TFrame', background='red')
    style.configure('Body.TFrame', background='blue')
    style.configure('lframe.TFrame', background='green')
    style.configure('rframe.TFrame', background='yellow')
    style.configure('sched.TFrame', background='green')
    style.configure('TCheckbutton', font="-size 18")
    style.configure("TEntry", font="-size 18")
    style.configure("instructions.TLabel", font='-size 25')

    def Notes(NAME):

        Notes_window = ttk.Toplevel(master)
        width = 500
        height = 300
        screen_width = Notes_window.winfo_screenwidth()
        screen_height = Notes_window.winfo_screenheight()
        top_left_corner_x = (screen_width - width)//2
        top_left_corner_y = (screen_height - height)//2
        #Notes_window.geometry(f'{width}x{height}+{top_left_corner_x}+{top_left_corner_y}')
        Notes_window.geometry(f'+{top_left_corner_x}+{top_left_corner_y}')
        Notes_window.resizable(False, False)
        Notes_window.title('Edit notes')
        s = ttk.Style('litera')
        s.configure('notes.title.TLabel', font="-size 24 -weight bold")

        notes_header = ttk.Frame(Notes_window, style='notes.TFrame')
        notes_header.pack(expand=NO, fill=X, anchor=N)

        notes_title = ttk.Label(notes_header, text=f"{NAME} Notes", style="notes.title.TLabel")
        notes_title.pack(padx=0, pady=(10, 0))

        ttk.Separator(notes_header).pack(fill=X, padx=30)

        notes_body = ttk.Frame(Notes_window, style='notes.body.TFrame')
        notes_body.pack(fill=BOTH, expand=True, padx=10, pady=10)

        note1 = ttk.Text(notes_body, takefocus=False, height=1, width=30)
        note1.grid(row=0, column=0, padx=5, pady=5)

        var = tk.StringVar()
        options = ['Add to notes column', 'Add to name column', 'Remove note']
        menu1 = ttk.OptionMenu(notes_body, var, 'Add to notes column', *options)
        menu1.config(width=14)
        var.set('Add to notes column')
        menu1.grid(row=0, column=1, padx=5, pady=5)

        note2 = ttk.Text(notes_body, takefocus=False, height=1, width=30)
        note2.grid(row=1, column=0, padx=5, pady=5)

        var = tk.StringVar()
        options = ['Add to notes column', 'Add to name column', 'Remove note']
        menu2 = ttk.OptionMenu(notes_body, var, 'Add to notes column',  *options)
        menu2.config(width=14)
        var.set('Add to notes column')
        menu2.grid(row=1, column=1, padx=5, pady=5)

        note3 = ttk.Text(notes_body, takefocus=False, height=1, width=30)
        note3.grid(row=2, column=0, padx=5, pady=5)

        var = tk.StringVar()
        options = ['Add to notes column', 'Add to name column', 'Remove note']
        menu3 = ttk.OptionMenu(notes_body, var, 'Add to notes column',  *options)
        menu3.config(width=14)
        var.set('Add to notes column')
        menu3.grid(row=2, column=1, padx=5, pady=5)

        return Notes_window

    def Populate_Schedule(event):

        selection = sched.selection()[0]
        selection = selection.split('/')
        if len(selection) > 2:
            TEACHER = selection[0]
            DAY = selection[1]
            LOC = selection[2]
            title.configure(text=f'{TEACHER}   {DAY}   {LOC}')

            for widget in schedule_frame.winfo_children():
                widget.destroy()

            row = 0
            for hour in CHEATSHEET[LOC][DAY][TEACHER]:
                for student in CHEATSHEET[LOC][DAY][TEACHER][hour]:
                    if student != '' and student != '(OPEN)':
                        column = 0
                        check = ttk.Checkbutton(schedule_frame, takefocus=False)
                        check.grid(row=row, column=column, padx=0)
                        check.invoke()
                        check.invoke()
                        column += 1

                        name = ttk.Label(schedule_frame, text=student, takefocus=False)
                        name.grid(row=row, column=column, sticky=W, padx=10, pady=5)
                        column += 1

                        check_math = ttk.Checkbutton(schedule_frame, text='Math:', takefocus=False)
                        check_math.grid(row=row, column=column, padx=(10, 0), pady=5)
                        check_math.invoke()
                        check_math.invoke()
                        column += 1

                        math_book = ctk.EditableLabel(schedule_frame, text='5b G')
                        math_book.grid(row=row, column=column, padx=(2, 10), pady=5)
                        column += 1

                        check_eng = ttk.Checkbutton(schedule_frame, text='Eng:', takefocus=False)
                        check_eng.grid(row=row, column=column, padx=(10, 0), pady=5)
                        check_eng.invoke()
                        check_eng.invoke()
                        column += 1

                        # eng_book = ttk.Label(schedule_frame, text='L1 H')
                        eng_book = ctk.EditableLabel(schedule_frame, text='L1 H')
                        eng_book.grid(row=row, column=column, padx=(2, 10), pady=5)
                        column += 1

                        both = ttk.Checkbutton(schedule_frame, text='Both', takefocus=False)
                        both.grid(row=row, column=column, padx=10, pady=5)
                        both.invoke()
                        column += 1

                        edit_notes = ttk.Button(schedule_frame, text='Edit Notes', takefocus=False,
                                                command=lambda NAME=student: Notes(NAME))
                        edit_notes.grid(row=row, column=column, padx=10, pady=5)
                        column += 1

                        flag_as = ttk.Label(schedule_frame, text='Mark as', takefocus=False)
                        flag_as.grid(row=row, column=column, padx=(5, 0), sticky=W)
                        column += 1

                        flag = ttk.Combobox(schedule_frame, state='readonly', width=10)
                        flag['values'] = ['-', 'Absent', 'New', 'Parent Talk']
                        flag.current(0)
                        flag.grid(row=row, column=column, padx=(2, 15))

                        row += 1

            schedule_frame.columnconfigure(1, weight=1)

    header = ttk.Frame(master)
    header.pack(expand=YES, fill=X, anchor=N)

    title = ttk.Label(header, text='Best Brains Schedule Builder', font="-size 28 -weight bold")
    title.pack(pady=(10, 0))

    ttk.Separator(header).pack(fill=X, padx=30)

    bodyframe = ttk.Frame(master)
    bodyframe.pack(fill=BOTH, pady=(0, 20), side=TOP, expand=True)

    lframe = ttk.Labelframe(bodyframe, text='Schedules', padding=18)
    lframe.pack(side=LEFT, fill=Y, expand=False, padx=30, pady=10)

    sched = ttk.Treeview(lframe, height=40, show='tree', selectmode='browse', takefocus=False)
    sched.bind('<<TreeviewSelect>>', Populate_Schedule)

    for location in CHEATSHEET:
        sched.insert('', 'end', location, text=location, open=True)
        for day in CHEATSHEET[location]:
            sched.insert(location, 'end', f"{day}/{location}", text=day, open=True)
            teachers = CHEATSHEET[location][day].keys()
            teachers = reversed(teachers)
            for teacher in teachers:
                sched.insert(f"{day}/{location}", 'end', f"{teacher}/{day}/{location}", text=teacher, open=True)

    sched.pack(side=LEFT, anchor=NE, fill=BOTH)

    sched_scroll = ttk.Scrollbar(lframe, orient='vertical', command=sched.yview)
    sched_scroll.pack(side=LEFT, fill=Y)
    sched.configure(yscrollcommand=sched_scroll.set)

    rframe = ttk.Frame(bodyframe)
    rframe.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 30), pady=10)

    actions = ttk.Labelframe(rframe, text='Actions')
    actions.pack(side=TOP, fill=X)

    button_width = 40

    advance_all = ttk.Button(actions, text='Advance All', takefocus=False, width=button_width)
    advance_all.grid(row=0, column=0, padx=10, pady=10)

    advance_selected = ttk.Button(actions, text='Advance Selected', takefocus=False, width=button_width)
    advance_selected.grid(row=0, column=1, padx=10, pady=10)

    refresh_cheatsheet = ttk.Button(actions, text='Refresh Cheatsheet', takefocus=False, width=button_width)
    refresh_cheatsheet.grid(row=0, column=2, padx=10, pady=10)

    actions.columnconfigure(0, weight=1)
    actions.columnconfigure(1, weight=1)
    actions.columnconfigure(2, weight=1)

    canvas_label = ttk.Labelframe(rframe, text='Students')
    canvas_label.pack(side=TOP, fill=BOTH, expand=True)

    schedule_frame = ScrolledFrame(canvas_label)
    schedule_frame.pack(side=TOP, expand=True, fill=BOTH, padx=10, pady=10, anchor=CENTER)

    instructions = ttk.Label(schedule_frame,
                             text='Select a location, day, or teacher from the panel to the left.',
                             style='instructions.TLabel')
    instructions.place(relx=0.5, rely=0.5, anchor=CENTER)

    finalize_frame = ttk.Labelframe(rframe, text='Finalize')
    finalize_frame.pack(side=BOTTOM, fill=X)

    preview_schedule = ttk.Button(finalize_frame, text='Preview Schedule', width=button_width, takefocus=False)
    preview_schedule.grid(row=0, column=0, padx=10, pady=10)

    export = ttk.Button(finalize_frame, text='Export as PDF', width=button_width, takefocus=False)
    export.grid(row=0, column=1, padx=10, pady=10)

    send = ttk.Button(finalize_frame, text='Send', width=button_width, takefocus=False)
    send.grid(row=0, column=2, padx=10, pady=10)

    finalize_frame.columnconfigure(0, weight=1)
    finalize_frame.columnconfigure(1, weight=1)
    finalize_frame.columnconfigure(2, weight=1)

    return root

if __name__ == '__main__':
    app = ttk.Window('BB Schedule Manager')
    app.state('zoomed')

    bagel = Main(app)
    bagel.pack(fill=BOTH, expand=YES)

    app.mainloop()
