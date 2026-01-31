@echo off
REM Сборка APK через WSL с включенной виртуализацией

echo 🚀 СБОРКА APK ЧЕРЕЗ WSL (ВИРТУАЛИЗАЦИЯ ВКЛЮЧЕНА)
echo ================================================

echo Виртуализация включена - WSL должен работать лучше!
echo.

echo 1. Перезапускаем WSL для применения виртуализации...
wsl --shutdown
timeout /t 3

echo 2. Запускаем Ubuntu с исправлениями...
wsl -d Ubuntu-22.04 bash -c "
echo '🔧 Исправляем сеть и DNS...'
sudo rm -f /etc/resolv.conf
echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf
echo 'nameserver 8.8.4.4' | sudo tee -a /etc/resolv.conf
echo 'nameserver 1.1.1.1' | sudo tee -a /etc/resolv.conf
sudo chattr +i /etc/resolv.conf

echo '📡 Тестируем подключение...'
ping -c 2 google.com

if [ \$? -eq 0 ]; then
    echo '✅ Интернет работает!'
    
    echo '📁 Копируем проект...'
    mkdir -p ~/CryptoKeyFinder_Android
    cp -r /mnt/c/Users/Maddog/Desktop/Новая\ папка/CryptoKeyFinder_Android/* ~/CryptoKeyFinder_Android/
    cd ~/CryptoKeyFinder_Android
    
    echo '🔧 Создаем оптимизированный buildozer.spec...'
    cat > buildozer.spec << 'EOF'
[app]
title = CryptoKeyFinder Mobile
package.name = cryptokeyfinder
package.domain = org.cryptokeyfinder
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,md
version = 1.0
requirements = python3,kivy,requests,ecdsa,base58,pycryptodome
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 1
warn_on_root = 0
build_dir = ./.buildozer
bin_dir = ./bin

android.api = 28
android.minapi = 21
android.ndk = 21b
android.sdk = 28
android.archs = arm64-v8a
android.allow_backup = True
android.release_artifact = apk
android.debug_artifact = apk
android.accept_sdk_license = True
EOF
    
    echo '🛠️ Устанавливаем зависимости...'
    pip3 install --user --upgrade pip
    pip3 install --user buildozer cython
    
    echo '🏗️ Собираем APK...'
    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
    export PATH=\$PATH:~/.local/bin
    ~/.local/bin/buildozer android debug
    
    if [ -f bin/*.apk ]; then
        echo '🎉 APK СОЗДАН УСПЕШНО!'
        ls -la bin/
        cp bin/*.apk /mnt/c/Users/Maddog/Desktop/Новая\ папка/CryptoKeyFinder_Android/
        echo '📱 APK скопирован в Windows папку!'
    else
        echo '❌ APK не создан'
    fi
else
    echo '❌ Интернет не работает в WSL'
    echo 'Используйте GitHub Actions'
fi
"

echo.
if exist "*.apk" (
    echo 🎉 APK ГОТОВ!
    dir *.apk
    echo.
    echo 📱 УСТАНОВКА НА ANDROID:
    echo 1. Скопируйте APK на Android устройство
    echo 2. Включите "Неизвестные источники"
    echo 3. Установите APK
) else (
    echo ❌ APK не создан через WSL
    echo.
    echo 🚀 ИСПОЛЬЗУЙТЕ GITHUB ACTIONS
    echo ============================
    echo Это самый надежный метод!
    echo Откройте CREATE_APK_GITHUB.md
)

pause