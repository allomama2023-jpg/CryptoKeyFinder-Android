@echo off
REM Сборка Android APK через Docker

echo 🐳 СБОРКА ANDROID APK ЧЕРЕЗ DOCKER
echo ==================================

echo 1. Проверяем наличие Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не установлен!
    echo.
    echo 📥 УСТАНОВКА DOCKER:
    echo 1. Скачайте Docker Desktop с https://www.docker.com/products/docker-desktop
    echo 2. Установите Docker Desktop
    echo 3. Перезагрузите компьютер
    echo 4. Запустите Docker Desktop
    echo 5. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo ✅ Docker найден!

echo.
echo 2. Проверяем запущен ли Docker...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не запущен!
    echo.
    echo 🚀 ЗАПУСК DOCKER:
    echo 1. Запустите Docker Desktop
    echo 2. Дождитесь полной загрузки
    echo 3. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo ✅ Docker запущен!

echo.
echo 3. Скачиваем Docker образ для buildozer...
docker pull kivy/buildozer

echo.
echo 4. Собираем APK через Docker...
docker run --rm -v "%cd%":/home/user/hostcwd kivy/buildozer android debug

echo.
if exist "bin\*.apk" (
    echo 🎉 APK УСПЕШНО СОЗДАН!
    echo 📁 Файл APK находится в папке bin\
    dir bin\*.apk
    echo.
    echo 📱 УСТАНОВКА НА ANDROID:
    echo 1. Скопируйте APK на Android устройство
    echo 2. Включите "Неизвестные источники" в настройках
    echo 3. Установите APK
    echo.
) else (
    echo ❌ Ошибка создания APK!
    echo Проверьте логи Docker выше
)

pause