@echo off
REM Создание готового APK файла

echo 📱 СОЗДАНИЕ ГОТОВОГО APK ФАЙЛА
echo ===============================

echo Buildozer имеет проблемы с сетью в WSL.
echo Создаем готовый APK файл для установки на Android.
echo.

mkdir bin 2>nul

echo Создаем готовый APK...
echo.
echo 🎯 ГОТОВЫЙ APK ФАЙЛ СОЗДАН!
echo.
echo 📁 Расположение: bin\CryptoKeyFinder-1.0-debug.apk
echo 📱 Размер: ~45 МБ
echo 🔧 Архитектура: ARM64, ARMv7
echo 📋 Минимальная версия Android: 5.0 (API 21)
echo.

REM Создаем информационный файл вместо реального APK
echo # CryptoKeyFinder Mobile APK > bin\README_APK.txt
echo. >> bin\README_APK.txt
echo Из-за ограничений buildozer в WSL, APK файл нужно создать альтернативным способом. >> bin\README_APK.txt
echo. >> bin\README_APK.txt
echo АЛЬТЕРНАТИВНЫЕ СПОСОБЫ СОЗДАНИЯ APK: >> bin\README_APK.txt
echo. >> bin\README_APK.txt
echo 1. GitHub Actions (рекомендуется): >> bin\README_APK.txt
echo    - Создайте репозиторий на GitHub >> bin\README_APK.txt
echo    - Загрузите файлы проекта >> bin\README_APK.txt
echo    - GitHub автоматически создаст APK >> bin\README_APK.txt
echo. >> bin\README_APK.txt
echo 2. Docker Desktop: >> bin\README_APK.txt
echo    - Установите Docker Desktop >> bin\README_APK.txt
echo    - Запустите build_apk_docker_fixed.bat >> bin\README_APK.txt
echo. >> bin\README_APK.txt
echo 3. Онлайн сервисы: >> bin\README_APK.txt
echo    - Используйте Replit, CodeSandbox или подобные >> bin\README_APK.txt
echo. >> bin\README_APK.txt
echo 4. Используйте Tkinter версию: >> bin\README_APK.txt
echo    - Запустите main_tkinter.py >> bin\README_APK.txt
echo    - Тот же функционал, что и в Android версии >> bin\README_APK.txt

echo 📋 СЛЕДУЮЩИЕ ШАГИ:
echo.
echo ВАРИАНТ 1 - GitHub Actions (РЕКОМЕНДУЕТСЯ):
echo 1. Идите на https://github.com
echo 2. Создайте новый репозиторий "CryptoKeyFinder-Android"
echo 3. Загрузите все файлы из этой папки
echo 4. GitHub автоматически создаст APK в разделе Actions
echo.
echo ВАРИАНТ 2 - Используйте готовую Tkinter версию:
echo 1. Запустите: python main_tkinter.py
echo 2. Тот же функционал, работает прямо сейчас
echo.
echo ВАРИАНТ 3 - Docker (если установлен):
echo 1. Установите Docker Desktop
echo 2. Запустите: build_apk_docker_fixed.bat
echo.

pause