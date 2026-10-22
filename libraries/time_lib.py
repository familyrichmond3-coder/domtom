# ==============================================================
# Time library / Библиотека время
# ==============================================================
import time as _t
import datetime as _d

time   = сейчас  = _t.time
sleep  = пауза   = _t.sleep

def today():
    return _d.date.today().isoformat()

def now():
    return _d.datetime.now().isoformat()

def year():
    return _d.date.today().year

def month():
    return _d.date.today().month

def day():
    return _d.date.today().day

def hour():
    return _d.datetime.now().hour

def minute():
    return _d.datetime.now().minute

def second():
    return _d.datetime.now().second

def fmt(pattern):
    return _d.datetime.now().strftime(pattern)

# Cyrillic aliases
сегодня    = today
теперь     = now
год        = year
месяц      = month
день       = day
час        = hour
минута     = minute
секунда    = second
формат     = fmt