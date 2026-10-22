# ==============================================================
# Game library / Библиотека игра (turtle)
# ==============================================================
import turtle as _turtle

_screen = None

def start(width=800, height=600, title='DoMtor Game', bg='white'):
    global _screen
    _screen = _turtle.Screen()
    _screen.setup(width, height)
    _screen.title(title)
    _screen.bgcolor(bg)
    return _screen

def hero(shape='turtle', color='blue'):
    t = _turtle.Turtle()
    t.shape(shape)
    t.color(color)
    t.penup()
    return t

def on_key(fn, key):
    _turtle.Screen().onkey(fn, key)

def listen():
    _turtle.Screen().listen()

def done():
    _turtle.done()

# Cyrillic aliases
запустить   = start
герой       = hero
на_клавишу  = on_key
слушать     = listen
показать    = done