# -*- mode: python ; coding: utf-8 -*-
# Конфигурация сборки DoMtor в один EXE-файл

a = Analysis(
    ['admin.py'], # Главный файл, с которого всё начинается
    pathex=[],
    binaries=[],
    datas=[
        # Эти строки говорят сборщику: "Возьми папку libraries и examples и положи их внутрь EXE"
        ('libraries', 'libraries'),
        ('examples', 'examples'),
        ('first_run.py', '.'),
    ],
    hiddenimports=['flask', 'tkinter', 'turtle', 'telebot', 'discord', 'vk_api'], # Скрытые модули, которые нужны для ботов
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DoMtor', # Название твоего итогового файла
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # False означает, что при запуске не будет открываться черное окно консоли (только GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None # Сюда потом сможешь вписать путь к иконке: 'icon.ico'
)