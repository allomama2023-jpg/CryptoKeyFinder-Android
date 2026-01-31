#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест Tkinter версии CryptoKeyFinder
"""

print("🖥️ ТЕСТ TKINTER ВЕРСИИ CryptoKeyFinder")
print("=" * 50)

# Тест 1: Импорт Tkinter (входит в стандартную библиотеку)
try:
    print("1. Импорт Tkinter...", end=" ")
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 2: Импорт crypto_utils_android
try:
    print("2. Импорт crypto_utils_android...", end=" ")
    from crypto_utils_android import AndroidBitcoinUtils, AndroidEthereumUtils
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 3: Генерация Bitcoin ключа
try:
    print("3. Генерация Bitcoin ключа...", end=" ")
    btc_key = AndroidBitcoinUtils.generate_private_key()
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 4: Генерация Bitcoin адреса
try:
    print("4. Генерация Bitcoin адреса...", end=" ")
    btc_addr = AndroidBitcoinUtils.private_key_to_address(btc_key)
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 5: Генерация Ethereum ключа и адреса
try:
    print("5. Генерация Ethereum ключа и адреса...", end=" ")
    eth_key = AndroidEthereumUtils.generate_private_key()
    eth_addr = AndroidEthereumUtils.private_key_to_address(eth_key)
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 6: Импорт главного приложения
try:
    print("6. Импорт главного приложения...", end=" ")
    from main_tkinter import CryptoKeyFinderTkinter
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Результаты
print("\n📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
print(f"Bitcoin ключ: {btc_key[:16]}...")
print(f"Bitcoin адрес: {btc_addr}")
print(f"Ethereum ключ: {eth_key[:16]}...")
print(f"Ethereum адрес: {eth_addr}")

print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
print("✅ Tkinter версия готова к запуску!")

# Предложение запуска
print("\n🚀 ЗАПУСК ПРИЛОЖЕНИЯ:")
print("Хотите запустить приложение сейчас? (y/n): ", end="")

try:
    choice = input().lower()
    if choice in ['y', 'yes', 'да', 'д']:
        print("\n🖥️ Запускаем Tkinter версию...")
        print("Закройте окно приложения для завершения.")
        print("=" * 50)
        
        app = CryptoKeyFinderTkinter()
        app.run()
        
        print("\n✅ Приложение закрыто успешно!")
    else:
        print("\n📋 Для запуска в любое время используйте:")
        print("python main_tkinter.py")
        
except KeyboardInterrupt:
    print("\n\n👋 До свидания!")
except Exception as e:
    print(f"\n❌ Ошибка запуска: {e}")

print("\n✅ Тест завершен!")
input("Нажмите Enter для выхода...")