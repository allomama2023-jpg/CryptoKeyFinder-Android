@echo off
REM Установка всех зависимостей для Android версии CryptoKeyFinder

echo 📦 УСТАНОВКА ЗАВИСИМОСТЕЙ ДЛЯ ANDROID ВЕРСИИ
echo ================================================

echo 1. Установка Kivy...
pip install kivy

echo.
echo 2. Установка requests...
pip install requests

echo.
echo 3. Установка ecdsa...
pip install ecdsa

echo.
echo 4. Установка base58...
pip install base58

echo.
echo 5. Установка pycryptodome...
pip install pycryptodome

echo.
echo 6. Установка buildozer (для будущей сборки APK)...
pip install buildozer

echo.
echo ✅ ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ!
echo.
echo 📋 СЛЕДУЮЩИЕ ШАГИ:
echo 1. Для тестирования на Windows: python run_desktop_test.py
echo 2. Для сборки APK: используйте WSL (см. WINDOWS_BUILD_GUIDE.md)
echo.
pause