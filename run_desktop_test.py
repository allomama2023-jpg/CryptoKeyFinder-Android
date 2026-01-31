#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый запуск Android версии на десктопе
Для проверки функциональности перед сборкой APK
"""

import os
import sys

print("🖥️ ТЕСТОВЫЙ ЗАПУСК ANDROID ВЕРСИИ НА ДЕСКТОПЕ")
print("=" * 60)
print("Это позволит протестировать приложение перед сборкой APK")
print("=" * 60)

# Проверяем наличие Kivy
try:
    import kivy
    print(f"✅ Kivy установлен (версия {kivy.__version__})")
except ImportError:
    print("❌ Kivy не установлен!")
    print("Установите командой: pip install kivy")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

# Проверяем наличие других зависимостей
dependencies = [
    ("requests", "requests"),
    ("ecdsa", "ecdsa"),
    ("base58", "base58"),
    ("pycryptodome", "Crypto")
]

missing_deps = []

for dep_name, import_name in dependencies:
    try:
        __import__(import_name)
        print(f"✅ {dep_name} установлен")
    except ImportError:
        print(f"⚠️ {dep_name} не установлен (будет использован fallback режим)")
        missing_deps.append(dep_name)

if missing_deps:
    print(f"\n📦 Для полной функциональности установите:")
    for dep in missing_deps:
        print(f"   pip install {dep}")
    print("\nПриложение будет работать в упрощенном режиме.")

# Проверяем наличие файлов
required_files = ["main.py", "crypto_utils_android.py"]
missing_files = []

for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file} найден")
    else:
        print(f"❌ {file} не найден!")
        missing_files.append(file)

if missing_files:
    print(f"\n❌ Отсутствуют необходимые файлы: {missing_files}")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

print("\n🚀 Запускаем Android версию на десктопе...")
print("Закройте окно приложения для завершения.")
print("=" * 60)

# Запускаем приложение
try:
    from main import CryptoKeyFinderApp
    app = CryptoKeyFinderApp()
    app.run()
except Exception as e:
    print(f"\n❌ Ошибка запуска приложения: {e}")
    print("\nВозможные причины:")
    print("1. Не установлены зависимости")
    print("2. Ошибка в коде приложения")
    print("3. Проблемы с Kivy")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

print("\n✅ Приложение закрыто успешно!")
input("Нажмите Enter для выхода...")