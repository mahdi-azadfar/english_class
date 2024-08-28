from PIL import Image,ImageTk
import json
from tkinter import PhotoImage, ttk
import tkinter
from GUI_base import NewWindow
from persiantools.jdatetime import *
from models import Base, EnClass, Student
DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
MONTHS = ["Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad", "Shahrivar", "Mehr", "Aban", "Azar", "Dey","Bahman","Esfand",]

class monthlyStatus(NewWindow):
    def __init__(self, master_page):
        super().__init__(master=master_page, title='Monthly Status')
        self.data = Base.classes_list
        self.today = JalaliDate.today()
        self.day = self.today.day
        self.month = self.today.month
        self.year = self.today.year
        self.dates_dict = EnClass.all_classes_date_creator()
        self.green = PhotoImage(file='./assets/green.png')            
        self.blue = PhotoImage(file='./assets/blue.png')            
        self.red = PhotoImage(file='./assets/red.png')            
        self.orange = PhotoImage(file='./assets/orange.png')            
        self.image_address = None
        self.render_page()
    
    def session_status_changer(self, class_id, date):
        
        def active_delay():
            delay_entery.configure(state='normal')
            save_btn.configure(state='active')
            delay_entery.focus()
        def deactive_delay():
            delay_entery.configure(state='disabled')
            save_btn.configure(state='active')
        def save_status():
            key = value.get()
            def save_and_ext():
                with open('Data/canceling_list.json', 'w') as fi:
                    fi.write(json.dumps(self.canceling_list))
                Base.add_canceling_data_to_classes()
                session_status_changer_page.destroy()
                index = self.dates_dict[class_id].index(date)
                if key=='complete':
                    color='lightgreen'
                    image = self.green
                elif key == 'canceled_by_teacher':
                    color='indianred'
                    image = self.red
                elif key == 'canceled_by_student':
                    color='lightblue'
                    image = self.blue
                elif key == 'remaining_time':
                    color='sandybrown'
                    image = self.orange
                else:

                    color = 'white'
                    image = ''
                self.dict_of_labels[class_id][index].configure(background=color, image=image)
                return
            def index_found(index=None, state_value=None):
                if index is not None:
                    self.canceling_list[class_id][state_value].pop(index)

                if key == 'complete' or key == 'clear':    
                    save_and_ext()
                            
                elif key == 'remaining_time':
                    delay_entery.get()
                    self.canceling_list[class_id][key].append([date, delay_entery.get()])
                    save_and_ext()

                else:
                    self.canceling_list[class_id][key].append(date)
                    save_and_ext()
            
                
            if self.canceling_list.get(class_id) is None:
                self.canceling_list[class_id] = {
                    'canceled_by_student': [],
                    'canceled_by_teacher': [],
                    'remaining_time': []
                }
            index = None
            for state in self.canceling_list[class_id]:
                for state_date in self.canceling_list[class_id][state]:
                    if date == state_date:
                        index = self.canceling_list[class_id][state].index(state_date)
                        index_found(index= index , state_value=state)
                    if state == 'remaining_time':
                        if date == state_date[0]:
                            index = self.canceling_list[class_id][state].index(state_date)
                            index_found(index= index , state_value=state)
            if index is None : 
                index_found()
            
        session_status_changer_page = NewWindow(master=self,title='Status', pop_up=True)
        info_label = tkinter.Label(master=session_status_changer_page, text=f'class : {class_id} \n Date : {date} {MONTHS[self.month]}',
                                   background='black', foreground='white', font=('Montserrat Alternates Medium',12))
        info_label.pack(fill='both', expand=True)
        value = tkinter.StringVar(master=session_status_changer_page)
        cancel1 = tkinter.Radiobutton(master=session_status_changer_page, text='Canceled by teacher',variable=value,
                                  value='canceled_by_teacher',justify='center',command=deactive_delay,
                                    indicatoron=False,selectcolor='red')
        cancel2 = tkinter.Radiobutton(master=session_status_changer_page, text='Canceled by student',variable=value
                                  , value='canceled_by_student',justify='center',command=deactive_delay,
                                    indicatoron=False,selectcolor='lightblue')
        cancel3 = tkinter.Radiobutton(master=session_status_changer_page, text='Remaining time',variable=value
                                  , value='remaining_time', indicatoron=False,command=active_delay,
                                  selectcolor='orange')
        delay_entery = tkinter.Entry(master=session_status_changer_page, justify='center', state='disabled')
        completed = tkinter.Radiobutton(master=session_status_changer_page, text='Completed', value='complete'
                                        ,variable=value, indicatoron=False,command=deactive_delay, selectcolor='green')
        clear = tkinter.Radiobutton(master=session_status_changer_page, text='No Status', value='clear'
                                        ,variable=value, indicatoron=False,command=deactive_delay, selectcolor='white')
        cancel1.pack(fill='both', expand=True)
        cancel2.pack(fill='both', expand=True)
        cancel3.pack(fill='both', expand=True)
        delay_entery.pack(fill='both', expand=True, padx=15, pady=15)
        completed.pack(fill='both', expand=True)
        clear.pack(fill='both', expand=True)
        if date > self.day:
            completed.configure(state = 'disabled')
        else:
            clear.configure(state='disabled')
        save_btn = tkinter.Button(master=session_status_changer_page, text='Save', command=save_status, state='disabled')
        save_btn.pack(fill='y', padx=15, pady=15)

    def render_page(self):
        self.canceling_list = Base.canceling_list
        self.notebook = ttk.Notebook(master=self)
        self.pages = {}
        image = Image.open('./assets/students.jpg')
        self.image = ImageTk.PhotoImage(image)
        self.dict_of_label_frames = {}
        self.dict_of_labels = {}

        #function fo creating clickable labels(dates)
        
        def creat_labels(date,class_id):
            date_label = tkinter.Label(master=dates_label_frame, text=date,background=color, image=self.image_address,
                                       width=2,compound='center',justify='left', anchor='center', relief='solid',
                                         font=('Montserrat Alternates Medium',10))
            date_label.pack(side='left', fill='both', padx=1, anchor='center',expand=True)
            date_label.bind(sequence='<Button>', func=lambda x:self.session_status_changer(class_id,date))
            self.dict_of_labels[class_id].append(date_label)
        counter = 0
        page_number=0
        for each_class in self.data:                
            days_have_class = ''
            self.dict_of_labels[each_class] = []            
            if counter == 5:
                page_number +=1
                counter=0
            if self.pages.get(page_number) is None:
                self.pages[page_number] = ttk.Frame(master=self.notebook, height=100, width=100)
                self.notebook.add(self.pages[page_number], text=f' Records : {(page_number*5)+1} - {(page_number+1)*5} ')
                self.notebook.pack(expand=True, fill='both')
                self.month_label = tkinter.Label(master=self.pages[page_number], text=f'<<{MONTHS[self.month-1]} Semester>>',background='peachpuff').pack(fill='both', expand=True)
                self.image_label= tkinter.Label(master=self.pages[page_number], image=self.image, 
                                                            height=200, width=1100)
                self.image_label.pack(fill='both',side='bottom',anchor='s')
            for time in self.data[each_class]['times']:
                if days_have_class != '':
                    days_have_class += '\n'
                days_have_class += time[0]
            title = EnClass.search_class(class_id=each_class, key='students_names')
            dates_label_frame = ttk.LabelFrame(master=self.pages[page_number],text=f'class {each_class}', height=50)
            self.dict_of_label_frames[each_class] = dates_label_frame
            class_label = ttk.Label(master=dates_label_frame, text=title, relief='raised',font=('Montserrat Alternates Medium',10),
                                    anchor='center',background=self.data[each_class]['color'],width=25
                                    ).pack(side='left', fill='y',anchor='center',padx=5, ipadx=10)
            def color_manager(date):
                if self.canceling_list.get(each_class):
                    for canceled in self.canceling_list[each_class]['canceled_by_teacher']:
                        if date == canceled:
                            self.image_address = self.red
                            return 'indianred'
                    for canceled in self.canceling_list[each_class]['canceled_by_student']:
                        if date == canceled:
                            self.image_address = self.blue
                            return 'lightblue'
                    for canceled in self.canceling_list[each_class]['remaining_time']:
                        if date == canceled[0]:
                            self.image_address = self.orange
                            return 'sandybrown'
                if self.day < int(date):
                    self.image_address = None
                    return 'white'
                else:
                    self.image_address = self.green
                    return 'lightgreen'
            for date in self.dates_dict[each_class]:
                color = color_manager(date)
                creat_labels(date=date, class_id=each_class)
            dates_label_frame.pack(fill='both', padx=2,side='top', expand=True)
            days_label = ttk.Label(master=dates_label_frame, text=days_have_class,anchor='center', justify='center'
                                ,relief='raised',background='black', foreground='white',width=20, font=('Montserrat Alternates Medium',10)
                                ).pack(side='left',fill='both')
            count = str(len(self.dates_dict[each_class])) + ' sessions'
            count_label = ttk.Label(master=dates_label_frame, text=count,anchor='center', justify='center',
                                font=('Montserrat Alternates Medium',10),relief='raised',background='black', foreground='white',width=20
                                ).pack(side='left',fill='both')
            
            counter += 1
        #decorate last page 
        if self.data != {}:
            for number in range(0, 5-(len(self.data)%5)):
                temp_label_frame = ttk.LabelFrame(master=self.pages[page_number],
                                            height=50).pack(fill='both', expand=True,side='top')
        else:
            temp_label = tkinter.Label(self , text='You have no class',font=('Montserrat Alternates Medium',12), 
                                        anchor='center').pack(fill='both',expand=True, anchor='center')
    
    def start(self):
        pass

class Outlook(NewWindow):
    def __init__(self, master, title='Month Outlook'):
        super().__init__(master, title,pop_up=True)
        self.render_page()
    def render_page(self):
        students = Student.active_students_list()
        title_label = tkinter.Label(master=self, text=f'{Base.semester_name} Semester',background='peachpuff',
                                             font=('Montserrat Alternates Medium',12)).pack(fill='x', side='top')
        students_count_label = tkinter.Label(master=self, text=f'Active Students  :  {len(students)}',
                                             font=('Montserrat Alternates Medium',12))
        students_count_label.pack(fill='x', expand=True)
        classes_count = Base.last_ids['class']
        classes_count_label = tkinter.Label(master=self, text=f'This Month Class  :  {classes_count}',
                                            font=('Montserrat Alternates Medium',12)).pack(fill='x', expand=True)
        all_dates = EnClass.all_classes_date_creator()
        sessions_count=0
        income =0
        sessions_in_week = 0
        for each_class in all_dates:
            sessions_in_week += len(Base.classes_list[each_class]['times'])
            class_sessions_count = len(all_dates[each_class])
            sessions_count += class_sessions_count
            class_income = class_sessions_count * int(Base.classes_list[each_class]['salary'])
            income += class_income
        income_expected_label = tkinter.Label(master=self, text=f'Income Expected  :  {income}',
                                              font=('Montserrat Alternates Medium',12))
        income_expected_label.pack(fill='x', expand=True)
        session_Count_label = tkinter.Label(master=self, text=f'This Month Sessions  :  {sessions_count}',
                                            font=('Montserrat Alternates Medium',12))
        session_Count_label.pack(fill='x', expand=True)
        sessions_in_week_label = tkinter.Label(master=self, text=f'Sessions In Week  :  {sessions_in_week}',
                                             font=('Montserrat Alternates Medium',12)).pack(fill='x', expand=True)

        def start(self):
            pass