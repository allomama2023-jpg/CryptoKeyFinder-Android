@echo off
REM Установка Kivy через conda (более надежный способ для Windows)

echo 🐍 УСТАНОВКА KIVY ЧЕРЕЗ CONDA
echo ================================

echo Проверяем наличие conda...
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Conda не установлен!
    echo.
    echo 📥 УСТАНОВИТЕ MINICONDA:
    echo 1. Скачайте с https://docs.conda.io/en/latest/miniconda.html
    echo 2. Установите Miniconda
    echo 3. Перезапустите командную строку
    echo 4. Запустите этот скрипт снова
    pause
    exit /b 1
)

echo ✅ Conda найден!
echo.

echo 1. Создаем окружение для Kivy...
conda create -n kivy_env python=3.11 -y

echo.
echo 2. Активируем окружение...
call conda activate kivy_env

echo.
echo 3. Устанавливаем Kivy...
conda install -c conda-forge kivy -y

echo.
echo 4. Устанавливаем остальные зависимости...
pip install requests ecdsa base58 pycryptodome

echo.
echo ✅ УСТАНОВКА ЗАВЕРШЕНА!
echo.
echo 📋 ДЛЯ ЗАПУСКА ПРИЛОЖЕНИЯ:
echo 1. conda activate kivy_env
echo 2. python run_desktop_test.py
echo.
pause