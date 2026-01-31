@echo off
REM Быстрый тест десктопной версии CryptoKeyFinder

echo 🖥️  ТЕСТ ДЕСКТОПНОЙ ВЕРСИИ CRYPTOKEYFINDER
echo ==========================================

echo Проверяем Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден!
    echo Установите Python с https://python.org
    pause
    exit /b 1
)

echo ✅ Python найден!

echo.
echo Запускаем Tkinter версию...
echo (Это займет несколько секунд)
echo.

python main_tkinter.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка запуска!
    echo Попробуйте:
    echo 1. python test_tkinter_simple.py
    echo 2. Проверьте зависимости
    echo.
    pause
) else (
    echo.
    echo ✅ Приложение работает!
    echo.
)

pause