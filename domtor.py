# ==============================================================
# DoMtor v4.0 — language core
# Previous name: __init__.py (which has double underscores __).
# That name is a Python system marker and cannot be renamed.
# We merged the whole language into one file domtor.py.
# ==============================================================
import importlib.util
import io
import json
import os
import sys
import tokenize

LANGUAGE = 'DoMtor'
VERSION  = '4.0'

# Data lives next to the .exe (portable) or next to this file (dev mode)
if getattr(sys, 'frozen', False):
    _BASE = os.path.dirname(sys.executable)
else:
    _BASE = os.path.dirname(os.path.abspath(__file__))

_DATA = os.path.join(_BASE, 'data')
_LIBS = os.path.join(_BASE, 'libraries')
os.makedirs(_DATA, exist_ok=True)

_CMD_PATH   = os.path.join(_DATA, 'commands.json')
_LIB_PATH   = os.path.join(_DATA, 'libraries.json')
_FLAG_PATH  = os.path.join(_DATA, 'first_run_done.flag')


# ============================================================
# 1. TRANSLATOR: DoMtor words -> Python words
# ============================================================
def translate(source, keyword_aliases):
    if not keyword_aliases:
        return source
    lines = source.split('\n')
    offsets = [0]
    for line in lines[:-1]:
        offsets.append(offsets[-1] + len(line) + 1)
    replacements = []
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError):
        return source
    for tok in tokens:
        if tok.type != tokenize.NAME:
            continue
        word = tok.string
        if word not in keyword_aliases:
            continue
        sl, sc = tok.start
        if sc > 0 and lines[sl - 1][sc - 1] == '.':
            continue
        start_off = offsets[sl - 1] + sc
        el, ec = tok.end
        end_off = offsets[el - 1] + ec
        replacements.append((start_off, end_off, keyword_aliases[word]))
    result = source
    for s, e, r in sorted(replacements, reverse=True):
        result = result[:s] + r + result[e:]
    return result


# ============================================================
# 2. LIBRARY LOADER
# ============================================================
def _load_libraries(lib_dir, libraries):
    for canon, info in libraries.items():
        if not info.get('enabled', True):
            continue
        alias = info['alias']
        path = os.path.join(lib_dir, info['path'])
        if not os.path.exists(path) or alias in sys.modules:
            continue
        try:
            spec = importlib.util.spec_from_file_location(alias, path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[alias] = mod
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f'[DoMtor] Library {alias}: {e}')


# ============================================================
# 3. BUILT-IN FUNCTIONS
# ============================================================
def _type_name(x):
    if x is None:
        return 'None'
    return type(x).__name__

BUILTINS = {
    'print': print, 'input': input, 'len': len, 'range': range,
    'str': str, 'int': int, 'float': float, 'bool': bool,
    'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
    'abs': abs, 'sum': sum, 'min': min, 'max': max,
    'sorted': sorted, 'reversed': reversed, 'round': round, 'pow': pow,
    'open': open, 'enumerate': enumerate, 'zip': zip, 'map': map,
    'filter': filter, 'any': any, 'all': all,
    'chr': chr, 'ord': ord, 'isinstance': isinstance,
    'type': _type_name,
}


# ============================================================
# 4. DEFAULT COMMANDS (DoMtor words)
# ============================================================
DEFAULT_COMMANDS = {
    # --- builtins ---
    'print':     {'alias': 'печать',      'desc': 'Вывести в консоль',    'kind': 'builtin'},
    'input':     {'alias': 'ввод',        'desc': 'Прочитать строку',     'kind': 'builtin'},
    'len':       {'alias': 'длина',       'desc': 'Длина',                'kind': 'builtin'},
    'range':     {'alias': 'диапазон',    'desc': 'Диапазон чисел',       'kind': 'builtin'},
    'sum':       {'alias': 'сумма',       'desc': 'Сумма списка',         'kind': 'builtin'},
    'min':       {'alias': 'минимум',     'desc': 'Минимум',              'kind': 'builtin'},
    'max':       {'alias': 'максимум',    'desc': 'Максимум',             'kind': 'builtin'},
    'sorted':    {'alias': 'сортировано', 'desc': 'Сортировка',           'kind': 'builtin'},
    'str':       {'alias': 'строка',      'desc': 'В строку',             'kind': 'builtin'},
    'int':       {'alias': 'целое',       'desc': 'В целое',              'kind': 'builtin'},
    'float':     {'alias': 'дробь',       'desc': 'В дробное',            'kind': 'builtin'},
    'bool':      {'alias': 'булево',      'desc': 'В логическое',         'kind': 'builtin'},
    'list':      {'alias': 'список',      'desc': 'Создать список',       'kind': 'builtin'},
    'dict':      {'alias': 'словарь',     'desc': 'Создать словарь',      'kind': 'builtin'},
    'tuple':     {'alias': 'кортеж',      'desc': 'Создать кортеж',       'kind': 'builtin'},
    'set':       {'alias': 'множество',   'desc': 'Создать множество',    'kind': 'builtin'},
    'abs':       {'alias': 'модуль',      'desc': 'Модуль числа',         'kind': 'builtin'},
    'type':      {'alias': 'тип',         'desc': 'Тип значения',         'kind': 'builtin'},
    'open':      {'alias': 'открыть',     'desc': 'Открыть файл',         'kind': 'builtin'},
    'enumerate': {'alias': 'синумером',   'desc': 'Индексы + значения',   'kind': 'builtin'},
    'zip':       {'alias': 'склеить',     'desc': 'Склеить итераторы',    'kind': 'builtin'},
    'map':       {'alias': 'преобразить', 'desc': 'Преобразовать',        'kind': 'builtin'},
    'filter':    {'alias': 'отфильтровать','desc': 'Отфильтровать',       'kind': 'builtin'},
    'any':       {'alias': 'любой',       'desc': 'Хоть один True',       'kind': 'builtin'},
    'all':       {'alias': 'каждый',      'desc': 'Все True',             'kind': 'builtin'},
    'round':     {'alias': 'округли',     'desc': 'Округлить',            'kind': 'builtin'},
    'pow':       {'alias': 'степень',     'desc': 'Возвести в степень',   'kind': 'builtin'},
    'chr':       {'alias': 'символ',      'desc': 'Код → символ',         'kind': 'builtin'},
    'ord':       {'alias': 'кодсимвола',  'desc': 'Символ → код',         'kind': 'builtin'},
    'isinstance':{'alias': 'является',    'desc': 'Проверка типа',        'kind': 'builtin'},

    # --- keywords ---
    'if':       {'alias': 'если',       'desc': 'Условие',               'kind': 'keyword'},
    'elif':     {'alias': 'иначеесли',  'desc': 'Иначе если',            'kind': 'keyword'},
    'else':     {'alias': 'иначе',      'desc': 'Иначе',                 'kind': 'keyword'},
    'while':    {'alias': 'пока',       'desc': 'Цикл с условием',       'kind': 'keyword'},
    'for':      {'alias': 'для',        'desc': 'Цикл по элементам',     'kind': 'keyword'},
    'in':       {'alias': 'в',          'desc': 'Вхождение',             'kind': 'keyword'},
    'def':      {'alias': 'функция',    'desc': 'Объявление функции',    'kind': 'keyword'},
    'return':   {'alias': 'вернуть',    'desc': 'Вернуть значение',      'kind': 'keyword'},
    'break':    {'alias': 'стоп',       'desc': 'Выйти из цикла',        'kind': 'keyword'},
    'continue': {'alias': 'дальше',     'desc': 'Следующая итерация',    'kind': 'keyword'},
    'pass':     {'alias': 'пропуск',    'desc': 'Ничего не делать',      'kind': 'keyword'},
    'and':      {'alias': 'и',          'desc': 'Логическое И',          'kind': 'keyword'},
    'or':       {'alias': 'или',        'desc': 'Логическое ИЛИ',        'kind': 'keyword'},
    'not':      {'alias': 'не',         'desc': 'Логическое НЕ',         'kind': 'keyword'},
    'True':     {'alias': 'Истина',     'desc': 'Истина',                'kind': 'keyword'},
    'False':    {'alias': 'Ложь',       'desc': 'Ложь',                  'kind': 'keyword'},
    'None':     {'alias': 'Ничто',      'desc': 'Пустое значение',       'kind': 'keyword'},
    'import':   {'alias': 'подключить', 'desc': 'Подключить библиотеку', 'kind': 'keyword'},
    'from':     {'alias': 'из',         'desc': 'Импорт из модуля',      'kind': 'keyword'},
    'as':       {'alias': 'как',        'desc': 'Псевдоним',             'kind': 'keyword'},
    'class':    {'alias': 'класс',      'desc': 'Класс',                 'kind': 'keyword'},
    'try':      {'alias': 'попробовать','desc': 'Блок try',              'kind': 'keyword'},
    'except':   {'alias': 'поймать',    'desc': 'Обработчик ошибки',     'kind': 'keyword'},
    'finally':  {'alias': 'вконце',     'desc': 'Выполнить в конце',     'kind': 'keyword'},
    'with':     {'alias': 'используя',  'desc': 'Контекстный менеджер',  'kind': 'keyword'},
    'lambda':   {'alias': 'лямбда',     'desc': 'Анонимная функция',     'kind': 'keyword'},
    'yield':    {'alias': 'уступить',   'desc': 'Генератор',             'kind': 'keyword'},
    'global':   {'alias': 'глобально',  'desc': 'Глобальная область',    'kind': 'keyword'},
    'del':      {'alias': 'удалить',    'desc': 'Удалить',               'kind': 'keyword'},
}


# ============================================================
# 5. DEFAULT LIBRARIES (English filenames)
# ============================================================
DEFAULT_LIBRARIES = {
    'math':   {'alias': 'математика', 'desc': 'Математика / Math',         'path': 'math_lib.py',   'enabled': True},
    'random': {'alias': 'случайное',  'desc': 'Случайные числа / Random',  'path': 'random_lib.py', 'enabled': True},
    'time':   {'alias': 'время',      'desc': 'Время и дата / Time',       'path': 'time_lib.py',   'enabled': True},
    'system': {'alias': 'система',    'desc': 'Файлы и папки / Files',     'path': 'system_lib.py', 'enabled': True},
    'gui':    {'alias': 'окна',       'desc': 'Приложения / GUI (tkinter)','path': 'gui_lib.py',    'enabled': True},
    'web':    {'alias': 'веб',        'desc': 'Сайты / Web (Flask)',       'path': 'web_lib.py',    'enabled': True},
    'game':   {'alias': 'игра',       'desc': 'Игры / Games (turtle)',     'path': 'game_lib.py',   'enabled': True},
    
    # --- НОВЫЕ БИБЛИОТЕКИ ДЛЯ БОТОВ ---
    'tg_bot': {'alias': 'телеграм',   'desc': 'Telegram боты',             'path': 'tg_bot_lib.py',      'enabled': True},
    'ds_bot': {'alias': 'дискорд',    'desc': 'Discord боты',              'path': 'discord_bot_lib.py', 'enabled': True},
    'vk_bot': {'alias': 'вк',         'desc': 'VK боты',                   'path': 'vk_bot_lib.py',      'enabled': True},
}


# ============================================================
# 6. SAVE / LOAD SETTINGS
# ============================================================
def _load(path, defaults):
    if not os.path.exists(path):
        _save(path, defaults)
        return {k: dict(v) for k, v in defaults.items()}
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}
    out = {k: dict(v) for k, v in defaults.items()}
    for k, v in data.items():
        if k in out:
            out[k].update(v)
    return out


def _save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_commands():   return _load(_CMD_PATH, DEFAULT_COMMANDS)
def save_commands(c):  _save(_CMD_PATH, c)
def load_libraries():  return _load(_LIB_PATH, DEFAULT_LIBRARIES)
def save_libraries(l): _save(_LIB_PATH, l)


def needs_setup():
    return not os.path.exists(_FLAG_PATH)


def mark_setup_done():
    with open(_FLAG_PATH, 'w', encoding='utf-8') as f:
        f.write('ok')


# ============================================================
# 7. MAIN ENTRY POINT
# ============================================================
def run(source, filename='<dm>'):
    commands = load_commands()
    libraries = load_libraries()
    _load_libraries(_LIBS, libraries)

    aliases = {info['alias']: canon
               for canon, info in commands.items()
               if info['kind'] == 'keyword'}
    py_source = translate(source, aliases)

    env = {'__name__': '__main__', '__file__': filename,
           '__builtins__': __builtins__}
    for canon, info in commands.items():
        if info['kind'] == 'builtin':
            fn = BUILTINS.get(canon)
            if fn:
                env[info['alias']] = fn

    try:
        code = compile(py_source, filename, 'exec')
    except SyntaxError as e:
        raise SyntaxError(f'DoMtor syntax: {e}') from None
    exec(code, env)


if __name__ == '__main__':
    print(f'{LANGUAGE} v{VERSION}')