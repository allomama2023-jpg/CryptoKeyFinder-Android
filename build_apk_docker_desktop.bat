@echo off
REM Сборка APK через Docker Desktop

echo 🐳 СБОРКА APK ЧЕРЕЗ DOCKER DESKTOP
echo =================================

echo Проверяем Docker Desktop...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Desktop не запущен!
    echo.
    echo 📥 ЗАПУСТИТЕ DOCKER DESKTOP:
    echo 1. Найдите Docker Desktop в меню Пуск
    echo 2. Запустите Docker Desktop
    echo 3. Дождитесь зеленого индикатора "Engine running"
    echo 4. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo ✅ Docker Desktop работает!

echo.
echo 🔧 Создаем оптимизированный Dockerfile...
echo # Используем специальный образ для Android сборки > Dockerfile
echo FROM cimg/android:2023.12 >> Dockerfile
echo. >> Dockerfile
echo # Устанавливаем рабочую директорию >> Dockerfile
echo WORKDIR /app >> Dockerfile
echo. >> Dockerfile
echo # Копируем файлы проекта >> Dockerfile
echo COPY . /app >> Dockerfile
echo. >> Dockerfile
echo # Устанавливаем Python зависимости >> Dockerfile
echo RUN sudo apt-get update ^&^& sudo apt-get install -y python3-pip >> Dockerfile
echo RUN pip3 install --user buildozer cython >> Dockerfile
echo. >> Dockerfile
echo # Создаем оптимизированный buildozer.spec >> Dockerfile
echo RUN echo '[app]' ^> buildozer.spec >> Dockerfile
echo RUN echo 'title = CryptoKeyFinder Mobile' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'package.name = cryptokeyfinder' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'package.domain = org.cryptokeyfinder' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'source.dir = .' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'version = 1.0' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'requirements = python3,kivy,requests' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'orientation = portrait' ^>^> buildozer.spec >> Dockerfile
echo RUN echo '[buildozer]' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'log_level = 1' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'warn_on_root = 0' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'android.api = 28' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'android.minapi = 21' ^>^> buildozer.spec >> Dockerfile
echo RUN echo 'android.archs = arm64-v8a' ^>^> buildozer.spec >> Dockerfile
echo. >> Dockerfile
echo # Настраиваем переменные окружения >> Dockerfile
echo ENV PATH="/home/circleci/.local/bin:$PATH" >> Dockerfile
echo ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64" >> Dockerfile
echo. >> Dockerfile
echo # Собираем APK >> Dockerfile
echo RUN buildozer android debug >> Dockerfile

echo.
echo 🏗️ Собираем APK через Docker (это займет 20-30 минут)...
echo Не закрывайте окно во время сборки!
echo.

docker build -t cryptokeyfinder-desktop .

if %errorlevel% equ 0 (
    echo.
    echo 📦 Извлекаем APK из контейнера...
    docker create --name temp-desktop cryptokeyfinder-desktop
    docker cp temp-desktop:/app/bin/. ./bin/ 2>nul
    docker rm temp-desktop
    
    if exist "bin\*.apk" (
        echo.
        echo 🎉 APK УСПЕШНО СОЗДАН ЧЕРЕЗ DOCKER DESKTOP!
        echo 📁 Расположение: bin\
        dir bin\*.apk
        echo.
        echo 📱 ГОТОВ К УСТАНОВКЕ НА ANDROID!
        echo.
        echo 📋 СЛЕДУЮЩИЕ ШАГИ:
        echo 1. Скопируйте APK на Android устройство
        echo 2. Включите "Неизвестные источники" в настройках
        echo 3. Установите APK
        echo 4. Запустите CryptoKeyFinder Mobile
        echo.
    ) else (
        echo ❌ APK не найден в контейнере
        echo Попробуйте GitHub Actions метод
    )
) else (
    echo.
    echo ❌ ОШИБКА СБОРКИ DOCKER
    echo.
    echo 🚀 РЕКОМЕНДАЦИЯ: GITHUB ACTIONS
    echo ==============================
    echo GitHub Actions - самый надежный метод:
    echo 1. Откройте FINAL_APK_SOLUTION.md
    echo 2. Следуйте инструкции
    echo 3. Получите APK за 25 минут
)

echo.
pause