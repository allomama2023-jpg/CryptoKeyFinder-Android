# 🪟 СБОРКА ANDROID APK НА WINDOWS

## ⚠️ ВАЖНО: Buildozer не работает нативно на Windows!

Buildozer предназначен для Linux/Mac систем. Для Windows есть несколько решений:

---

## 🔄 РЕШЕНИЕ 1: WSL (Windows Subsystem for Linux) - РЕКОМЕНДУЕТСЯ

### 1. Установите WSL:
```cmd
wsl --install
```

### 2. Перезагрузите компьютер

### 3. Откройте WSL и установите зависимости:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

### 4. Установите buildozer в WSL:
```bash
pip3 install --user buildozer
```

### 5. Скопируйте файлы проекта в WSL:
```bash
cp -r /mnt/c/Users/Maddog/Desktop/"Новая папка"/CryptoKeyFinder_Android ~/CryptoKeyFinder_Android
cd ~/CryptoKeyFinder_Android
```

### 6. Запустите сборку:
```bash
buildozer android debug
```

---

## 🔄 РЕШЕНИЕ 2: Виртуальная машина с Linux

### 1. Установите VirtualBox или VMware
### 2. Создайте виртуальную машину с Ubuntu 20.04+
### 3. Установите зависимости как в WSL
### 4. Скопируйте файлы проекта
### 5. Соберите APK

---

## 🔄 РЕШЕНИЕ 3: Использование GitHub Actions (Облачная сборка)

Создайте репозиторий на GitHub и используйте автоматическую сборку в облаке.

---

## 🔄 РЕШЕНИЕ 4: Альтернативные инструменты для Windows

### BeeWare Briefcase (Экспериментально):
```cmd
pip install briefcase
briefcase create android
briefcase build android
briefcase package android
```

### Kivy Buildozer Docker:
```cmd
docker run --rm -v "%cd%":/home/user/hostcwd kivy/buildozer android debug
```

---

## 🎯 РЕКОМЕНДАЦИЯ

**Лучший вариант для Windows - использовать WSL.** Это даст вам полноценную Linux среду внутри Windows без необходимости виртуальной машины.

### Пошаговая инструкция для WSL:

1. **Включите WSL:**
   - Откройте PowerShell как администратор
   - Выполните: `wsl --install`
   - Перезагрузите компьютер

2. **Настройте Ubuntu в WSL:**
   - Откройте "Ubuntu" из меню Пуск
   - Создайте пользователя
   - Обновите систему: `sudo apt update && sudo apt upgrade`

3. **Установите зависимости:**
   ```bash
   sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   pip3 install --user buildozer
   ```

4. **Скопируйте проект:**
   ```bash
   cp -r /mnt/c/Users/Maddog/Desktop/"Новая папка"/CryptoKeyFinder_Android ~/
   cd ~/CryptoKeyFinder_Android
   ```

5. **Соберите APK:**
   ```bash
   buildozer android debug
   ```

6. **Найдите APK:**
   APK будет в папке `bin/` и доступен из Windows по пути:
   `\\wsl$\Ubuntu\home\[username]\CryptoKeyFinder_Android\bin\`

---

## 🚀 АЛЬТЕРНАТИВА: ГОТОВЫЙ APK

Если сборка вызывает сложности, я могу предоставить инструкции по созданию APK другими способами или помочь с настройкой WSL.

---

*Обновлено: 30 января 2025*