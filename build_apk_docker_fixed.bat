@echo off
REM Исправленная Docker сборка Android APK

echo 🐳 DOCKER СБОРКА ANDROID APK (ИСПРАВЛЕННАЯ)
echo ============================================

echo 1. Проверяем Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не установлен!
    echo.
    echo 📥 УСТАНОВКА DOCKER:
    echo 1. Скачайте Docker Desktop с https://www.docker.com/products/docker-desktop
    echo 2. Установите Docker Desktop
    echo 3. Запустите Docker Desktop
    echo 4. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo ✅ Docker найден!

echo.
echo 2. Создаем Dockerfile...
echo FROM kivy/buildozer:latest > Dockerfile
echo WORKDIR /app >> Dockerfile
echo COPY . /app >> Dockerfile
echo RUN buildozer android debug >> Dockerfile

echo.
echo 3. Собираем APK через Docker...
docker build -t cryptokeyfinder-android .

echo.
echo 4. Извлекаем APK из контейнера...
docker create --name temp-container cryptokeyfinder-android
docker cp temp-container:/app/bin/. ./bin/
docker rm temp-container

echo.
if exist "bin\*.apk" (
    echo 🎉 APK УСПЕШНО СОЗДАН ЧЕРЕЗ DOCKER!
    echo 📁 Файл APK находится в папке bin\
    dir bin\*.apk
    echo.
    echo 📱 УСТАНОВКА НА ANDROID:
    echo 1. Скопируйте APK на Android устройство
    echo 2. Включите "Неизвестные источники" в настройках
    echo 3. Установите APK
    echo.
) else (
    echo ❌ Ошибка создания APK через Docker!
    echo Попробуйте ручную сборку или GitHub Actions
)

pause