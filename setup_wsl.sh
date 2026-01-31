#!/bin/bash
# Настройка WSL для сборки Android APK

echo "🐧 НАСТРОЙКА WSL ДЛЯ СБОРКИ ANDROID APK"
echo "======================================"

# Обновление системы
echo "1. Обновление системы..."
sudo apt update && sudo apt upgrade -y

# Установка зависимостей
echo "2. Установка зависимостей..."
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    ccache \
    m4 \
    libc6-dev \
    libgmp-dev

# Установка Python зависимостей
echo "3. Установка Python зависимостей..."
pip3 install --user --upgrade pip
pip3 install --user buildozer
pip3 install --user cython
pip3 install --user kivy[base]

# Добавление в PATH
echo "4. Настройка PATH..."
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
export PATH=$PATH:~/.local/bin

# Настройка Java
echo "5. Настройка Java..."
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Проверка установки
echo "6. Проверка установки..."
python3 --version
pip3 --version
buildozer --version

echo "✅ WSL настроен для сборки Android APK!"
echo "Теперь можно собирать APK командой: buildozer android debug"