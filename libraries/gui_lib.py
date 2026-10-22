# ==============================================================
# GUI library / Библиотека окна (tkinter)
# ==============================================================
import tkinter as _tk
from tkinter import messagebox as _mb, filedialog as _fd

def create(title='DoMtor App', width=600, height=400):
    win = _tk.Tk()
    win.title(title)
    win.geometry(f'{width}x{height}')
    return win

def label(parent, text, x=10, y=10, size=12):
    w = _tk.Label(parent, text=text, font=('Arial', size))
    w.place(x=x, y=y)
    return w

def button(parent, text, command, x=10, y=10, width=20):
    w = _tk.Button(parent, text=text, command=command, width=width)
    w.place(x=x, y=y)
    return w

def entry(parent, x=10, y=10, width=30):
    w = _tk.Entry(parent, width=width)
    w.place(x=x, y=y)
    return w

def text_area(parent, x=10, y=60, width=60, height=15):
    w = _tk.Text(parent, width=width, height=height)
    w.place(x=x, y=y)
    return w

def show(win):
    win.mainloop()

def info(title, text):
    _mb.showinfo(title, text)

def ask(title, text):
    return _mb.askyesno(title, text)

def warn(title, text):
    _mb.showwarning(title, text)

def open_file():
    return _fd.askopenfilename()

def save_file():
    return _fd.asksaveasfilename()

# Cyrillic aliases
создать        = create
метка          = label
кнопка         = button
поле           = entry
текст          = text_area
показать       = show
сообщить       = info
спросить       = ask
предупредить   = warn
открыть_файл   = open_file
сохранить_файл = save_file