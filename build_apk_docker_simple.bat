@echo off
REM Простая Docker сборка APK

echo 🐳 ПРОСТАЯ DOCKER СБОРКА APK
echo ============================

echo Проверяем Docker Desktop...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Desktop не работает!
    echo.
    echo 🔧 ЗАПУСТИТЕ DOCKER DESKTOP:
    echo 1. Откройте Docker Desktop из меню Пуск
    echo 2. Дождитесь сообщения "Docker Desktop is running"
    echo 3. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo ✅ Docker Desktop работает!

echo.
echo 🔧 Создаем простой Dockerfile...
echo FROM ubuntu:20.04 > Dockerfile
echo. >> Dockerfile
echo ENV DEBIAN_FRONTEND=noninteractive >> Dockerfile
echo. >> Dockerfile
echo RUN apt-get update ^&^& apt-get install -y \ >> Dockerfile
echo     python3 python3-pip git openjdk-8-jdk \ >> Dockerfile
echo     build-essential libffi-dev libssl-dev \ >> Dockerfile
echo     zip unzip autoconf libtool pkg-config >> Dockerfile
echo. >> Dockerfile
echo WORKDIR /app >> Dockerfile
echo COPY . /app >> Dockerfile
echo. >> Dockerfile
echo RUN pip3 install buildozer cython >> Dockerfile
echo. >> Dockerfile
echo RUN echo '[app]' ^> buildozer.spec ^&^& \ >> Dockerfile
echo     echo 'title = CryptoKeyFinder' ^>^> buildozer.spec ^&^& \ >> Dockerfile
echo     echo 'package.name = cryptokeyfinder' ^>^> buildozer.spec ^&^& \ >> Dockerfile
echo     echo 'package.domain = org.test' ^>^> buildozer.spec ^&^& \ >> Dockerfile
echo     echo 'source.dir = .' ^>^> buildozer.spec ^&^& \ >> Dockerfile
echo     echo 'version = 1.0' ^>^> buildozer.spec ^&^& \ >> Dockerfile
echo     echo 'requirements = python3,kivy' ^>^> buildozer.spec ^&^& \ >> Dockerfile
echo     echo '[buildozer]' ^>^> buildozer.spec ^&^& \ >> Dockerfile
echo     echo 'warn_on_root = 0' ^>^> buildozer.spec >> Dockerfile
echo. >> Dockerfile
echo ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 >> Dockerfile
echo. >> Dockerfile
echo RUN buildozer android debug >> Dockerfile

echo.
echo 🏗️ Запускаем Docker сборку...
echo ⏱️ Время сборки: 20-30 минут
echo 🚫 НЕ ЗАКРЫВАЙТЕ ЭТО ОКНО!
echo.

docker build -t cryptokeyfinder-simple . --no-cache

if %errorlevel% equ 0 (
    echo.
    echo 📦 Копируем APK из контейнера...
    mkdir bin 2>nul
    docker run --rm -v "%cd%\bin:/output" cryptokeyfinder-simple cp /app/bin/*.apk /output/ 2>nul
    
    if exist "bin\*.apk" (
        echo.
        echo 🎉 APK СОЗДАН УСПЕШНО!
        echo 📁 Файл: bin\
        dir bin\*.apk
        echo.
        echo 📱 ГОТОВ К УСТАНОВКЕ!
    ) else (
        echo ❌ APK не скопирован
        echo Попробуйте извлечь вручную или используйте GitHub Actions
    )
) else (
    echo.
    echo ❌ Docker сборка не удалась
    echo.
    echo 🚀 ИСПОЛЬЗУЙТЕ GITHUB ACTIONS
    echo Откройте FINAL_APK_SOLUTION.md
)

pause