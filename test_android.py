#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест Android версии CryptoKeyFinder
Проверяем работу всех компонентов
"""

import sys
import os

def test_imports():
    """Тест импорта всех модулей"""
    print("🧪 ТЕСТ ИМПОРТА МОДУЛЕЙ")
    print("=" * 40)
    
    try:
        print("Импорт crypto_utils_android...", end=" ")
        from crypto_utils_android import AndroidBitcoinUtils, AndroidEthereumUtils, AndroidCryptoScanner
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    try:
        print("Импорт Kivy...", end=" ")
        import kivy
        print(f"✅ (версия {kivy.__version__})")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    try:
        print("Импорт requests...", end=" ")
        import requests
        print(f"✅ (версия {requests.__version__})")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    return True

def test_crypto_functions():
    """Тест криптографических функций"""
    print("\n🔐 ТЕСТ КРИПТОГРАФИЧЕСКИХ ФУНКЦИЙ")
    print("=" * 40)
    
    try:
        from crypto_utils_android import AndroidBitcoinUtils, AndroidEthereumUtils
        
        # Тест Bitcoin
        print("Bitcoin генерация ключа...", end=" ")
        btc_key = AndroidBitcoinUtils.generate_private_key()
        print("✅")
        
        print("Bitcoin генерация адреса...", end=" ")
        btc_addr = AndroidBitcoinUtils.private_key_to_address(btc_key)
        print("✅")
        
        print("Bitcoin валидация ключа...", end=" ")
        btc_valid = AndroidBitcoinUtils.validate_private_key(btc_key)
        print(f"{'✅' if btc_valid else '❌'}")
        
        # Тест Ethereum
        print("Ethereum генерация ключа...", end=" ")
        eth_key = AndroidEthereumUtils.generate_private_key()
        print("✅")
        
        print("Ethereum генерация адреса...", end=" ")
        eth_addr = AndroidEthereumUtils.private_key_to_address(eth_key)
        print("✅")
        
        print("Ethereum валидация ключа...", end=" ")
        eth_valid = AndroidEthereumUtils.validate_private_key(eth_key)
        print(f"{'✅' if eth_valid else '❌'}")
        
        print(f"\nПримеры результатов:")
        print(f"Bitcoin ключ: {btc_key[:16]}...")
        print(f"Bitcoin адрес: {btc_addr}")
        print(f"Ethereum ключ: {eth_key[:16]}...")
        print(f"Ethereum адрес: {eth_addr}")
        
        return btc_valid and eth_valid
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_app_creation():
    """Тест создания приложения"""
    print("\n📱 ТЕСТ СОЗДАНИЯ ПРИЛОЖЕНИЯ")
    print("=" * 40)
    
    try:
        print("Импорт главного приложения...", end=" ")
        from main import CryptoKeyFinderApp
        print("✅")
        
        print("Создание экземпляра приложения...", end=" ")
        app = CryptoKeyFinderApp()
        print("✅")
        
        print("Проверка атрибутов приложения...", end=" ")
        assert hasattr(app, 'title')
        assert hasattr(app, 'is_running')
        assert hasattr(app, 'found_wallets_list')
        print("✅")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_file_structure():
    """Тест структуры файлов"""
    print("\n📁 ТЕСТ СТРУКТУРЫ ФАЙЛОВ")
    print("=" * 40)
    
    required_files = [
        "main.py",
        "crypto_utils_android.py",
        "buildozer.spec",
        "requirements.txt",
        "build_android.sh",
        "build_android.bat"
    ]
    
    all_present = True
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"{filename}: ✅")
        else:
            print(f"{filename}: ❌")
            all_present = False
    
    return all_present

def test_buildozer_config():
    """Тест конфигурации buildozer"""
    print("\n⚙️ ТЕСТ КОНФИГУРАЦИИ BUILDOZER")
    print("=" * 40)
    
    try:
        with open("buildozer.spec", "r", encoding="utf-8") as f:
            content = f.read()
        
        checks = [
            ("title = CryptoKeyFinder Mobile", "Название приложения"),
            ("package.name = cryptokeyfinder", "Имя пакета"),
            ("requirements = python3,kivy,requests,ecdsa,base58,pycryptodome", "Зависимости"),
            ("android.api = 33", "Android API"),
            ("android.minapi = 21", "Минимальный API")
        ]
        
        all_good = True
        
        for check, description in checks:
            if check in content:
                print(f"{description}: ✅")
            else:
                print(f"{description}: ❌")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Ошибка чтения buildozer.spec: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🎯 ТЕСТ ANDROID ВЕРСИИ CryptoKeyFinder")
    print("=" * 50)
    
    tests = [
        ("Импорт модулей", test_imports),
        ("Криптографические функции", test_crypto_functions),
        ("Создание приложения", test_app_creation),
        ("Структура файлов", test_file_structure),
        ("Конфигурация buildozer", test_buildozer_config)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 Ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    # Итоговый отчет
    print("\n" + "=" * 50)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nПройдено тестов: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("✅ Android версия готова к сборке!")
        print("\n📋 Следующие шаги:")
        print("1. Установите buildozer: pip install buildozer")
        print("2. Запустите сборку: ./build_android.sh (Linux/Mac) или build_android.bat (Windows)")
        print("3. Установите APK на Android устройство")
        return True
    else:
        print(f"\n⚠️ НЕ ВСЕ ТЕСТЫ ПРОЙДЕНЫ: {total-passed} ошибок")
        print("❌ Исправьте ошибки перед сборкой!")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
        sys.exit(1)