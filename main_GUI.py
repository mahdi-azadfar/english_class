from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText
import tkinter
from tkinter import Menu, ttk
from persiantools.jdatetime import JalaliDate
from Class_GUI import ClassGUI
from models import Base, EnClass, Student
from Monthly_Status import monthlyStatus, Outlook
from GUI_base import NewWindow
from Student_GUI import StudentGUI

DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
temp_extra_session = []


class MainPage(tkinter.Tk):
    def __init__(self):

        self.times_label = {}
        self.lines = {}
        self.days_label = {}
        self.days_class_label = {}
        self.dict_of_class_labels_in_tabel = {}
        super().__init__()
        self.render_page(title='Main Page', window_height=600, window_width=1100)
        if Base.last_ids['month'] == Base.today.month:
            self.normal_run()
        else:
            self.new_month_gui()

    def normal_run(self):
        main_page_image = Image.open('./assets/Teacher.png')
        tk_image = ImageTk.PhotoImage(main_page_image)
        image_label = tkinter.Label(master=self, image=tk_image, height=480, width=200)
        image_label.place(x=900, y=0)
        self.table_structure()
        self.start()
        self.mainloop()

    def new_month_gui(self):
        def new_month_protocol():
            image_label.destroy()
            ok_btn.destroy()
            info_label.destroy()
            Base.new_month()
            if Base.new_month != '':
                ClassGUI.remake_last_month_classes(master=self)
            else:
                Base.last_ids['month'] = Base.today.month
                Base.finishing_up()
            self.normal_run()

        main_page_image = Image.open('./assets/new_month.jpg')
        tk_image = ImageTk.PhotoImage(main_page_image)
        image_label = tkinter.Label(master=self, image=tk_image)
        image_label.pack(fill='x')
        if Base.semester_name == '':
            message = "Welcome To EnglishClass\nHope You enjoy this application"
        else:
            message = f'WELL DONE!\nYou completed {Base.semester_name} semester\n' \
                      f'Your entire data move to records and your workspace is clean'
        info_label = tkinter.Label(self, text=message, font=('Caviar Dreams', 24))
        ok_btn = tkinter.Button(self, text='Start New Month', command=new_month_protocol)
        info_label.pack(fill='y', expand=True)
        ok_btn.pack(pady=10)
        self.mainloop()

    def render_page(self, title, window_width, window_height):

        self.title(title)
        self.resizable(False, False)
        self.configure(height=window_height, width=window_width)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def table_structure(self):
        # making times of day labels

        for time in range(8, 24):
            x_fixed = ((time - 8) * 50) + 101
            self.lines[time] = ttk.Separator(master=self, orient='vertical').place(x=x_fixed, y=0, height=600)
            self.times_label[time] = ttk.Label(self, text=str(time), font=('Montserrat Alternates Medium', 10)
                                               ).place(x=x_fixed - 5, y=0, height=60, width=50)

        # making days name labels

        counter = 0
        for day in DAYS:
            counter += 75
            self.days_label[day] = ttk.Label(master=self, text=day, justify='center', anchor='center',
                                             font=('Montserrat Alternates Medium', 10)
                                             ).place(x=5, y=counter, height=75, width=90)
            self.lines[day] = ttk.Separator(master=self, orient='horizontal').place(x=0, y=counter, width=900)
        # create a menubar
        menubar = Menu(self)
        self.config(menu=menubar)

        # create a menu
        student_menu = Menu(menubar, tearoff=False)
        class_menu = Menu(menubar, tearoff=False)
        data_menu = Menu(menubar, tearoff=False)
        month_menu = Menu(menubar, tearoff=False)

        # add a menu item to the menu
        student_menu.add_command(
            label='Add Student',
            command=lambda: StudentGUI(master=self, key='creat_page')
        )

        class_menu.add_command(
            label='Add Class',
            command=lambda: ClassGUI(master_page=self, key='new')
        )

        student_menu.add_command(
            label='Students list',
            command=lambda: StudentGUI(master=self, key='full_list')
        )

        student_menu.add_command(
            label='Find Students',
            command=lambda: StudentGUI(master=self, key='find_student')
        )

        month_menu.add_command(
            label='Monthly schedule',
            command=lambda: monthlyStatus(master_page=self)
        )

        month_menu.add_command(
            label='Month Outlook',
            command=lambda: Outlook(self)
        )

        data_menu.add_command(
            label='Backup Data',
            command=self.backup_gui
        )

        data_menu.add_command(
            label='Load Data',
            command=self.load_data_gui
        )
        # add the add_menu to the menubar
        menubar.add_cascade(
            label="Student",
            menu=student_menu
        )

        menubar.add_cascade(
            label="Class",
            menu=class_menu
        )

        menubar.add_cascade(
            label="Month",
            menu=month_menu
        )

        menubar.add_cascade(
            label="Data",
            menu=data_menu
        )
        seperator = ttk.Separator(self, orient='vertical').place(x=899, y=0, height=600)

    def backup_gui(self):
        Base.back_up()
        NewWindow(self, info_message='Backup created!')

    def load_data_gui(self):
        def load():
            if backup_name.get() != '':
                Base.load_back_up(backup_name=backup_name.get())

        load_page = NewWindow(self, pop_up=True)
        backup_name = ttk.Combobox(load_page, values=Base.load_back_up())
        info_label = tkinter.Label(
            load_page, text='Choose your backup :\n(names are combination of date an time of backup)')
        info_label.pack(fill='x', expand=True)
        backup_name.pack(expand=True)
        btn = tkinter.Button(load_page, text='Load Backup', command=load).pack(expand=True)

    def session_in_table_label(self, day, start, end, class_id, extra=False):
        class_color = Base.classes_list[class_id]['color']
        if self.dict_of_class_labels_in_tabel.get(class_id):
            pass
        else:
            self.dict_of_class_labels_in_tabel[class_id] = []

        start = start.replace(' : ', '')
        end = end.replace(' : ', '')

        # defining the x and y for labels

        start = int(start)
        end = int(end)
        y_for_class = 75 + (75 * DAYS.index(day))
        x_for_class = 100 + (start - 800) / 2
        width_for_class = (end - start) / 2
        if extra is not False:
            class_name = f'Extra class {class_id}'
        else:
            class_name = f'class {class_id}'
        temp_label = ttk.Label(self, text=class_name,
                               relief='raised', anchor='center', background=class_color,
                               font=('Montserrat Alternates Medium', 10))
        temp_label.place(x=x_for_class, y=y_for_class, height=75, width=width_for_class)
        temp_label.bind(sequence='<Button>', func=lambda x: ClassInfo(class_id=class_id, master_page=self, extra=extra))
        self.dict_of_class_labels_in_tabel[class_id].append(temp_label)

    def start(self):
        if self.dict_of_class_labels_in_tabel != {}:
            for class_labels in self.dict_of_class_labels_in_tabel.values():
                for label in class_labels:
                    label.destroy()
            self.dict_of_class_labels_in_table = {}

        for each_class in Base.classes_list:
            sessions = Base.classes_list[each_class]['times']
            for session in sessions:
                self.session_in_table_label(day=session[0], start=session[1], end=session[2], class_id=each_class)
        today = JalaliDate.today()

        for extra in Base.extra_list:
            for data in Base.extra_list[extra]:
                compare_date = data['date']
                compare_date = compare_date.split('-')
                compare_date = JalaliDate(int(compare_date[0]), int(compare_date[1]), int(compare_date[2]))
                if compare_date >= today:
                    self.session_in_table_label(
                        day=data['day'],
                        start=data['start'],
                        end=data['end'],
                        class_id=extra,
                        extra=data
                    )


class ClassInfo(NewWindow):
    def __init__(self, class_id, master_page, extra=None):
        self.general_info = None
        self.extra = extra
        edit = Image.open('./assets/edit.png')
        self.tk_edit = ImageTk.PhotoImage(edit)

        delete = Image.open('./assets/delete.png')
        self.tk_delete = ImageTk.PhotoImage(delete)

        extra = Image.open('./assets/extra.png')
        self.tk_extra = ImageTk.PhotoImage(extra)

        note = Image.open('./assets/note.png')
        self.tk_note = ImageTk.PhotoImage(note)

        self.class_id = class_id
        self.master_page = master_page
        super().__init__(master=self.master_page, title='Extra class info', pop_up=True)

        self.render_page()
        self.start()

    def render_page(self):
        if self.extra is not None:
            self.title = 'Extra class info'
            self.pop_up = True
            class_color = Base.classes_list[self.class_id]['color']
            title = f"Extra Class For Class {self.class_id}"
            general_info_label = tkinter.Label(master=self, text=title,
                                               background='black', foreground='white', font=('coolvetica rg', 14))
            general_info_label.pack(anchor='nw', fill='x')
            for part in self.extra:
                name_label = tkinter.Label(self, text=part, anchor='center'
                                           , relief='groove', font=('coolvetica rg', 12), background=class_color)
                name_label.pack(fill='both', expand=True)
                info_label = tkinter.Label(self, text=self.extra[part], anchor='center', relief='groove',
                                           font=('Montserrat Alternates Medium', 12))
                info_label.pack(fill='both', expand=True)

            delete_btn = ttk.Button(self, text='Delete', image=self.tk_delete, compound='left'
                                    ).pack(anchor='center', fill='x', padx=5, pady=10)
        else:
            self.title = 'Class Info'
            self.general_info.pack(side='left', fill='both', expand=True, padx=5)
            general_info_label = tkinter.Label(master=self.general_info, text=" General Information",
                                               background='black',
                                               foreground='white', font=('coolvetica rg', 14)).pack(anchor='nw',
                                                                                                    fill='x')
            self.students_in_class_label = ttk.Label(
                self.general_info, text='Students In Class:', anchor='center', relief='groove',
                font=('coolvetica rg', 12))
            self.students_in_class_label.pack(fill='both', expand=True)
            self.students_label = tkinter.Label(master=self.general_info, font=('Montserrat Alternates Medium', 12))
            self.students_label.pack(fill='both', expand=True)
            self.sessions_label = ttk.Label(
                self.general_info, text='Sessions:', relief='groove'
                , anchor='center', justify='center', font=('coolvetica rg', 12))
            self.sessions_label.pack(fill='both', expand=True)
            self.sessions_info_label = tkinter.Label(master=self.general_info,
                                                     font=('Montserrat Alternates Medium', 12))
            self.sessions_info_label.pack(fill='both', expand=True)
            self.other_info_label = ttk.Label(self.general_info, text='Other Information:'
                                              , relief='groove', anchor='center', justify='center',
                                              font=('coolvetica rg', 12))
            self.other_info_label.pack(fill='both', expand=True)
            self.salary_label = ttk.Label(self.general_info, text="", anchor='center', justify='center',
                                          font=('Montserrat Alternates Medium', 12))
            self.salary_label.pack(fill='both', expand=True)
            self.level_label = ttk.Label(self.general_info, text="", anchor='center', justify='center',
                                         font=('Montserrat Alternates Medium', 12))
            self.level_label.pack(fill='both', expand=True)
            self.start_label = ttk.Label(self.general_info, text='', anchor='center', justify='center',
                                         font=('Montserrat Alternates Medium', 12))
            self.start_label.pack(fill='both', expand=True)

            self.status = ttk.Frame(master=self, relief='ridge', border=10)
            self.status.pack(side='left', fill='both', expand=True, padx=5)
            status_info_label = tkinter.Label(self.status, text='Class Status', background='black',
                                              foreground='white', font=('coolvetica rg', 14)).pack(anchor='nw',
                                                                                                   fill='x')
            self.notes = ttk.Frame(master=self, relief='ridge', border=10)
            self.notes.pack(side='left', fill='both', expand=True, padx=5)
            notes_info_label = tkinter.Label(self.notes, text='Notes on Class', background='black',
                                             foreground='white', font=('coolvetica rg', 14)).pack(anchor='nw', fill='x')
            todo_label = ttk.Label(master=self.notes, text='TODO:', font=('coolvetica rg', 12)).pack(anchor='w')
            self.todo_text = ScrolledText(master=self.notes, height=10, width=23, font=('Chocolate Donuts', 12))
            self.todo_text.pack(padx=5, pady=10, fill='both')
            summary_label = ttk.Label(master=self.notes, text='Summary:', font=('coolvetica rg', 12)).pack(anchor='w')
            self.summary_text = ScrolledText(master=self.notes, height=10, width=23, font=('Chocolate Donuts', 12))
            self.summary_text.pack(padx=5, pady=10, fill='both')

            def add_notes():
                EnClass.add_notes(class_id=self.class_id, summary=self.summary_text.get("1.0", tkinter.END),
                                  todo=self.todo_text.get("1.0", tkinter.END))
                info = NewWindow(master=self, title='Note added', info_message='Your note added successfully!')
                self.wait_window(info)
                self.lift()

            add_notes_btn = ttk.Button(master=self.notes, text='Add notes', image=self.tk_note, compound='left',
                                       command=add_notes).pack(side='bottom', fill='x', anchor='s', padx=5, pady=10,
                                                               expand=True)
            self.cancel_student_label = tkinter.Label(master=self.status, text='Canceled by student', relief='groove'
                                                      , anchor='center', font=('coolvetica rg', 12))
            self.cancel_student_label.pack(fill='both', expand=True)
            self.cancel_student_info = tkinter.Label(master=self.status, text='0', anchor='center',
                                                     font=('Montserrat Alternates Medium', 12))
            self.cancel_student_info.pack(fill='both', expand=True)
            self.cancel_teacher_label = tkinter.Label(master=self.status, text='Canceled by teacher', anchor='center',
                                                      relief='groove', font=('coolvetica rg', 12))
            self.cancel_teacher_label.pack(fill='both', expand=True)
            self.cancel_teacher_info = tkinter.Label(master=self.status, text='0', anchor='center',
                                                     font=('Montserrat Alternates Medium', 12))
            self.cancel_teacher_info.pack(fill='both', expand=True)
            self.delay_times_label = tkinter.Label(master=self.status, text='Remaining times:', anchor='center',
                                                   relief='groove', font=('coolvetica rg', 12))
            self.delay_times_label.pack(fill='both', expand=True)
            self.delay_times_info = tkinter.Label(master=self.status, text='0', anchor='center',
                                                  font=('Montserrat Alternates Medium', 12))
            self.delay_times_info.pack(fill='both', expand=True)
            self.extras_label = tkinter.Label(master=self.status, text='Extra Classes:', anchor='center',
                                              relief='groove', font=('coolvetica rg', 12))
            self.extras_label.pack(fill='both', expand=True)
            self.extras_info = tkinter.Label(master=self.status, text='0', anchor='center',
                                             font=('Montserrat Alternates Medium', 12))
            self.extras_info.pack(fill='both', expand=True)
            edit_btn = ttk.Button(self.general_info, text='Edit', command=lambda: ClassGUI(
                master_page=self, key='new', edited_class_id=self.class_id
            ), image=self.tk_edit, compound='left'
                                  ).pack(side='left', anchor='center', fill='x', padx=5, pady=10, expand=True)
            extra_btn = ttk.Button(self.status, text='Add extra class', command=lambda: ClassGUI(
                master_page=self, key='extra', extra_class_id=self.class_id), image=self.tk_extra, compound='left'
                                   ).pack(side='left', anchor='center', fill='x', padx=5, pady=10, expand=True)

            def delete_class():
                question = NewWindow(self, q_box='Are You sure want to delete this class?')
                self.wait_window(question)
                if question.ok:
                    EnClass.finishing_class(class_id=self.class_id)
                    self.destroy()
                    self.master_page.start()

            delete_btn = ttk.Button(self.general_info, text='Delete', command=delete_class, image=self.tk_delete,
                                    compound='left'
                                    ).pack(anchor='center', side='left', fill='x', padx=5, pady=10, expand=True)

    def start(self):
        if self.extra:
            pass
        else:
            class_color = Base.classes_list[self.class_id]['color']
            class_info = Base.classes_list[self.class_id]
            notes_info = EnClass.read_notes(class_id=self.class_id)
            self.todo_text.insert(tkinter.INSERT, notes_info[0])
            self.summary_text.insert(tkinter.INSERT, notes_info[1])
            canceling_list = Base.canceling_list
            cancel_teacher = '0'
            cancel_student = '0'
            delay_times = 0
            extras = str(class_info['extra']) + ' sessions'
            if canceling_list.get(self.class_id):
                cancel_teacher = str(len(canceling_list[self.class_id]['canceled_by_teacher'])) + ' sessions'
                cancel_student = str(len(canceling_list[self.class_id]['canceled_by_student'])) + ' sessions'

                for time in canceling_list[self.class_id]['remaining_time']:
                    delay_times += int(time[1])
                delay_times = str(delay_times)

            self.cancel_student_info.configure(text=cancel_student)
            self.cancel_teacher_info.configure(text=cancel_teacher)
            self.delay_times_info.configure(text=delay_times)
            self.extras_info.configure(text=extras)
            student_name = ''
            for student_id in class_info['students']:
                if student_name != '':
                    student_name += '\n'
                student_name += Student.search_student(student_id=student_id, key='full_name')
            self.students_label.configure(text=student_name, anchor='center', justify='center')
            message = ''

            for session in class_info['times']:
                if message != '':
                    message += '\n'

                message += session[0] + ' : '
                message += session[1]
                message += ' - '
                message += session[2]
            self.sessions_info_label.configure(text=message, anchor='center', justify='center')
            self.cancel_student_label.configure(background=class_color)
            self.cancel_teacher_label.configure(background=class_color)
            self.delay_times_label.configure(background=class_color)
            self.sessions_label.configure(background=class_color)
            self.extras_label.configure(background=class_color)
            self.students_in_class_label.configure(background=class_color)
            self.other_info_label.configure(background=class_color)
            self.salary_label.configure(text=f"salary : {class_info['salary']}")
            self.level_label.configure(text=f"Level / Book : {class_info['level']}")
            self.start_label.configure(text=f"Start Date : {class_info['start_date']}")


if __name__ == "__main__":
    Base.start()
    MainPage()
