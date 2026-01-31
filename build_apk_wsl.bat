@echo off
REM Автоматическая настройка WSL и сборка Android APK

echo 🤖 АВТОМАТИЧЕСКАЯ СБОРКА ANDROID APK ЧЕРЕЗ WSL
echo ================================================

echo 1. Проверяем наличие WSL...
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ WSL не установлен!
    echo.
    echo 📥 УСТАНОВКА WSL:
    echo Выполните следующие команды как администратор:
    echo.
    echo 1. Откройте PowerShell как администратор
    echo 2. Выполните: wsl --install
    echo 3. Перезагрузите компьютер
    echo 4. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo ✅ WSL найден!

echo.
echo 2. Проверяем наличие Ubuntu в WSL...
wsl -l -v | findstr Ubuntu >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ubuntu не установлен в WSL!
    echo.
    echo 🚀 АВТОМАТИЧЕСКАЯ УСТАНОВКА UBUNTU:
    echo Запускаем автоматическую установку Ubuntu 22.04 LTS...
    
    REM Попытка автоматической установки
    wsl --install -d Ubuntu-22.04
    
    if %errorlevel% equ 0 (
        echo ✅ Ubuntu установлен!
        echo ⚠️  ТРЕБУЕТСЯ ПЕРЕЗАГРУЗКА!
        echo.
        echo СЛЕДУЮЩИЕ ШАГИ:
        echo 1. Перезагрузите компьютер
        echo 2. Запустите Ubuntu из меню Пуск
        echo 3. Создайте пользователя и пароль
        echo 4. Запустите этот скрипт снова
        echo.
        pause
        exit /b 0
    ) else (
        echo ❌ Автоматическая установка не удалась
        echo.
        echo 📥 РУЧНАЯ УСТАНОВКА UBUNTU:
        echo 1. Откройте Microsoft Store
        echo 2. Найдите "Ubuntu 22.04 LTS"
        echo 3. Установите Ubuntu
        echo 4. Запустите Ubuntu и создайте пользователя
        echo 5. Запустите этот скрипт снова
        echo.
        echo Или запустите: install_ubuntu_step_by_step.bat
        pause
        exit /b 1
    )
)

echo ✅ Ubuntu найден в WSL!

echo.
echo 2.1. Проверяем готовность Ubuntu...
wsl -d Ubuntu-22.04 echo "Ubuntu готов" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ubuntu не настроен!
    echo.
    echo 🔧 НАСТРОЙКА UBUNTU:
    echo 1. Запустите Ubuntu из меню Пуск
    echo 2. Создайте имя пользователя и пароль
    echo 3. Дождитесь завершения настройки
    echo 4. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo ✅ Ubuntu готов к работе!

echo.
echo 3. Копируем файлы проекта в WSL...
wsl mkdir -p ~/CryptoKeyFinder_Android
wsl cp -r /mnt/c/Users/Maddog/Desktop/"Новая папка"/CryptoKeyFinder_Android/* ~/CryptoKeyFinder_Android/ 2>nul

echo.
echo 4. Устанавливаем зависимости в WSL...
wsl bash -c "cd ~/CryptoKeyFinder_Android && chmod +x setup_wsl.sh && ./setup_wsl.sh"

echo.
echo 5. ИСПРАВЛЯЕМ ПРОБЛЕМЫ BUILDOZER...
wsl bash -c "cd ~/CryptoKeyFinder_Android && chmod +x fix_buildozer_network.sh && ./fix_buildozer_network.sh"

echo.
echo 6. Собираем APK с исправлениями...
wsl bash -c "cd ~/CryptoKeyFinder_Android && chmod +x build_apk_fixed.sh && ./build_apk_fixed.sh"

echo.
echo 7. АЛЬТЕРНАТИВНАЯ СБОРКА (если основная не работает)...
echo Если основная сборка не удалась, попробуем ручную сборку...
wsl bash -c "cd ~/CryptoKeyFinder_Android && chmod +x manual_build_apk.sh && ./manual_build_apk.sh"

echo.
echo 6. Копируем APK обратно в Windows...
wsl cp ~/CryptoKeyFinder_Android/bin/*.apk /mnt/c/Users/Maddog/Desktop/"Новая папка"/CryptoKeyFinder_Android/ 2>nul

echo.
if exist "*.apk" (
    echo 🎉 APK УСПЕШНО СОЗДАН!
    echo 📁 Файл APK находится в текущей папке
    dir *.apk
    echo.
    echo 📱 УСТАНОВКА НА ANDROID:
    echo 1. Скопируйте APK на Android устройство
    echo 2. Включите "Неизвестные источники" в настройках
    echo 3. Установите APK
    echo.
) else (
    echo ❌ Ошибка создания APK!
    echo Проверьте логи WSL выше
)

pause