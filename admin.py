# ==============================================================
# DoMtor v4.2 — Admin panel + Editor + Guides + Detailed Commands
# ==============================================================
import io
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import domtor
import first_run

# --- ПОДРОБНЫЕ ПРИМЕРЫ ДЛЯ ВСЕХ КОМАНД ---
COMMAND_EXAMPLES = {
    # --- ВСТРОЕННЫЕ ФУНКЦИИ ---
    'print': 'печать("Привет, мир!")\nпечать("Мне", 15, "лет") # Можно выводить несколько вещей через запятую',
    'input': 'имя = ввод("Как тебя зовут? ")\nпечать("Привет,", имя)',
    'len': 'текст = "Привет"\nпечать(длина(текст)) # Выведет 6 (количество букв)\nпечать(длина([1, 2, 3])) # Выведет 3 (количество элементов)',
    'range': 'для i в диапазон(1, 4):\n    печать(i) # Выведет 1, 2, 3 (от 1 до 4, не включая 4)',
    'sum': 'числа = [10, 20, 30]\nпечать(сумма(числа)) # Выведет 60 (10+20+30)',
    'min': 'печать(минимум(5, 2, 8)) # Выведет 2\nпечать(минимум([10, 4, 7])) # Выведет 4',
    'max': 'печать(максимум(5, 2, 8)) # Выведет 8\nпечать(максимум([10, 4, 7])) # Выведет 10',
    'sorted': 'числа = [3, 1, 4, 2]\nпечать(сортировано(числа)) # Выведет [1, 2, 3, 4]',
    'str': 'число = 123\nтекст = строка(число)\nпечать("Это строка: " + текст) # Склеиваем текст и число',
    'int': 'текст = "42"\nчисло = целое(текст)\nпечать(число + 8) # Выведет 50',
    'float': 'число = дробь("3.14")\nпечать(число * 2) # Выведет 6.28',
    'bool': 'печать(булево(1))    # Истина\nпечать(булево(0))    # Ложь\nпечать(булево(""))   # Ложь (пустая строка)',
    'list': 'мой_список = список([1, 2, 3])\nпечать(мой_список[0]) # Выведет 1',
    'dict': 'моя_карта = словарь(имя="Иван", возраст=20)\nпечать(моя_карта["имя"]) # Выведет Иван',
    'tuple': 'мой_кортеж = кортеж([1, 2, 3])\nпечать(мой_кортеж[1]) # Выведет 2',
    'set': 'мое_множество = множество([1, 2, 2, 3])\nпечать(мое_множество) # Выведет {1, 2, 3} (без повторов)',
    'abs': 'печать(модуль(-5)) # Выведет 5 (убирает минус)\nпечать(модуль(3.14)) # 3.14',
    'type': 'печать(тип(123))      # Выведет int (целое)\nпечать(тип("Привет")) # Выведет str (строка)',
    'open': 'файл = открыть("test.txt", "w")\nфайл.write("Привет")\nфайл.close() # Закрываем файл после работы',
    'enumerate': 'фрукты = ["яблоко", "банан"]\nдля i, ф в синумером(фрукты):\n    печать(i, ф) # 0 яблоко, 1 банан',
    'zip': 'имена = ["Иван", "Мария"]\nвозраст = [20, 22]\nдля и, в в склеить(имена, возраст):\n    печать(и, в) # Иван 20, Мария 22',
    'map': 'числа = ["1", "2", "3"]\nновые = преобразить(целое, числа)\nпечать(список(новые)) # [1, 2, 3]',
    'filter': 'числа = [1, 2, 3, 4, 5]\nчетные = отфильтровать(лямбда x: x % 2 == 0, числа)\nпечать(список(четные)) # [2, 4]',
    'any': 'печать(любой([Ложь, Ложь, Истина])) # Выведет Истина (есть хоть один)',
    'all': 'печать(каждый([Истина, Истина, Ложь])) # Выведет Ложь (не все Истина)',
    'round': 'печать(округли(3.14159, 2)) # Выведет 3.14 (2 знака после запятой)',
    'pow': 'печать(степень(2, 3)) # Выведет 8 (2 в степени 3)',
    'chr': 'печать(символ(65)) # Выведет A (буква по её номеру)',
    'ord': 'печать(кодсимвола("A")) # Выведет 65 (номер буквы)',
    'isinstance': 'печать(является(5, целое)) # Истина\nпечать(является("Текст", целое)) # Ложь',

    # --- КЛЮЧЕВЫЕ СЛОВА ---
    'if': 'возраст = 18\nесли возраст >= 18:\n    печать("Взрослый")\nиначе:\n    печать("Ребенок")',
    'elif': 'оценка = 4\nесли оценка == 5:\n    печать("Отлично")\nиначеесли оценка == 4:\n    печать("Хорошо")\nиначе:\n    печать("Плохо")',
    'else': 'если Ложь:\n    печать("Не сработает")\nиначе:\n    печать("Сработает это!")',
    'while': 'i = 0\nпока i < 3:\n    печать(i)\n    i += 1 # Не забывай увеличивать i, иначе будет вечный цикл!',
    'for': 'фрукты = ["яблоко", "банан"]\nдля ф в фрукты:\n    печать(ф)',
    'in': 'если "яблоко" в ["яблоко", "банан"]:\n    печать("Есть такое!")',
    'def': 'функция привет(имя):\n    печать("Привет,", имя)\n\nпривет("Алексей")',
    'return': 'функция квадрат(x):\n    вернуть x * x\n\nрезультат = квадрат(5)\nпечать(результат) # 25',
    'break': 'для i в диапазон(10):\n    если i == 3:\n        стоп # Цикл прервется на цифре 3\n    печать(i)',
    'continue': 'для i в диапазон(5):\n    если i == 2:\n        дальше # Пропустит цифру 2 и пойдет дальше\n    печать(i)',
    'pass': 'если Истина:\n    пропуск # Ничего не делает, просто заглушка',
    'and': 'возраст = 20\nесли возраст > 18 и возраст < 30:\n    печать("Молодой взрослый")',
    'or': 'день = "Суббота"\nесли день == "Суббота" или день == "Воскресенье":\n    печать("Выходной!")',
    'not': 'холодно = Ложь\nесли не холодно:\n    печать("Можно гулять!")',
    'True': 'идет_дождь = Истина\nесли идет_дождь:\n    печать("Берем зонт")',
    'False': 'солнце_светит = Ложь\nесли не солнце_светит:\n    печать("Сидим дома")',
    'None': 'результат = Ничто\nесли результат == Ничто:\n    печать("Пусто")',
    'import': 'подключить математика\nпечать(математика.корень(25))',
    'from': 'из математика подключить корень\nпечать(корень(16)) # Не нужно писать математика.корень',
    'as': 'подключить математика как мат\nпечать(мат.пи) # Используем короткое имя',
    'class': 'класс Собака:\n    функция __init__(self, имя):\n        self.имя = имя\n\n    функция гавкать(self):\n        печать(self.имя, "говорит Гав!")',
    'try': 'попробовать:\n    результат = 10 / 0\nпоймать:\n    печать("На ноль делить нельзя!")',
    'except': 'попробовать:\n    x = 1 + 1\nпоймать Ошибка:\n    печать("Что-то пошло не так")',
    'finally': 'попробовать:\n    печать("Пытаемся")\nвконце:\n    печать("Это выполнится в любом случае")',
    'with': 'используя открыть("test.txt", "w") как файл:\n    файл.write("Привет") # Файл закроется сам',
    'lambda': 'квадрат = лямбда x: x * x\nпечать(квадрат(5)) # Выведет 25',
    'yield': 'функция счетчик():\n    уступить 1\n    уступить 2\n\nдля i в счетчик():\n    печать(i)',
    'global': 'x = 10\nфункция изменить():\n    глобально x\n    x = 20\nизменить()\nпечать(x) # Выведет 20',
    'del': 'x = 10\nудалить x\n# печать(x) выдаст ошибку, так как x больше нет',
}

# --- Тексты для вкладки "Гайды" ---
GUIDES = {
    "1. Первая программа": {
        "text": """Добро пожаловать в DoMtor! 
Давай напишем твою первую программу.

Команда `печать` выводит текст на экран. 
Текст должен быть в кавычках.

Нажми кнопку "▶ Проверить этот код" ниже, чтобы запустить его!""",
        "code": 'печать("Привет, мир! Я программирую на DoMtor.")\n'
    },
    "2. Переменные и математика": {
        "text": """Переменная — это коробка, в которую мы кладем данные.
Создается она очень просто: придумываешь имя и ставишь знак `=`.

Текст (строки) мы пишем в кавычках, а числа — без них.
С числами можно делать математику: +, -, *, /""",
        "code": 'имя = "Александр"\nвозраст = 15\nследующий_год = возраст + 1\n\nпечать("Меня зовут", имя)\nпечать("Мне", возраст, "лет")\nпечать("В следующем году мне будет", следующий_год)\n'
    },
    "3. Условия (Если)": {
        "text": """Чтобы программа принимала решения, используется `если`.
Если условие верное — выполняется код под ним (с отступом в 4 пробела).

Также есть `иначе` — что делать, если условие неверное.""",
        "code": 'оценка = 5\n\nесли оценка == 5:\n    печать("Отлично! Ты молодец.")\nиначе:\n    печать("Надо подтянуть учебу.")\n'
    },
    "4. Циклы (Повторения)": {
        "text": """Чтобы не писать одно и то же 100 раз, используют циклы.
`для` берет список или диапазон и перебирает его.

`диапазон(1, 5)` создает числа от 1 до 4.""",
        "code": 'для i в диапазон(1, 6):\n    печать("Считаю до шести:", i)\n'
    },
    "5. Библиотеки (Импорт)": {
        "text": """В DoMtor уже встроены крутые библиотеки.
Чтобы их использовать, нужно написать `подключить`.

Давай подключим математику и случайные числа.""",
        "code": 'подключить математика\nподключить случайное\n\nпечать("Корень из 25 =", математика.корень(25))\nпечать("Случайное число:", случайное.целое(1, 100))\n'
    }
}

class App:
    def __init__(self, root):
        self.root = root
        root.title(f'{domtor.LANGUAGE} v4.2 - IDE')
        root.geometry('1200x800')

        self.cmds = domtor.load_commands()
        self.libs = domtor.load_libraries()

        self._build_menu()

        self.nb = ttk.Notebook(root)
        self.nb.pack(fill='both', expand=True)
        
        self.tab_guide = ttk.Frame(self.nb); self.nb.add(self.tab_guide, text='📖 Гайды (Обучение)')
        self.tab_ed = ttk.Frame(self.nb);    self.nb.add(self.tab_ed,   text='💻 Редактор')
        self.tab_cmd = ttk.Frame(self.nb);   self.nb.add(self.tab_cmd,  text='⚙️ Команды')
        self.tab_lib = ttk.Frame(self.nb);   self.nb.add(self.tab_lib,  text='📚 Библиотеки')

        self._build_guide()
        self._build_editor()
        self._build_cmds()
        self._build_libs()

        self.apply_theme('dark')

        if domtor.needs_setup():
            root.after(300, lambda: first_run.show(root))

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Тёмная", command=lambda: self.apply_theme('dark'))
        theme_menu.add_command(label="Светлая", command=lambda: self.apply_theme('light'))
        theme_menu.add_command(label="Хакер (Зеленая)", command=lambda: self.apply_theme('hacker'))
        menubar.add_cascade(label="🎨 Сменить тему", menu=theme_menu)
        self.root.config(menu=menubar)

    def apply_theme(self, theme):
        style = ttk.Style()
        bg, fg, code_bg, code_fg = '#2b2b2b', 'white', '#1e1e1e', '#d4d4d4'
        
        if theme == 'light':
            bg, fg, code_bg, code_fg = '#f0f0f0', 'black', '#ffffff', '#000000'
            style.theme_use('clam')
        elif theme == 'hacker':
            bg, fg, code_bg, code_fg = 'black', '#00ff00', '#0a0a0a', '#00ff00'
            style.theme_use('clam')
        else:
            style.theme_use('clam')

        self.root.configure(bg=bg)
        style.configure('TFrame', background=bg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TNotebook', background=bg)
        
        self.code.configure(bg=code_bg, fg=code_fg, insertbackground=fg)
        self.out.configure(bg=code_bg, fg=code_fg, insertbackground=fg)
        self.guide_text.configure(bg=code_bg, fg=code_fg, insertbackground=fg)
        self.cmd_info.configure(bg=code_bg, fg=code_fg, insertbackground=fg)

    # ---------------- ГАЙДЫ ----------------
    def _build_guide(self):
        paned = ttk.PanedWindow(self.tab_guide, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(paned)
        self.lesson_list = tk.Listbox(left_frame, font=('Arial', 12), width=25)
        self.lesson_list.pack(fill='both', expand=True)
        for title in GUIDES.keys():
            self.lesson_list.insert('end', title)
        self.lesson_list.bind('<<ListboxSelect>>', self._on_guide_select)
        paned.add(left_frame, weight=1)

        right_frame = ttk.Frame(paned)
        self.guide_text = scrolledtext.ScrolledText(right_frame, wrap='word', font=('Arial', 14))
        self.guide_text.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="▶ Проверить этот код", command=self._run_guide_code).pack(side='right')
        paned.add(right_frame, weight=3)
        
        self.current_guide_code = ""

    def _on_guide_select(self, event):
        sel = self.lesson_list.curselection()
        if not sel: return
        title = self.lesson_list.get(sel[0])
        data = GUIDES[title]
        
        self.guide_text.delete('1.0', 'end')
        self.guide_text.insert('end', data["text"] + "\n\n--- ПРИМЕР КОДА ---\n\n" + data["code"])
        self.current_guide_code = data["code"]

    def _run_guide_code(self):
        if not self.current_guide_code:
            messagebox.showinfo("Внимание", "Сначала выбери урок слева!")
            return
        self.code.delete('1.0', 'end')
        self.code.insert('1.0', self.current_guide_code)
        self.nb.select(self.tab_ed)
        self._run_code()

    # ---------------- РЕДАКТОР ----------------
    def _build_editor(self):
        bar = ttk.Frame(self.tab_ed); bar.pack(fill='x', padx=6, pady=4)
        ttk.Button(bar, text='▶ Запустить', command=self._run_code).pack(side='left')
        ttk.Button(bar, text='Открыть…', command=self._open).pack(side='left', padx=4)
        ttk.Button(bar, text='Сохранить…', command=self._save).pack(side='left')

        paned = ttk.PanedWindow(self.tab_ed, orient='vertical')
        paned.pack(fill='both', expand=True, padx=6, pady=4)

        self.code = scrolledtext.ScrolledText(paned, font=('Consolas', 12), undo=True)
        paned.add(self.code, weight=3)

        self.out = scrolledtext.ScrolledText(paned, font=('Consolas', 11))
        paned.add(self.out, weight=1)

        self.code.insert('1.0', '''# Добро пожаловать в DoMtor v4.2!
# Загляни во вкладку "📖 Гайды", если не знаешь, с чего начать.
печать("Привет, мир!")
''')

    def _run_code(self):
        src = self.code.get('1.0', 'end')
        self.out.delete('1.0', 'end')
        
        old_stdout = sys.stdout
        buf = io.StringIO(); sys.stdout = buf
        
        try:
            domtor.run(src)
        except Exception as e:
            sys.stdout = old_stdout
            self.out.insert('end', f'\n[Ошибка] {e}\n')
            return
        finally:
            sys.stdout = old_stdout
        self.out.insert('end', buf.getvalue() or '(Программа завершена)')

    def _open(self):
        p = filedialog.askopenfilename(filetypes=[('DoMtor', '*.dm')])
        if p:
            self.code.delete('1.0', 'end')
            self.code.insert('1.0', open(p, encoding='utf-8').read())

    def _save(self):
        p = filedialog.asksaveasfilename(defaultextension='.dm', filetypes=[('DoMtor', '*.dm')])
        if p:
            open(p, 'w', encoding='utf-8').write(self.code.get('1.0', 'end'))

    # ---------------- КОМАНДЫ ----------------
    def _build_cmds(self):
        paned = ttk.PanedWindow(self.tab_cmd, orient='vertical')
        paned.pack(fill='both', expand=True, padx=8, pady=8)

        top_frame = ttk.Frame(paned)
        cols = ('canon', 'alias', 'kind', 'desc')
        self.tree_cmd = ttk.Treeview(top_frame, columns=cols, show='headings', height=12)
        
        # Обновленные заголовки, как ты просил
        self.tree_cmd.heading('canon', text='Python (Оригинал)')
        self.tree_cmd.heading('alias', text='DoMtor (Твой псевдоним)')
        self.tree_cmd.heading('kind', text='Тип')
        self.tree_cmd.heading('desc', text='Что делает')
        
        self.tree_cmd.column('canon', width=120)
        self.tree_cmd.column('alias', width=160)
        self.tree_cmd.column('kind', width=80)
        self.tree_cmd.column('desc', width=400)
        
        self.tree_cmd.pack(fill='both', expand=True)
        self.tree_cmd.bind('<<TreeviewSelect>>', self._on_cmd_select)

        for k, v in self.cmds.items():
            self.tree_cmd.insert('', 'end', values=(k, v['alias'], v['kind'], v['desc']))
            
        paned.add(top_frame, weight=1)

        bottom_frame = ttk.Frame(paned)
        self.cmd_info = scrolledtext.ScrolledText(bottom_frame, wrap='word', font=('Consolas', 12), height=10)
        self.cmd_info.pack(fill='both', expand=True)
        self.cmd_info.insert('end', 'Выбери команду в таблице выше, чтобы увидеть подробный пример её использования.')
        self.cmd_info.config(state='disabled')
        paned.add(bottom_frame, weight=1)

    def _on_cmd_select(self, event):
        sel = self.tree_cmd.selection()
        if not sel: return
        
        values = self.tree_cmd.item(sel[0])['values']
        canon = values[0]  # Это Python (например, del)
        alias = values[1]  # Это DoMtor (например, удалить)
        desc = values[3]   # Описание
        
        # Ищем пример
        example = COMMAND_EXAMPLES.get(canon, "Пример для этой команды пока не добавлен.")
        
        # Формируем красивый текст с оригиналом и псевдонимом
        info_text = f"В PYTHON:  {canon}\n"
        info_text += f"В DOMTOR:  {alias}\n"
        info_text += f"ЧТО ДЕЛАЕТ: {desc}\n"
        info_text += "=" * 50 + "\n"
        info_text += "ПРИМЕР КОДА НА DOMTOR:\n\n"
        info_text += example
        
        self.cmd_info.config(state='normal')
        self.cmd_info.delete('1.0', 'end')
        self.cmd_info.insert('end', info_text)
        self.cmd_info.config(state='disabled')

    # ---------------- БИБЛИОТЕКИ ----------------
    def _build_libs(self):
        self.tree_lib = ttk.Treeview(self.tab_lib, columns=('c','a'), show='headings')
        self.tree_lib.heading('c', text='Модуль'); self.tree_lib.heading('a', text='Псевдоним')
        self.tree_lib.pack(fill='both', expand=True, padx=8, pady=8)
        for k, v in self.libs.items():
            self.tree_lib.insert('', 'end', values=(k, v['alias']))

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.lesson_list.selection_set(0)
    app._on_guide_select(None)
    root.mainloop()