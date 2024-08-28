from PIL import Image,ImageTk
import tkinter
from tkinter import ttk
from models import Base, EnClass
from GUI_base import NewWindow
SESSION_TITLES = ['Day', 'Start Time', 'End Time']
SESSION_WEITH = [150, 100, 100]
DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

class Session(NewWindow):
    def __init__(self, master, key='window', data=None):
        self.master = master
        self.key = key

        save = Image.open('./assets/save.png')
        self.tk_save = ImageTk.PhotoImage(save)

        time = Image.open('./assets/time.png')
        self.tk_time = ImageTk.PhotoImage(time)
        
        wrong_image = Image.open('./assets/wrong.png')
        self.tk_wrong = ImageTk.PhotoImage(wrong_image)

        if key == 'no_window':
            self.data = data
            self.check_sessions()
        elif key == 'window':
            super().__init__(master=self.master, title='Add Session', pop_up=True)
            self.render_page()
    
    def render_page(self):
        def info_collector():
            
            self.day=day_cmb.get()
            inputed_time = {}
            inputed_time[0] = start_time_h_entry.get()
            inputed_time[1] = start_time_m_entry.get()
            inputed_time[2] = end_time_h_entry.get()
            inputed_time[3] = end_time_m_entry.get()
                        
            for each_input in inputed_time:
                if inputed_time[each_input] is False:
                    error = NewWindow(master=self, title='error', error='Please fill the time boxes')
                    self.wait_window(error)
                    self.lift()
                    return False
                
                if inputed_time[each_input].isdigit() is False:
                    error = NewWindow(master=self,title='error', error='Please fill the time boxes with only digits')
                    self.wait_window(error)
                    self.lift()
                    return False

                #adding zero to first of singel digit inputs and checking for wrong data
                    
                if len(inputed_time[each_input]) == 1:
                    inputed_time[each_input] = '0' + inputed_time[each_input]
            
            self.start = inputed_time[0] + inputed_time[1]
            self.end = inputed_time[2] + inputed_time[3]
            
            self.str_start = inputed_time[0] +' : '+ inputed_time[1]
            self.str_end = inputed_time[2] +' : '+ inputed_time[3]
            self.check_sessions()
            if self.status[0]:
                
                last_class_time = str(self.status[1])
                if last_class_time == '0':
                    last_class.config(text= 'No eralier class')
                    last_class_time = ''
                else:
                    last_class_time = last_class_time[0] + last_class_time[1] + ' : ' + last_class_time[2] + last_class_time[3]
                next_class_time = str(self.status[2])
                if next_class_time == '2400':
                    next_class_time = ''
                    next_class.config(text='No further class')
                else:
                    next_class_time = next_class_time[0] + next_class_time[1] + ' : ' + next_class_time[2] + next_class_time[3]

                last_class_info.config(text=last_class_time)
                next_class_info.config(text=next_class_time)

                def save_data():
                    self.destroy()
                    self.master.lift()
                save_btn.config(command=save_data)
                save_btn.configure(state='active')
            else:
                info = NewWindow(master=self,info_message=f'{self.status[2]} class : {self.status[1]}')
                self.wait_window(info)
                self.lift()
        def show_times_avilable(event):
            day = day_cmb.get()
            for i in range(8,24):
                hour_label[i].configure(background='lightgreen')

            for hour in Base.schedule[day]:
                times = hour.split('-')
                times[0]= int(times[0])
                times[0] = times[0]/100
                times[1]= int(times[1])
                times[1] = times[1]/100
                counter = 8
                while counter < 24:
                    print(counter)
                    if counter<=times[0]<counter+1 and times[1]>=counter+1:
                        if times[0] == counter:
                            color = 'red'
                        else:
                            color = 'yellow'
                        compare_time = int(times[0])
                        str_time = str(times[0])
                        str_time = str_time.replace('.',':')
                        if len(str_time)<=4 and str_time[-2]==':':
                            str_time+='0'
                        hour_label[compare_time].configure(background=color)
                        compare_time += 1 
                        while compare_time < times[1]:
                            hour_label[compare_time].configure(background='red')
                            compare_time += 1

                        if compare_time-1<times[1]<compare_time:
                            str_time = str(times[1])
                            str_time = str_time.replace('.',':')
                            if len(str_time)<=4 and str_time[-2]==':':
                                str_time+='0'
                            print(compare_time , times)
                            hour_label[compare_time-1].configure(background='yellow')
                        counter = compare_time
                    counter += 1


        input_label_frame = tkinter.LabelFrame(master=self, width=250)
        input_label_frame.anchor('center')
        day_label = ttk.Label(input_label_frame, text='Day:', font=('Montserrat Alternates Medium',10))
        day_label.grid(row=1, column=1,columnspan=2, pady=5)
        day_cmb = ttk.Combobox(master=input_label_frame, values=DAYS)
        day_cmb.grid(row=2,columnspan=2, column=1, pady=5)
        day_cmb.bind('<<ComboboxSelected>>', show_times_avilable)

        start_time_label = ttk.Label(input_label_frame, text='Start Time:', font=('Montserrat Alternates Medium',10))
        start_time_label.grid(row=3, columnspan=2, column=1, pady=5)
        start_time_h_entry = ttk.Entry(input_label_frame, width=5)
        start_time_h_entry.grid(row=4, column=1, pady=5, sticky='e', padx=5)
        start_time_m_entry = ttk.Entry(input_label_frame, width=5)
        start_time_m_entry.grid(row=4, column=2, pady=5, sticky='w', padx=5)
        
        end_time_label = ttk.Label(input_label_frame, text='End Time:', font=('Montserrat Alternates Medium',10))
        end_time_label.grid(row=5, columnspan=2, column=1, pady=5)
        end_time_h_entry = ttk.Entry(input_label_frame, width=5)        
        end_time_h_entry.grid(row=6, column=1, pady=5, sticky='e', padx=5)
        end_time_m_entry = ttk.Entry(input_label_frame, width=5)
        end_time_m_entry.grid(row=6, column=2, pady=5, sticky='w', padx=5)
    
        last_class = ttk.Label(master=input_label_frame, text='Last class ends at:', font=('Montserrat Alternates Medium',10))
        last_class_info = ttk.Label(master=input_label_frame, font=('Montserrat Alternates Medium',10))
        next_class = ttk.Label(master=input_label_frame, text='Next class starts at :', font=('Montserrat Alternates Medium',10))
        next_class_info = ttk.Label(master=input_label_frame, font=('Montserrat Alternates Medium',10))
        last_class.grid(row=7, column=1, pady=5, sticky='w', padx=5)
        last_class_info.grid(row=7, column=2, pady=5, sticky='w', padx=5)
        next_class.grid(row=8, column=1, pady=5, sticky='w', padx=5)
        next_class_info.grid(row=8, column=2, pady=5, sticky='w', padx=5)
    
        check_btn = tkinter.Button(input_label_frame, command=info_collector, text='Check', image=self.tk_time, compound='left', width=100)
        cancel_btn = tkinter.Button(input_label_frame, command=self.destroy, text='cancel', image=self.tk_wrong, compound='left', width=100)
        save_btn = tkinter.Button(master=input_label_frame, text="Save", state='disabled', image=self.tk_save, compound='left', width=100)
        check_btn.grid(row=9, column=1, columnspan=2, pady=5, padx=5)
        cancel_btn.grid(row=10, column=2, pady=5, sticky='e')
        save_btn.grid(row=10 , column=1 , pady=5, sticky='w')
    
        input_label_frame.pack(side='left', fill='both', expand=True)
        times_avilable_label_frame = tkinter.LabelFrame(self)
        times_avilable_label_frame.pack(side='left',fill='both', expand=True)

        hour_label= {}
        for i in range(8,24):
            hour_label[i] = tkinter.Label(times_avilable_label_frame,anchor='center', text=f'{i}', font=('Montserrat Alternates Medium',8))
            hour_label[i].pack(fill='both', expand=True)

    def value(self):
        if self.status:
            return [self.day , self.str_start , self.str_end]

    def check_sessions(self):
        if self.key == 'window':
            #checking if this time is avalibale or not
            status = EnClass.is_this_time_free(day=self.day, start_time=self.start, end_time=self.end)
            self.status = status

        elif self.key == 'no_window':
            self.status = True
            self.day = self.data[0]
            self.str_start = self.data[1]
            self.str_end = self.data[2]

    def start(self):
        pass