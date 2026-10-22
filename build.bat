@echo off
pip install -r requirements.txt
pyinstaller build.spec --clean --noconfirm
echo.
echo Done! Your app is in dist\DoMtor.exe
pause