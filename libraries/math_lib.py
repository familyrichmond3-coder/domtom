# ==============================================================
# Math library / Библиотека математика
# Both Cyrillic and English names work.
# ==============================================================
import math as _m

# constants
pi = пи = _m.pi
e  = е  = _m.e

# English names
sqrt      = корень     = _m.sqrt
sin       = синус      = _m.sin
cos       = косинус    = _m.cos
tan       = тангенс    = _m.tan
asin      = арксинус   = _m.asin
acos      = арккосинус = _m.acos
atan      = арктангенс = _m.atan
log10     = логарифм10 = _m.log10
exp       = экспонента = _m.exp
floor     = пол        = _m.floor
ceil      = потолок    = _m.ceil
factorial = факториал  = _m.factorial
gcd       = нод        = _m.gcd
radians   = радианы    = _m.radians
degrees   = градусы    = _m.degrees
fmod      = остаток    = _m.fmod
hypot     = гипотенуза = _m.hypot

def log(x, base=None):
    return _m.log(x, base) if base else _m.log(x)

# Cyrillic alias for log
логарифм = log