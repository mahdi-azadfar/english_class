from PIL import Image,ImageTk
import tkinter
from tkinter import ttk
from persiantools.jdatetime import JalaliDate
from models import Base, EnClass, ExtraClass, Student
from GUI_base import NewWindow
from Tree_view_base import Tree_view
from Session_GUI import Session
from Student_GUI import StudentGUI
STUDENT_TITLES = ['ID','Full Name']
STUDENT_WEITH = [70,350]
SESSION_TITLES = ['Day', 'Start Time', 'End Time']
SESSION_WEITH = [150, 100, 100]
DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

class ClassGUI(NewWindow):
    def __init__(self, master_page,key, edited_class_id = None, extra_class_id=None
                 , window_title="Add Class"):
        self.master_page = master_page
        self.extra_class_id = extra_class_id
        self.first_time = True
        self.key = key
        add_class_image = Image.open('./assets/new_class.jpg')
        self.image_tk = ImageTk.PhotoImage(add_class_image)
        
        wrong_image = Image.open('./assets/wrong.png')
        self.tk_wrong = ImageTk.PhotoImage(wrong_image)

        save = Image.open('./assets/save.png')
        self.tk_save = ImageTk.PhotoImage(save)

        add = Image.open('./assets/add.png')
        self.tk_add = ImageTk.PhotoImage(add)

        schedule = Image.open('./assets/schedule.png')
        self.tk_schedule = ImageTk.PhotoImage(schedule)

        extra = Image.open('./assets/extra.png')
        self.tk_extra = ImageTk.PhotoImage(extra)

        self.edited_class_id=edited_class_id
        self.render_page()
        
    
    def add_student_in_class(self):
        student = StudentGUI(master=self, key='select_student')
        self.wait_window(student)
        if self.students_in_class.count(student.value) == 0 and student.value is not None:
            full_name = Student.search_student(student_id=student.value, key='full_name')
            self.students_report.add_record(record=[student.value ,full_name])
            self.students_in_class = self.students_report.values_list()                        
     
    def render_page(self):
        
        def remove_from_tree(event=None,tree= None):
            selected_item = tree.tree.selection()
            def remove_this():
                tree.tree.delete(selected_item)
                box.destroy()
            item = tree.tree.item(selected_item)
            message = f'Do you want to delete this {tree.key}?'
            box = NewWindow(master=self, title='Remover',q_box=message)        
            yes_btn = tkinter.Button(master=box, text='Yes', command=remove_this).pack(side='left',fill='x', expand=True)
            No_btn = tkinter.Button(master=box, text='No', command=box.destroy).pack(side='right',fill='x', expand=True)
    
        if self.key == 'new':
            super().__init__(master=self.master_page, title='New Class')
            self.main_frame = tkinter.Frame(master=self, padx=1)
            self.main_frame.pack(fill='both', expand=True , side='top', ipadx=5, ipady=5)
            self.frame_one = tkinter.Frame(master=self.main_frame, padx=1)
            self.frame_one.pack(fill='both', expand=True , side='left', ipadx=5, ipady=5)
            self.frame_two = tkinter.Frame(master=self.main_frame, padx=1)
            self.frame_two.pack(fill='both', expand=True , side='left', ipadx=5, ipady=5)
            self.pic_frame = tkinter.Frame(master=self, width=600, background='white')
            self.pic_frame.pack( fill='both', side='top')
            image_label = ttk.Label(master=self.pic_frame, image=self.image_tk).pack(fill='both')
                        
            self.student_label_frame = ttk.LabelFrame(self.frame_one, text='Students in class:', height=150)
            self.student_label_frame.pack( fill='both', pady=2,expand=True,padx=5)            
            def final_check():
                times = self.sessions_report.values_list()
                
                year = self.year_entry.get()
                year = str(year)
                month = self.month_entry.get()
                month = str(month)
                day = self.day_entry.get()
                day = str(day)
                start_date = year + '-' + month + '-' + day
                if self.edited_class_id is None:
                    for i in range(len(self.students_in_class)):
                        self.students_in_class[i] = str(self.students_in_class[i])
                        
                    new_class = EnClass(
                        students = self.students_in_class,
                        times = times,
                        level= self.level_entry.get(),
                        salary= self.salary_entry.get(),
                        start_date= start_date,
                        color=self.color_cmb.get()

                    )
                    info = NewWindow(master=self, title='class added', info_message=' your class added')
                    self.wait_window(info)
                    self.destroy()
                else:
                    EnClass.edit_class_data(
                        class_id=self.edited_class_id,
                        students = self.students_in_class,
                        times = times,
                        level= self.level_entry.get(),
                        salary= self.salary_entry.get(),
                        start_date= start_date,
                        color=self.color_cmb.get()
                        )
                    info = NewWindow(master=self, title='Edit complete', info_message='Your class edited succesfully')
                    self.destroy()
            self.students_report = Tree_view('Student', ['ID' , 'Full name'] , STUDENT_WEITH, self.student_label_frame)
            self.students_report.tree.bind('<<TreeviewSelect>>', func= lambda x:remove_from_tree(tree=self.students_report))
            add_student_btn = ttk.Button(self.frame_one, text='Add Student', image=self.tk_add, compound='left',
                                        command=self.add_student_in_class)
            add_student_btn.pack(anchor='center', padx=10, ipadx=5,pady=5)

            self.sessions_label_frame = ttk.LabelFrame(self.frame_one, text='Sessions:', height=150)
            self.sessions_label_frame.pack( fill='both', pady=2,expand=True,padx=5)
            self.sessions_report = Tree_view('Session',SESSION_TITLES ,SESSION_WEITH, self.sessions_label_frame)
            self.sessions_report.tree.bind('<<TreeviewSelect>>', func= lambda x:remove_from_tree(tree=self.sessions_report))

            def sessioner():
                added_session = Session(master=self, key='window')
                added_session.wait_window()
                self.sessions_report.add_record(record=added_session.value())
            add_session_btn = ttk.Button(self.frame_one, text='Add Session',
                                        command=sessioner, image=self.tk_schedule, compound='left')
            add_session_btn.pack(anchor='s', padx=10, ipadx=5,pady=5)


            self.color_tag_label_frame = ttk.LabelFrame(master=self.frame_two , text = 'Color Tag', height=75)
            self.color_cmb = ttk.Combobox(master=self.color_tag_label_frame, values=Base.COLORS, justify='center')
            self.color_cmb.pack(side='left', fill='x',expand=True,padx=10)
            self.color_test = ttk.Label(master=self.color_tag_label_frame, width=15, relief='raised')
            self.color_test.pack(side='left', fill='x',expand=True,padx=10)
            def change_color(event):
                self.color_test.config(background=self.color_cmb.get())
            self.color_cmb.bind('<<ComboboxSelected>>',change_color)
            self.color_tag_label_frame.pack(pady=2, fill='both',padx=5, expand=True)

            level_label_frame = ttk.LabelFrame(self.frame_two, text='Level and salary:', height=75)
            level_label_frame.pack(ipadx=20, fill='both', pady=2, ipady=10,padx=5, expand=True)
            level_label_frame.anchor('center')
            self.level_entry = ttk.Entry(master=level_label_frame)
            level_label = ttk.Label(master=level_label_frame, text='Level / Book:')
            level_label.grid(row=1,column=1, padx=10)
            self.level_entry.grid(row=1, column=2, padx=10)
            salary_label = ttk.Label(master=level_label_frame, text='salary:')
            self.salary_entry= ttk.Entry(master=level_label_frame)
            salary_label.grid(row=1,column=3, padx=10)
            self.salary_entry.grid(row=1,column=4, padx=10)

            class_start_date = ttk.Labelframe(self.frame_two, text='Class Start Date:', height=75)
            class_start_date.pack(ipadx=20, fill='both', pady=2, ipady=10,padx=5, expand=True)
            class_start_date.anchor('center')
            year_label = ttk.Label(class_start_date, text='Year').grid(row=1, column=1)
            self.year_entry = ttk.Entry(class_start_date,width=10)
            self.year_entry.grid(row=1, column=2)
            month_label = ttk.Label(class_start_date, text='Month').grid(row=1, column=3)
            self.month_entry = tkinter.Entry(class_start_date,width=10)
            self.month_entry.grid(row=1, column=4)
            day_label = ttk.Label(class_start_date, text='Day').grid(row=1, column=5)
            self.day_entry = ttk.Entry(class_start_date,width=10)
            self.day_entry.grid(row=1, column=6)
            today_label = ttk.Label(class_start_date, text=f' Today  :  {JalaliDate.today()} ').grid(row=1, column=7)
            

            commands_label_frame = ttk.LabelFrame(master=self.frame_two, text='commands:', height=75)
            commands_label_frame.pack(ipadx=20, fill='both',padx=5)
            save_btn = ttk.Button(commands_label_frame, text='Save',
                                        command=final_check, image=self.tk_save, compound='left')
            save_btn.pack(side='left', padx=10, ipadx=5,pady=5, expand=True)
            cancel_btn = ttk.Button(commands_label_frame, text='Cancel',
                                        command=self.destroy, image=self.tk_wrong, compound='left')
            cancel_btn.pack(side='left', padx=10, ipadx=5,pady=5, expand=True)
            
            if self.edited_class_id:
                self.edited_class = Base.classes_list[self.edited_class_id]
                self.students_in_class = self.edited_class['students']
                self.sessions = self.edited_class['times']
                self.salary=self.edited_class['salary']
                self.level=self.edited_class['level']
                self.start_date=self.edited_class['start_date']
                self.start_date=self.start_date.split('-')
                self.color = self.edited_class['color']
                Base.COLORS.append(self.edited_class['color'])
                self.color_index = Base.COLORS.index(self.color)
                
            else:
                self.students_in_class = []
                self.times = []
                self.sessions = []
                self.salary='0'
                self.level=''
                self.start_date=['0','0','0']
                self.color = Base.COLORS[0]
                self.color_index = 0
                            
            self.start()
    
        elif self.key == 'extra':
            super().__init__(master=self.master_page , title="Extra class", pop_up=True)
            def extra_Session_handler():
                self.extra_session = Session(master=self, key='window')
                self.extra_session.wait_window()
                self.extra_session = self.extra_session.value()
                extra_session_label.configure(text=f'{self.extra_session[0]} : {self.extra_session[1]} - {self.extra_session[2]}')
                dates = []
                today = JalaliDate.today()
                month = today.month
                first_Day_of_month = JalaliDate(year=today.year, month=today.month, day=1)
                if first_Day_of_month.weekday() <= DAYS.index(self.extra_session[0]):
                    date = DAYS.index(self.extra_session[0]) - first_Day_of_month.weekday() + 1
                else:
                    date = DAYS.index(self.extra_session[0]) - first_Day_of_month.weekday() + 8

                while date <= today.days_in_month(year=today.year, month=today.month):
                    date_str = first_Day_of_month = JalaliDate(year=today.year, month=today.month, day=date)
                    dates.append(date_str)
                    date += 7
                extra_session_date_cmb.configure(state='normal')
                extra_session_date_cmb.configure(value = dates)
            extra_session_btn = tkinter.Button(master=self,text='Add Session',command=extra_Session_handler
                                            , image=self.tk_extra, compound='left').pack(fill='both',expand=True, pady=5)
            extra_session_label = tkinter.Label(master=self, text='')
            extra_session_label.pack( fill='y',pady=5,expand=True)
            extra_session_date_label = tkinter.Label(master=self, text="Extra class date : "
                                                        ).pack(fill='both',expand=True, pady=5)
            extra_session_date_cmb = ttk.Combobox(master=self, values=[],state='disabled')

            extra_session_date_cmb.pack( fill='y',pady=5,expand=True)
            # TODO
            def save_Extra_class():
                ExtraClass(date=extra_session_date_cmb.get(),
                            day=self.extra_session[0],
                            start=self.extra_session[1],
                            end=self.extra_session[2],
                            class_id=self.extra_class_id
                            )
                self.destroy()                
            save_extra_class_btn = tkinter.Button(master=self, text='Save', state='active',command= save_Extra_class
                                                    , image=self.tk_save, compound='left').pack(fill='y',expand=True,pady=5)

    def start(self):

        # adding data to page
        if self.key == 'new':
            self.students_report.start(data=self.students_in_class)
            self.sessions_report.start(data=self.sessions)
            self.color_cmb.configure(values=Base.COLORS)
            self.color_cmb.current(self.color_index)
            self.color_test.configure(background=self.color)
            self.year_entry.delete(0, 'end')
            self.year_entry.insert(0, self.start_date[0])
            self.day_entry.delete(0, 'end')
            self.day_entry.insert(0, self.start_date[2])
            self.salary_entry.delete(0, 'end')
            self.salary_entry.insert(0,self.salary)
            self.level_entry.delete(0, 'end')
            self.level_entry.insert(0, self.level)
            self.month_entry.delete(0, 'end')
            self.month_entry.insert(0, self.start_date[1])
            # self.first_time = False

    @classmethod
    def remake_last_month_classes(cls, master):
        remake_page = NewWindow(master, 'Remake last month classes')
        data = Base.read_back_up()
        def remake_classes():
            for class_id in dict_of_checkboxes_var:
                if dict_of_checkboxes_var[class_id].get() == 1:
                    #TODO: check for interfrence
                    new_class = EnClass(
                        students = data[class_id]['students'],
                        times = data[class_id]['times'],
                        level= level_dict[class_id].get(),
                        salary= salary_dict[class_id].get(),
                        start_date= 'today',
                        color=Base.COLORS[0]
                        )
            Base.last_ids['month'] = Base.today.month
            Base.finishing_up()
            remake_page.destroy()
        if data is False:
            Base.last_ids['month'] = Base.today.month
            Base.finishing_up()
            remake_page.destroy()
        else:
            dict_of_checkboxes_var = {}
            dict_of_checkboxes = {}
            pages = {}
            notebook = ttk.Notebook(master=remake_page)
            pages = {}
            level_dict = {}
            salary_dict = {}
            counter = 0
            page_number=0
            for each_class in data:    
                dict_of_checkboxes_var[each_class] = tkinter.IntVar()            
                if counter == 8:
                    page_number +=1
                    counter=0
                if pages.get(page_number) is None:
                    pages[page_number] = tkinter.Frame(master=notebook, height=100, width=100)
                    notebook.add(pages[page_number], text=f' Records : {(page_number*6)+1} - {(page_number+1)*6} ')
                    notebook.pack(expand=True, fill='both')
                class_label_frame = tkinter.LabelFrame(master=pages[page_number],text=f'class {each_class}', height=50)
                title = ''
                sessions = ''
                for student in data[each_class]['students']:
                    title += Student.search_student(student_id=student, key='full_name') + '\n'
                for time in data[each_class]['times']:
                    sessions += time[0]+' : '+ time[1] +' - ' + time[2] +'\n'
                
                class_name_label = tkinter.Label(master=class_label_frame, text=title, relief='raised',
                                        anchor='center',background=data[each_class]['color'],width=25
                                        ).pack(side='left', fill='x',anchor='center',padx=5, ipadx=10, expand=True)
                sessions_label = tkinter.Label(master=class_label_frame, text=sessions
                                            ).pack(side='left', fill='x',anchor='center',padx=5, ipadx=10, expand=True)
                class_label_frame.pack(fill='both', padx=2,side='top', expand=True)
                
                level_dict[each_class] = ttk.Entry(master=class_label_frame)
                level_label = ttk.Label(master=class_label_frame, text='Level / Book:')
                level_label.pack(side='left', fill = 'x',anchor='center',padx=5, ipadx=10)
                level_dict[each_class].pack(side='left', fill = 'x',anchor='center',padx=5, ipadx=10)
                salary_label = ttk.Label(master=class_label_frame, text='salary:')
                salary_dict[each_class]= ttk.Entry(master=class_label_frame)
                salary_label.pack(side='left', fill = 'x',anchor='center',padx=5, ipadx=10)
                salary_dict[each_class].pack(side='left', fill = 'x',anchor='center',padx=5, ipadx=10)
                salary_dict[each_class].insert(0,data[each_class]['salary'])
                level_dict[each_class].insert(0, data[each_class]['level'])
                dict_of_checkboxes[each_class] = tkinter.Checkbutton(master=class_label_frame, background='red', onvalue=1, offvalue=0
                                            ,text='Remake', activebackground='yellow', indicatoron=False,selectcolor='lightgreen',
                                                variable=dict_of_checkboxes_var[each_class]).pack(side='left', fill='x',anchor='center',padx=5, ipadx=10)
                counter += 1
            #decorate last page 
            if data != {}:
                for number in range(0, 6-(len(data)%6)):
                    temp_label_frame = ttk.LabelFrame(master=pages[page_number],
                                                height=50).pack(fill='both', expand=True,side='top')
            else:
                temp_label = tkinter.Label(remake_page , text='You have no class',
                                            anchor='center').pack(fill='both',expand=True, anchor='center')
            add = Image.open('./assets/add.png')
            tk_add = ImageTk.PhotoImage(add)
            add_btn = tkinter.Button(master=remake_page, text='Add and Start', command=remake_classes
                                    , image=tk_add, compound='left')
            add_btn.pack()