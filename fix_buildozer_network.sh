#!/bin/bash
# Исправление сетевых проблем buildozer в WSL

echo "🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМ BUILDOZER В WSL"
echo "===================================="

echo "1. Настройка DNS для WSL..."
# Исправляем DNS проблемы WSL
sudo rm -f /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
echo "nameserver 8.8.4.4" | sudo tee -a /etc/resolv.conf
echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf

echo "2. Настройка git для работы с GitHub..."
git config --global http.version HTTP/1.1
git config --global http.postBuffer 157286400
git config --global http.maxRequestBuffer 100M
git config --global core.compression 0
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999

echo "3. Тестируем подключение к GitHub..."
ping -c 3 github.com
curl -I https://github.com/kivy/python-for-android.git

echo "4. Очищаем кеш buildozer..."
rm -rf ~/.buildozer
rm -rf .buildozer

echo "5. Создаем оптимизированный buildozer.spec..."
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
log_level = 2
warn_on_root = 0
build_dir = ./.buildozer
bin_dir = ./bin

# Android specific - оптимизированные настройки
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30
android.archs = arm64-v8a
android.allow_backup = True
android.release_artifact = apk
android.debug_artifact = apk

# Сетевые оптимизации
android.gradle_dependencies = 
android.add_src = 
android.add_aars = 
android.add_jars = 
android.add_libs_armeabi_v7a = 
android.add_libs_arm64_v8a = 
android.add_libs_x86 = 
android.add_libs_mips = 

# Исправления для WSL
android.accept_sdk_license = True
android.skip_update = False
android.auto_last_revision = False
EOF

echo "6. Настройка переменных окружения..."
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export ANDROID_HOME=$HOME/.buildozer/android/platform/android-sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:~/.local/bin

echo "7. Предварительная загрузка python-for-android..."
cd ~/.buildozer
mkdir -p android/platform
cd android/platform

# Клонируем репозиторий вручную с retry логикой
for i in {1..5}; do
    echo "Попытка $i/5 клонирования python-for-android..."
    if git clone --depth 1 -b master https://github.com/kivy/python-for-android.git; then
        echo "✅ python-for-android успешно клонирован!"
        break
    else
        echo "❌ Попытка $i не удалась, ждем 10 секунд..."
        sleep 10
    fi
done

echo "✅ BUILDOZER НАСТРОЕН ДЛЯ WSL!"
echo "Теперь можно запускать: buildozer android debug"