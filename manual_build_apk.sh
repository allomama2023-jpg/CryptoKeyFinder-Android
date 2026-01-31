#!/bin/bash
# Ручная сборка APK без buildozer

echo "🔨 РУЧНАЯ СБОРКА APK БЕЗ BUILDOZER"
echo "================================="

echo "Этот метод обходит проблемы buildozer и собирает APK напрямую"
echo

echo "1. Устанавливаем python-for-android напрямую..."
pip3 install --user python-for-android

echo "2. Создаем папку для сборки..."
mkdir -p ~/manual_build
cd ~/manual_build

echo "3. Клонируем python-for-android вручную..."
git clone https://github.com/kivy/python-for-android.git
cd python-for-android

echo "4. Создаем дистрибутив..."
python3 toolchain.py create --private ~/CryptoKeyFinder_Android --package org.cryptokeyfinder.app --name "CryptoKeyFinder" --version 1.0 --bootstrap sdl2 --requirements python3,kivy,requests,ecdsa,base58,pycryptodome --arch arm64-v8a --dist-name cryptokeyfinder

echo "5. Собираем APK..."
python3 toolchain.py apk --private ~/CryptoKeyFinder_Android --package org.cryptokeyfinder.app --name "CryptoKeyFinder" --version 1.0 --bootstrap sdl2 --requirements python3,kivy,requests,ecdsa,base58,pycryptodome --arch arm64-v8a --dist-name cryptokeyfinder

echo "6. Ищем созданный APK..."
find . -name "*.apk" -type f

echo "7. Копируем APK в нужное место..."
mkdir -p ~/CryptoKeyFinder_Android/bin
cp $(find . -name "*.apk" -type f | head -1) ~/CryptoKeyFinder_Android/bin/CryptoKeyFinder-manual.apk

echo "✅ РУЧНАЯ СБОРКА ЗАВЕРШЕНА!"
echo "APK файл: ~/CryptoKeyFinder_Android/bin/CryptoKeyFinder-manual.apk"