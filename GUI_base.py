import tkinter
from PIL import Image, ImageTk


class NewWindow(tkinter.Toplevel):

    def __init__(self, master, title='', pop_up=False, q_box=False, info_message=False, error=False):

        self.master = master
        if pop_up or q_box or info_message or error:
            self.single_window = False
        else:
            self.single_window = True
        if q_box or info_message or error:
            self.refresh = False
        else:
            self.refresh = True
        if q_box is not False:
            super().__init__(master=master)
            self.ok = False

            def ok_func():
                self.ok = True
                self.destroy()
            self.make_page(title, 300, 200)
            self.message = tkinter.Label(master=self, text=q_box, font=('Montserrat Alternates Medium', 10)
                                         , wraplength=250).pack(side='top', pady=10)
            self.q_img = Image.open('./assets/q_box.png')
            self.image = ImageTk.PhotoImage(self.q_img)
            pic = tkinter.Label(master=self, image=self.image).pack(side='top')
            yes_btn = tkinter.Button(self, text='Yes', command=ok_func).pack(
                side='left', fill='x', padx=25, expand=True)
            no_btn = tkinter.Button(self, text='No', command=self.destroy).pack(
                side='left', fill='x', padx=25, expand=True)

        elif pop_up is not False:
            super().__init__(master=master)
            window_width = 350
            window_height = 350
            self.protocol("WM_DELETE_WINDOW", self.destroy)
            self.make_page(title=title, window_height=window_height, window_width=window_width)

        elif info_message is not False or error is not False:
            super().__init__(master=master)
            window_width = 300
            window_height = 200
            self.make_page(title=title, window_height=window_height, window_width=window_width)
            if info_message is not False:
                message = info_message
                self.i_img = Image.open('./assets/info.png')
            else:
                message = error
                self.i_img = Image.open('./assets/stop.png')

            self.i_image = ImageTk.PhotoImage(self.i_img)
            message_label = tkinter.Label(master=self, text=message, font=('Montserrat Alternates Medium', 12)
                                          , wraplength=250).pack(fill='both', expand=True)
            pic = tkinter.Label(master=self, image=self.i_image).pack(fill='both', expand=True)
            ok = tkinter.Button(master=self, text='OK', command=self.destroy).pack(fill='x', padx=90, expand=True)
        else:
            super().__init__(master=master)
            window_width = 1100
            master.withdraw()
            window_height = 600
            self.protocol("WM_DELETE_WINDOW", self.destroy)
            self.make_page(title=title, window_height=window_height, window_width=window_width)

    def make_page(self, title, window_width, window_height):
        self.iconphoto(True, tkinter.PhotoImage(file='./assets/icon.png'))
        self.title(title)
        self.resizable(False, False)
        s_width = self.winfo_screenwidth()
        center_x = int(s_width / 2 - window_width / 2)
        s_height = self.winfo_screenheight()
        center_y = int(s_height / 2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def destroy(self):
        super().destroy()
        if self.single_window:
            self.master.deiconify()
            self.master.lift()
        if self.refresh:
            self.master.start() 
