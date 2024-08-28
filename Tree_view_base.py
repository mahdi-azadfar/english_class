import tkinter
from tkinter import ttk
from GUI_base import NewWindow
from models import Student


class Tree_view():
    
    def __init__(self, key, titles, c_width, page=None):
        self.key = key
        self.make_tree(titles, c_width, page)
        self.page = page



    def make_tree(self, titles, c_width, page):
        self.tree = ttk.Treeview(page, columns=titles, show='headings', height=4)
        # define headings
        for column in titles:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=c_width[titles.index(column)], anchor=tkinter.N)
        self.tree.pack(anchor='center',side='left', fill='both', expand=True)

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(page, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(anchor='center',side='left', fill='y')

    def start(self, data):
        for child in self.tree.get_children():
            print(child)
            self.tree.delete(child)
        # add data to the treeview
        if self.key == 'Session':
            for contact in data:
                self.tree.insert(index=['end'], values=contact, parent='')

        elif self.key == 'Class':
            counter = 1
            for contact in self.data:
                data_list = []
                data_list.append(contact)
                data_list.append('')
                for student_id in self.data[contact]["students"]:
                    if data_list[1] != '':
                        data_list[1] += ' & '
                    data_list[1] += Student.search_student(student_id=student_id, key='full_name')
                data_list.append('')
                for session in self.data[contact]["times"]:
                    if data_list[2] != '':
                        data_list[2] += ' & '
                    data_list[2] += session[0] + ': ' + session[1]+' - '+session[2]
                data_list.append(data[contact]['level'])
                data_list.append(data[contact]['salary'])
                self.tree.insert(index=counter, values=data_list, parent='')
                self.tree.rowconfigure(index=counter,minsize=100)
                counter+=1

        elif self.key == 'Student':
            if data:
                for id in data:
                    data_list = []
                    data_list.append(id)
                    full_name = Student.search_student(student_id=id, key='full_name')
                    data_list.append(full_name)
                    self.tree.insert(index=['end'], values=data_list, parent='')

    def add_record(self , record):
        self.tree.insert(index=['end'], values=record, parent='')

    def remove_from_tree(self, event):
        selected_item = self.tree.selection()
        def remove_this():
            self.tree.delete(selected_item)
            box.destroy()
        item = self.tree.item(selected_item)
        messege = f'Do you want to delete this {self.key}?'
        box = NewWindow(master=self.page, title='Remover',q_box=messege)
        
        

        yes_btn = tkinter.Button(master=box, text='Yes', command=remove_this).pack(side='left',fill='x', expand=True)
        No_btn = tkinter.Button(master=box, text='No', command=box.destroy).pack(side='right',fill='x', expand=True)
    
    def values_list(self):
            final_list = []
            for index_num in self.tree.get_children():
                item = self.tree.item(index_num)

                if self.key == 'Student':
                    final_list.append(item['values'][0])
                elif self.key=='Class':
                    pass
                elif self.key=='Session':
                    final_list.append(item['values'])
            return final_list
