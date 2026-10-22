# ==============================================================
# System library / Библиотека система
# ==============================================================
import os as _os
from pathlib import Path as _Path

def getcwd():
    return _os.getcwd()

def listdir(path='.'):
    return _os.listdir(path)

def mkdir(path):
    _os.makedirs(path, exist_ok=True)

def remove(path):
    _os.remove(path)

def rename(src, dst):
    _os.rename(src, dst)

def exists(path):
    return _os.path.exists(path)

def read(file):
    return _Path(file).read_text(encoding='utf-8')

def write(file, text):
    _Path(file).write_text(text, encoding='utf-8')

def size(file):
    return _os.path.getsize(file)

# Cyrillic aliases
текущая_папка     = getcwd
список_файлов     = listdir
создать_папку     = mkdir
удалить           = remove
переименовать     = rename
существует        = exists
прочитать         = read
записать          = write
размер            = size