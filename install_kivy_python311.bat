@echo off
REM Установка Kivy с Python 3.11 (более совместимая версия)

echo 🐍 УСТАНОВКА KIVY С PYTHON 3.11
echo ==================================

echo ⚠️ ПРОБЛЕМА: Python 3.14 не полностью совместим с Kivy
echo.
echo 💡 РЕШЕНИЯ:
echo.
echo 1. УСТАНОВИТЬ PYTHON 3.11:
echo    - Скачайте Python 3.11 с https://www.python.org/downloads/
echo    - Установите параллельно с текущей версией
echo    - Используйте py -3.11 для запуска
echo.
echo 2. ИСПОЛЬЗОВАТЬ CONDA (рекомендуется):
echo    - Запустите install_kivy_conda.bat
echo.
echo 3. ИСПОЛЬЗОВАТЬ ВИРТУАЛЬНОЕ ОКРУЖЕНИЕ:
echo    - py -3.11 -m venv kivy_env
echo    - kivy_env\Scripts\activate
echo    - pip install kivy requests ecdsa base58 pycryptodome
echo.
echo 4. АЛЬТЕРНАТИВА - TKINTER ВЕРСИЯ:
echo    - Создать версию на Tkinter вместо Kivy
echo    - Tkinter входит в стандартную библиотеку Python
echo.
pause