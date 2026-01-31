@echo off
REM Исправленная Docker сборка с интерактивным режимом

echo 🐳 ИСПРАВЛЕННАЯ DOCKER СБОРКА APK
echo =================================

echo Создаем исправленный Dockerfile...
echo FROM kivy/buildozer:latest > Dockerfile
echo WORKDIR /app >> Dockerfile
echo COPY . /app >> Dockerfile
echo RUN echo 'y' ^| buildozer android debug >> Dockerfile

echo.
echo Собираем APK с автоматическим подтверждением...
docker build -t cryptokeyfinder-fixed .

echo.
echo Извлекаем APK из контейнера...
docker create --name temp-apk-fixed cryptokeyfinder-fixed
docker cp temp-apk-fixed:/app/bin/. ./bin/ 2>nul
docker rm temp-apk-fixed

echo.
if exist "bin\*.apk" (
    echo 🎉 APK УСПЕШНО СОЗДАН!
    echo 📁 Расположение: bin\
    dir bin\*.apk
) else (
    echo ❌ APK не создан через Docker
    echo Попробуем альтернативный метод...
    call :alternative_method
)

pause
exit /b

:alternative_method
echo.
echo 🚀 АЛЬТЕРНАТИВНЫЙ МЕТОД - ИНТЕРАКТИВНЫЙ DOCKER
echo =============================================
echo Запускаем Docker в интерактивном режиме...

docker run -it --rm -v "%cd%":/app -w /app kivy/buildozer bash -c "
echo 'Настраиваем buildozer для работы с root...'
export BUILDOZER_WARN_ON_ROOT=0
sed -i 's/warn_on_root = 1/warn_on_root = 0/g' buildozer.spec
echo 'y' | buildozer android debug
"

if exist "bin\*.apk" (
    echo 🎉 APK СОЗДАН АЛЬТЕРНАТИВНЫМ МЕТОДОМ!
    dir bin\*.apk
) else (
    echo ❌ Docker методы не работают
    echo Используйте GitHub Actions - это самый надежный способ
)
goto :eof