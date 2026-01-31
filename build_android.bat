@echo off
REM Скрипт сборки Android APK для CryptoKeyFinder (Windows)

echo 🚀 Начинаем сборку CryptoKeyFinder для Android...

REM Проверяем наличие buildozer
buildozer --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Buildozer не установлен!
    echo Установите его командой: pip install buildozer
    pause
    exit /b 1
)

REM Проверяем наличие основных файлов
if not exist "main.py" (
    echo ❌ Файл main.py не найден!
    pause
    exit /b 1
)

if not exist "crypto_utils_android.py" (
    echo ❌ Файл crypto_utils_android.py не найден!
    pause
    exit /b 1
)

if not exist "buildozer.spec" (
    echo ❌ Файл buildozer.spec не найден!
    pause
    exit /b 1
)

echo ✅ Все необходимые файлы найдены

REM Очистка предыдущих сборок
echo 🧹 Очистка предыдущих сборок...
buildozer android clean

REM Сборка APK в debug режиме
echo 📱 Сборка Android APK...
buildozer android debug

REM Проверяем результат
if exist "bin\*.apk" (
    echo 🎉 Сборка завершена успешно!
    echo 📁 APK файлы находятся в папке bin\
    dir bin\*.apk
    
    echo.
    echo 📋 Инструкции по установке:
    echo 1. Скопируйте APK файл на Android устройство
    echo 2. Включите 'Неизвестные источники' в настройках безопасности
    echo 3. Установите APK файл
    echo 4. Запустите CryptoKeyFinder Mobile
    
) else (
    echo ❌ Ошибка сборки! APK файл не создан.
    echo Проверьте логи выше для диагностики проблем.
    pause
    exit /b 1
)

echo ✅ Готово!
pause