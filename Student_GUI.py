from PIL import Image,ImageTk
import tkinter
from tkinter import ttk
from models import Base, Student
from GUI_base import NewWindow
from Tree_view_base import Tree_view
STUDENT_TITLES = ['ID','Full Name']
STUDENT_WEITH = [70,350]

class StudentGUI(NewWindow):
    def __init__(self,master, key, edited_id=None, ):
        self.edited_id = edited_id
        self.value = None
        self.key = key
        class_list_image = Image.open('./assets/class_list.jpg')
        add_student_image1 = Image.open('./assets/new_student_main1.jpg')
        add_student_image2 = Image.open('./assets/new_student_main2.jpg')   
        loading_image = Image.open('./assets/loading.png')
        correct_image = Image.open('./assets/correct.png')
        wrong_image = Image.open('./assets/wrong.png')
        self.tk_image1 = ImageTk.PhotoImage(add_student_image1)
        self.tk_image2 = ImageTk.PhotoImage(add_student_image2)
        self.tk_loading = ImageTk.PhotoImage(loading_image)
        self.tk_correct = ImageTk.PhotoImage(correct_image)
        self.tk_wrong = ImageTk.PhotoImage(wrong_image)
        self.tk_class_list = ImageTk.PhotoImage(class_list_image)

        save = Image.open('./assets/save.png')
        self.tk_save = ImageTk.PhotoImage(save)

        add = Image.open('./assets/add.png')
        self.tk_add = ImageTk.PhotoImage(add)

        active = Image.open('./assets/active.png')
        self.tk_active = ImageTk.PhotoImage(active)

        all = Image.open('./assets/all.png')
        self.tk_all = ImageTk.PhotoImage(all)
        
        new = Image.open('./assets/new.png')
        self.tk_new = ImageTk.PhotoImage(new)

        self.render_page(master)
        self.start()

    def render_page(self, master):
        if self.key == 'full_list':
           
            super().__init__(master=master, title='Students List')
            def info_manager(event):
                selected_item = self.student_tree_view.tree.selection()
                item = self.student_tree_view.tree.item(selected_item)
                record = item['values']
                show_student_info(master=self, id=str(record[0]), option=True)
            def filter_actives():
                self.student_tree_view.start(Student.active_students_list())
            def no_filter():
                self.student_tree_view.start(Base.students_list)

            data_label_frame = tkinter.LabelFrame(self)
            data_label_frame.pack(side='left', fill='both', expand=True)
            tree_label_frame = tkinter.LabelFrame(master=data_label_frame)
            image_label = tkinter.Label(master=self, image=self.tk_class_list, height=600, width=300)
            command_label_frame = tkinter.LabelFrame(master=data_label_frame)
            active_btn = tkinter.Button(master=command_label_frame, text='Active Students',command=filter_actives
                                        , image=self.tk_active, compound='left').pack(side='left', fill='x', padx=15, expand=True)
            all_btn = tkinter.Button(master=command_label_frame, text='All Students', command=no_filter
                                     , image=self.tk_all, compound='left').pack(side='left',fill='x', padx=15, expand=True)
            self.student_tree_view = Tree_view('Student', STUDENT_TITLES, STUDENT_WEITH, tree_label_frame)
            self.student_tree_view.tree.bind('<<TreeviewSelect>>', func=info_manager)
            tree_label_frame.pack(fill='both', expand=True)
            image_label.pack(fill='both',side='left')
            command_label_frame.pack(side='bottom', fill='x')
            self.student_tree_view.start(Base.students_list)
        elif self.key == 'creat_page':

            if self.edited_id:
                title = 'Edit Student'
            else:
                title = 'New Student'

            super().__init__(master=master, title=title)


            self.grid_anchor('center')
            def save_student():
                collected_data = {
                'First Name': self.first_name_entry.get(),
                "Last Name": self.last_name_entry.get(),
                "Age": self.age_entry.get(),
                'E-mail': self.email_entry.get(),
                'Phone Number': self.phone_number_entry.get(),
                'Type': self.type_cmb.get(),
                'Parent Phone Number': self.parent_phone_number_entry.get()
                }
                for data in collected_data:
                    if collected_data[data] == '':
                        error = NewWindow(master=self, title='Error',
                            error='Please fill all fields\nIf you want it to be empty, use * sign'
                        )
                        self.wait_window(error)
                        self.lift()
                        return False
                if self.edited_id:
                    Student.edit_student(id=self.edited_id, data=collected_data )
                    info = NewWindow(master=self,
                            title='Student Edited!',
                            info_message='Student Edited succesfully in database!'
                        )
                    self.wait_window(info)
                    self.destroy()

                else:
                    new_student = Student(collected_data)
                    if new_student.status:
                        info = NewWindow(master=self,
                            title='Student Saved!',
                            info_message='Student added succesfully to database!'
                        )
                        self.wait_window(info)
                        self.value = Base.last_ids['student']
                        self.destroy()
                    else:
                        error = NewWindow(
                            title='Duplicated data!',
                            error= f'You already have a student with this exact same information!\nstudent ID : {new_student.id}'
                        )
                        self.wait_window(error)
                        self.lift()
                    
            info_label_frame = tkinter.LabelFrame(master=self,text='')

            first_name_label = tkinter.Label(info_label_frame, text='First Name:'
                                             ,font=('Montserrat Alternates Medium',10))
            first_name_label.grid(column=0, row=0, pady=20, padx=15)
            self.first_name_entry = tkinter.Entry(info_label_frame, width=28)
            self.first_name_entry.grid(column=1, row=0, pady=20, padx=15)

            last_name_label = tkinter.Label(info_label_frame, text='Last Name:'
                                            ,font=('Montserrat Alternates Medium',10))
            last_name_label.grid(column=0, row=1, pady=20, padx=15)
            self.last_name_entry = tkinter.Entry(info_label_frame, width=28)
            self.last_name_entry.grid(column=1, row=1, pady=20, padx=15)

            email_label = tkinter.Label(info_label_frame, text='Email:'
                                        ,font=('Montserrat Alternates Medium',10))
            email_label.grid(column=0, row=2, pady=20, padx=15)
            self.email_entry = tkinter.Entry(info_label_frame, width=28)
            self.email_entry.grid(column=1, row=2, pady=20, padx=15)

            age_label = tkinter.Label(info_label_frame, text='Age:'
                                      ,font=('Montserrat Alternates Medium',10))
            age_label.grid(column=0, row=3, pady=20, padx=15)
            self.age_entry = tkinter.Entry(info_label_frame, width=28)
            self.age_entry.grid(column=1, row=3, pady=20, padx=15)

            phone_number_label = tkinter.Label(info_label_frame, text='Phone Number:'
                                               ,font=('Montserrat Alternates Medium',10))
            phone_number_label.grid(column=0, row=4, pady=20, padx=15)
            self.phone_number_entry = tkinter.Entry(info_label_frame, width=28)
            self.phone_number_entry.grid(column=1, row=4, pady=20, padx=15)

            type_label = tkinter.Label(info_label_frame, text='Student Type:'
                                       ,font=('Montserrat Alternates Medium',10))
            type_label.grid(column=0, row=5, pady=20, padx=15)
            self.type_cmb = ttk.Combobox(master=info_label_frame, values=['Adult', 'Child'])
            self.type_cmb.grid(column=1, row=5, pady=20, padx=15)

            parent_phone_number_label = tkinter.Label(info_label_frame, text='Parent Phone Number:'
                                                      ,font=('Montserrat Alternates Medium',10))
            parent_phone_number_label.grid(column=0, row=6, pady=20, padx=15)
            self.parent_phone_number_entry = tkinter.Entry(info_label_frame, width=28)
            self.parent_phone_number_entry.grid(column=1, row=6, pady=20, padx=15)


            save_btn = tkinter.Button(info_label_frame, text="SAVE", command=save_student,anchor='center', width=150
                                      , image=self.tk_save, compound='left')
            save_btn.grid(column=0, row=7 , pady=30,padx=15 ,sticky='W')
            cancel_btn = tkinter.Button(info_label_frame, text="CANCEL", command=self.destroy, width=150
                                        , image=self.tk_wrong, compound='left')
            cancel_btn.grid(column=1, row=7, pady=30,padx=15, sticky='E')
            info_label_frame.anchor('center')
            student_image1 = tkinter.Label(master=self, image=self.tk_image1).pack(side='right',fill='both')
            info_label_frame.pack(side='right',fill='both', expand=True)
            student_image2 = tkinter.Label(master=self, image=self.tk_image2).pack(side='right',fill='both')
        elif self.key == 'select_student':
            super().__init__(master=master, title='Add Student To Class', pop_up=True)
            self.student_id = None
            def add_student_btn():
                self.value = self.student_id
                self.destroy()
            
            def action_box_render():
                children_list = action_label_frame.winfo_children()
                if children_list:
                    for child in children_list:
                        child.destroy()

                if var.get() == 1:
                    add_btn.configure(state='disabled')
                    def search():
                        adding_data = {
                        "First Name" : first_name_entry.get(),
                        "Last Name" : last_name_entry.get()
                        }
                        if len(adding_data["First Name"]) and len(adding_data["Last Name"]):
                            result=Student.search_student(full_name=adding_data)
                            if result:
                                status_label.configure(image=self.tk_correct, text='Student Found')
                                self.student_id = result
                                add_btn.configure(state='active')
                            else:
                                status_label.configure(image=self.tk_wrong, text='Student Not Found')
                        else:
                            status_label.configure(image=self.tk_wrong, text='Incomplete Information')

                    first_name_label = ttk.Label(action_label_frame, text="First Name:"
                                                 ,font=('Montserrat Alternates Medium',12))
                    first_name_entry = ttk.Entry(action_label_frame)
                    first_name_label.pack(side='top', pady=5)
                    first_name_entry.pack(side='top', pady=10)
                    
                    last_name_label = ttk.Label(action_label_frame, text="Last Name:"
                                                ,font=('Montserrat Alternates Medium',12))
                    last_name_entry = ttk.Entry(action_label_frame)
                    last_name_label.pack(side='top', pady=5)
                    last_name_entry.pack(side='top', pady=10)

                    status_label = tkinter.Label(master=action_label_frame, text='', image=None, compound='left',
                                                 font=('Montserrat Alternates Medium',12))
                    status_label.pack( )

                    find_btn = tkinter.Button(master=action_label_frame, text="Find", command=search
                                              ,image=self.tk_loading, compound='left')
                    find_btn.pack(side='bottom', pady=10)

                elif var.get() == 3:
                    add_btn.configure(state='disabled')
                    def get_from_list(event):
                        add_btn.configure(state='active')
                        selected_item = student_tree_view.tree.selection()
                        item = student_tree_view.tree.item(selected_item)
                        self.student_id = item['values'][0]

                    student_tree_view = Tree_view('Student', STUDENT_TITLES, STUDENT_WEITH, action_label_frame)
                    student_tree_view.start(Base.students_list)
                    student_tree_view.tree.bind('<<TreeviewSelect>>', func=get_from_list)
                elif var.get() == 2:
                    add_btn.configure(state='disabled')
                    def new_student():
                        new_student = StudentGUI(master=self, key='creat_page')
                        self.wait_window(new_student)
                        self.student_id = new_student.value
                        if self.student_id is not None:
                            add_student_btn()
                            

                    move_btn = tkinter.Button(master=action_label_frame, text="Move to new student form", command=new_student
                                              , image=self.tk_new, compound='left')
                    move_btn.pack(fill='y', anchor='center', pady=50)
                 
            methhod_label_frame = tkinter.LabelFrame(master=self, text='Method : ')
            methhod_label_frame.pack(fill='both')
            var = tkinter.IntVar()
            method1 = tkinter.Radiobutton(master=methhod_label_frame, text='Add By Name', variable=var, value=1,
                                          selectcolor='green',indicatoron=False, command=action_box_render)
            method2 = tkinter.Radiobutton(master=methhod_label_frame, text='Add New', variable=var, value=2,
                                          selectcolor='green',indicatoron=False, command=action_box_render)
            method3 = tkinter.Radiobutton(master=methhod_label_frame, text='Add From List', variable=var, value=3,
                                          selectcolor='green',indicatoron=False, command=action_box_render)
            method1.pack(side='left', fill='both', expand=True)
            method2.pack(side='left', fill='both', expand=True)
            method3.pack(side='left', fill='both', expand=True)

            action_label_frame = tkinter.LabelFrame(master=self,text='Actioin Box : ')
            action_label_frame.pack(fill='both', expand=True)
            command_label_frame= tkinter.LabelFrame(master=self)
            add_btn = tkinter.Button(command_label_frame, command=add_student_btn, text='Add', state='disabled'
                                     , image=self.tk_add, compound='left')
            cancel_btn = tkinter.Button(command_label_frame, command=self.destroy, text='Cancel'
                                        , image=self.tk_wrong, compound='left')
            add_btn.pack(side='left', fill= 'both', expand=True)
            cancel_btn.pack(side='left', fill= 'both', expand=True)
            command_label_frame.pack(fill='x')
        elif self.key == 'find_student':
            super().__init__(master=master, title='Find Student', pop_up=True)
            self.find_student(find_page=self)

    def start (self):
        if self.edited_id:
            self.edited_data = Base.students_list[self.edited_id]
            self.first_name_entry.insert(0,self.edited_data["First Name"])
            self.last_name_entry.insert(0,self.edited_data["Last Name"])
            self.age_entry.insert(0, self.edited_data["Age"])
            self.email_entry.insert(0, self.edited_data["E-mail"])
            self.phone_number_entry.insert(0, self.edited_data['Phone Number'])
            if self.edited_data["type"] == 'Adult':
                self.type_cmb.current(0)
            else:
                self.type_cmb.current(1)
        if self.key == 'full_list':
            print('f start')
            self.student_tree_view.start(Base.students_list)

    def find_student(self, find_page):
        def search():
            adding_data = {
            "First Name" : first_name_entry.get(),
            "Last Name" : last_name_entry.get()
            }
            if len(adding_data["First Name"]) and len(adding_data["Last Name"]):
                result=Student.search_student(full_name=adding_data)
                if result:
                    page = show_student_info(master=self, id=result, option=True)
                    self.wait_window(page)
                    self.destroy()
                else:
                    status_label.configure(image=self.tk_wrong, text='Student Not Found')
            else:
                status_label.configure(image=self.tk_wrong, text='Incomplete Information')

        first_name_label = tkinter.Label(find_page, text="First Name:", font=('Montserrat Alternates Medium',12))
        first_name_entry = tkinter.Entry(find_page )
        first_name_label.pack(side='top', pady=5, fill='y', expand= True)
        first_name_entry.pack(side='top', pady=10, fill='y', expand= True)
        
        last_name_label = tkinter.Label(find_page, text="Last Name:", font=('Montserrat Alternates Medium',12))
        last_name_entry = tkinter.Entry(find_page)
        last_name_label.pack(side='top', pady=5, fill='y', expand= True)
        last_name_entry.pack(side='top', pady=10, fill='y', expand= True)

        status_label = tkinter.Label(master=find_page, text='', image=None, compound='left', font=('Montserrat Alternates Medium',12))
        status_label.pack( )

        find_btn = tkinter.Button(master=find_page, text="Find", command=search,
                                  image=self.tk_loading, compound='left')
        find_btn.pack(side='bottom', pady=10, fill='y', padx=15)

class show_student_info(NewWindow):
    def __init__(self,master, id, option=False):
        self.id = id
        self.option = option
        super().__init__(master=master, title='Student Info')
        edit = Image.open('./assets/edit.png')
        self.tk_edit = ImageTk.PhotoImage(edit)

        delete = Image.open('./assets/delete.png')
        self.tk_delete = ImageTk.PhotoImage(delete)

        self.render_page()
        self.start()
        
    def render_page(self):
        def delete_student():
            def remove_this():
                Student.delete_student(self.id)
                box.destroy()
                self.destroy()
            box = NewWindow(master=self, title='Remover', q_box='Do you want to delete this student?')
            self.wait_window(box)
            if box.ok:
                remove_this()
        def edit_student():
            edit = StudentGUI(master=self, edited_id=self.id, key='creat_page')
            self.wait_window(edit)
        def add_student():
            self.destroy()
        self.personal_frame = tkinter.LabelFrame(master=self, height=200, width=300)
        self.personal_frame.pack(side='left',fill='both', expand=True, padx=5)
        personal_label = tkinter.Label(master=self.personal_frame, text="Personal Information", background='black',
                                          foreground='white', font=('coolvetica rg', 14),height=2)
        personal_label.pack(side='top', fill='both')
        self.financial_frame = tkinter.LabelFrame(master=self, height=200, width=300)
        self.financial_frame.pack(side='left',fill='both', expand=True, padx=5)
        financial_label = tkinter.Label(master=self.financial_frame, text="Financial Information", background='black',
                                          foreground='white', font=('coolvetica rg', 14),height=2)
        financial_label.pack(side='top', fill='both')
        self.command_frame = tkinter.LabelFrame(master=self, width=10)
        self.command_frame.pack(side='left',fill='y', padx=5)
        command_label = tkinter.Label(master=self.command_frame, text="commands", background='black',
                                          foreground='white', font=('coolvetica rg', 14),height=2)
        command_label.pack(side='top', fill='both')
        if self.option:
            edit_btn = tkinter.Button(master=self.command_frame, text='Edit',command=edit_student
                                      , image=self.tk_edit, compound='left')
            edit_btn. pack(side='top', fill='both', padx=5, pady=15, expand=True)
            delete_btn = tkinter.Button(master=self.command_frame, text='Delete', command=delete_student
                                        , image=self.tk_delete, compound='left')
            delete_btn. pack(side='top', fill='both', padx=5, pady=15, expand=True)
            warning_btn = tkinter.Button(master=self.command_frame, text='Send Warning', command=None, state='disabled')
            warning_btn. pack(side='top', fill='both', padx=5, pady=15, expand=True)
            
            payment_btn = tkinter.Button(master=self.command_frame, text='Send Payment Gate', command=None, state='disabled')
            payment_btn. pack(side='top', fill='both', padx=5, pady=15, expand=True)
            laws_btn = tkinter.Button(master=self.command_frame, text='Inform Laws', command=None, state='disabled')
            laws_btn. pack(side='top', fill='both', padx=5, pady=15, expand=True)
            canceling_btn = tkinter.Button(master=self.command_frame, text='Inform Canseling', command=None, state='disabled')
            canceling_btn. pack(side='top', fill='both', padx=5, pady=15, expand=True)
        data = Student.search_student(student_id=self.id)
        counter = 0
        name_labels = {}
        self.info_labels = {}
        page = self.personal_frame

        for info in data :
            if counter>4:
                page= self.financial_frame
            name_labels[info] = tkinter.Label(master=page, text=info+' :', font=('coolvetica rg', 14), background='seagreen1'
                                       ,anchor='center', relief='groove').pack(fill='both', expand=True)
            self.info_labels[info] = tkinter.Label(master=page, text='', font=('Montserrat Alternates Medium',12))
            self.info_labels[info].pack(fill='both', expand=True)
            counter += 1 

    def start(self):
        data = Student.search_student(student_id=self.id)
        counter = 0
        for info in data :
            if counter>4:
                page= self.financial_frame
            self.info_labels[info].configure(text = data[info])
            counter += 1 
