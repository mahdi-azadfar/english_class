import tkinter as tk
from tkinter import ttk
import tkinter
from tkinter.messagebox import showinfo
from models import Base
from main_GUI import MainPage


def login_page():
    status = False
    # root window
    root = tk.Tk()
    root.geometry("300x200+500+200")
    root.resizable(False, False)
    root.title('Welcome')
    root.iconphoto(True, tkinter.PhotoImage(file='./assets/icon.png'))

    # store username address and password
    username = tk.StringVar()
    password = tk.StringVar()

    def login_clicked(event=None):
        """ callback when the login button clicked
        """
        if username_entry.get() == '1' and password_entry.get() == '1':

            root.destroy()
            Base.start()
            MainPage()
        else:
            showinfo(
                message='Wrong Username or Password!\nPlease try again'
            )

    # Sign in frame

    signin = ttk.Frame(root)
    signin.pack(padx=10, pady=10, fill='x', expand=True)

    # username
    username_label = ttk.Label(signin, text="Username:", font=('Montserrat Alternates Medium',12))
    username_label.pack(fill='x', expand=True ,side='top')

    username_entry = ttk.Entry(signin, textvariable=username)
    username_entry.pack(fill='x', expand=True ,side='top')
    username_entry.bind('<Return>', login_clicked)
    username_entry.focus()

    # password
    password_label = ttk.Label(signin, text="Password:", font=('Montserrat Alternates Medium',12))
    password_label.pack(fill='x', expand=True ,side='top')

    password_entry = ttk.Entry(signin, textvariable=password, show="*")
    password_entry.pack(fill='x', expand=True, side='top')
    password_entry.bind('<Return>', login_clicked)
    # login button
    login_button = ttk.Button(signin, text="Login", command=login_clicked)
    login_button.pack(fill='x', pady=10, side='bottom')
    root.mainloop()
    return True


if __name__ == "__main__":
    login_page()

