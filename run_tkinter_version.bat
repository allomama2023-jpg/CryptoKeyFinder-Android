@echo off
REM Запуск Tkinter версии CryptoKeyFinder (работает без Kivy)

echo 🖥️ ЗАПУСК TKINTER ВЕРСИИ CryptoKeyFinder
echo ==========================================

echo ✅ Tkinter входит в стандартную библиотеку Python
echo ✅ Не требует установки дополнительных зависимостей
echo.

echo Проверяем наличие файлов...
if not exist "main_tkinter.py" (
    echo ❌ Файл main_tkinter.py не найден!
    pause
    exit /b 1
)

if not exist "crypto_utils_android.py" (
    echo ❌ Файл crypto_utils_android.py не найден!
    pause
    exit /b 1
)

echo ✅ Все файлы найдены

echo.
echo 📦 Устанавливаем только необходимые зависимости...
pip install requests ecdsa base58 pycryptodome

echo.
echo 🚀 Запускаем Tkinter версию...
python main_tkinter.py

echo.
echo ✅ Программа завершена!
pause