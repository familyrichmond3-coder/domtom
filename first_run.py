# ==============================================================
# DoMtor first-run setup dialog.
# Shows a compact window on first launch:
# "Before you start programming, install the starter libraries."
# User ticks which libraries to enable.
# ==============================================================
import tkinter as tk
from tkinter import ttk
import domtor


def show(parent=None):
    """Show the setup dialog. Works standalone or inside admin.py."""
    libs = domtor.load_libraries()

    win = tk.Toplevel(parent) if parent else tk.Tk()
    win.title('DoMtor — Setup')
    win.geometry('640x520')
    win.resizable(False, False)
    win.transient(parent) if parent else None

    # ---- header ----
    tk.Label(win, text='Welcome to DoMtor!',
             font=('Arial', 20, 'bold'), fg='#2c3e50').pack(pady=(20, 6))
    tk.Label(win,
             text='Before you start programming,\ninstall the starter libraries.',
             font=('Arial', 12), justify='center').pack(pady=(0, 18))

    # ---- scrollable area ----
    container = tk.Frame(win)
    container.pack(fill='both', expand=True, padx=24, pady=4)

    canvas = tk.Canvas(container, highlightthickness=0)
    scroll = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
    inner = tk.Frame(canvas)

    inner.bind('<Configure>',
               lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0, 0), window=inner, anchor='nw')
    canvas.configure(yscrollcommand=scroll.set)
    canvas.pack(side='left', fill='both', expand=True)
    scroll.pack(side='right', fill='y')

    vars_ = {}
    for canon, info in libs.items():
        var = tk.BooleanVar(value=info.get('enabled', True))
        vars_[canon] = var
        row = tk.Frame(inner, padx=6, pady=4)
        row.pack(fill='x')
        cb = tk.Checkbutton(row, variable=var, font=('Arial', 11),
                            text=f"{info['alias']}   —   {info['desc']}")
        cb.pack(anchor='w')

    # ---- buttons ----
    btn = tk.Frame(win)
    btn.pack(fill='x', padx=24, pady=16)

    def select_all():
        for v in vars_.values():
            v.set(True)

    def install():
        for canon, var in vars_.items():
            libs[canon]['enabled'] = var.get()
        domtor.save_libraries(libs)
        domtor.mark_setup_done()
        win.destroy()
        if not parent:
            win.quit()

    def skip():
        domtor.mark_setup_done()
        win.destroy()
        if not parent:
            win.quit()

    tk.Button(btn, text='Skip', command=skip,
              font=('Arial', 10), padx=14, pady=6).pack(side='left')
    tk.Button(btn, text='Select all', command=select_all,
              font=('Arial', 10), padx=14, pady=6).pack(side='left', padx=6)
    tk.Button(btn, text='Install selected', command=install,
              font=('Arial', 11, 'bold'), bg='#4CAF50', fg='white',
              padx=20, pady=6).pack(side='right')

    if not parent:
        win.mainloop()


if __name__ == '__main__':
    show()