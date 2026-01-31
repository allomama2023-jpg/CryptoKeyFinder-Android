#!/bin/bash
# Скрипт сборки Android APK для CryptoKeyFinder

echo "🚀 Начинаем сборку CryptoKeyFinder для Android..."

# Проверяем наличие buildozer
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer не установлен!"
    echo "Установите его командой: pip install buildozer"
    exit 1
fi

# Проверяем наличие основных файлов
if [ ! -f "main.py" ]; then
    echo "❌ Файл main.py не найден!"
    exit 1
fi

if [ ! -f "crypto_utils_android.py" ]; then
    echo "❌ Файл crypto_utils_android.py не найден!"
    exit 1
fi

if [ ! -f "buildozer.spec" ]; then
    echo "❌ Файл buildozer.spec не найден!"
    exit 1
fi

echo "✅ Все необходимые файлы найдены"

# Очистка предыдущих сборок
echo "🧹 Очистка предыдущих сборок..."
buildozer android clean

# Инициализация buildozer (если нужно)
echo "🔧 Инициализация buildozer..."
buildozer init

# Сборка APK в debug режиме
echo "📱 Сборка Android APK..."
buildozer android debug

# Проверяем результат
if [ -f "bin/cryptokeyfinder-1.0-arm64-v8a-debug.apk" ] || [ -f "bin/cryptokeyfinder-1.0-armeabi-v7a-debug.apk" ]; then
    echo "🎉 Сборка завершена успешно!"
    echo "📁 APK файлы находятся в папке bin/"
    ls -la bin/*.apk
    
    echo ""
    echo "📋 Инструкции по установке:"
    echo "1. Скопируйте APK файл на Android устройство"
    echo "2. Включите 'Неизвестные источники' в настройках безопасности"
    echo "3. Установите APK файл"
    echo "4. Запустите CryptoKeyFinder Mobile"
    
else
    echo "❌ Ошибка сборки! APK файл не создан."
    echo "Проверьте логи выше для диагностики проблем."
    exit 1
fi

echo "✅ Готово!"