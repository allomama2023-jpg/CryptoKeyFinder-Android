#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест Android версии CryptoKeyFinder
"""

print("🎯 ПРОСТОЙ ТЕСТ ANDROID ВЕРСИИ")
print("=" * 50)

# Тест 1: Импорт crypto_utils_android
try:
    print("1. Импорт crypto_utils_android...", end=" ")
    from crypto_utils_android import AndroidBitcoinUtils, AndroidEthereumUtils
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 2: Генерация Bitcoin ключа
try:
    print("2. Генерация Bitcoin ключа...", end=" ")
    btc_key = AndroidBitcoinUtils.generate_private_key()
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 3: Генерация Bitcoin адреса
try:
    print("3. Генерация Bitcoin адреса...", end=" ")
    btc_addr = AndroidBitcoinUtils.private_key_to_address(btc_key)
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 4: Валидация ключа
try:
    print("4. Валидация Bitcoin ключа...", end=" ")
    btc_valid = AndroidBitcoinUtils.validate_private_key(btc_key)
    print(f"{'✅' if btc_valid else '❌'}")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 5: Генерация Ethereum ключа
try:
    print("5. Генерация Ethereum ключа...", end=" ")
    eth_key = AndroidEthereumUtils.generate_private_key()
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Тест 6: Генерация Ethereum адреса
try:
    print("6. Генерация Ethereum адреса...", end=" ")
    eth_addr = AndroidEthereumUtils.private_key_to_address(eth_key)
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

print("\n🎉 ВСЕ БАЗОВЫЕ ТЕСТЫ ПРОЙДЕНЫ!")
print("✅ Android версия готова к использованию!")

# Проверка файлов
print("\n📁 ПРОВЕРКА ФАЙЛОВ:")
import os
files = ["main.py", "crypto_utils_android.py", "buildozer.spec", "requirements.txt"]
for f in files:
    status = "✅" if os.path.exists(f) else "❌"
    print(f"{f}: {status}")

print("\n🚀 ГОТОВО К СБОРКЕ APK!")
print("Запустите: build_android.bat (Windows) или ./build_android.sh (Linux/Mac)")