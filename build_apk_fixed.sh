#!/bin/bash
# Полная сборка APK с исправлениями всех проблем

echo "🚀 ПОЛНАЯ СБОРКА APK С ИСПРАВЛЕНИЯМИ"
echo "==================================="

# Функция для повторных попыток
retry_command() {
    local cmd="$1"
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Попытка $attempt/$max_attempts: $cmd"
        if eval "$cmd"; then
            echo "✅ Команда выполнена успешно!"
            return 0
        else
            echo "❌ Попытка $attempt не удалась"
            if [ $attempt -lt $max_attempts ]; then
                echo "Ждем 15 секунд перед следующей попыткой..."
                sleep 15
            fi
            ((attempt++))
        fi
    done
    
    echo "❌ Все попытки исчерпаны для: $cmd"
    return 1
}

echo "1. Исправляем сетевые проблемы..."
chmod +x fix_buildozer_network.sh
./fix_buildozer_network.sh

echo "2. Переходим в папку проекта..."
cd ~/CryptoKeyFinder_Android

echo "3. Проверяем зависимости..."
python3 -c "import kivy; print('Kivy:', kivy.__version__)"
buildozer --version

echo "4. Инициализируем buildozer с исправлениями..."
retry_command "buildozer init"

echo "5. Запускаем сборку APK с подробными логами..."
export BUILDOZER_LOG_LEVEL=2
export JAVA_OPTS='-XX:+IgnoreUnrecognizedVMOptions --add-modules java.se.ee'

# Сборка с повторными попытками
retry_command "buildozer android debug"

echo "6. Проверяем результат..."
if [ -f "bin/*.apk" ]; then
    echo "🎉 APK УСПЕШНО СОЗДАН!"
    ls -la bin/
    
    echo "7. Копируем APK в Windows..."
    cp bin/*.apk /mnt/c/Users/Maddog/Desktop/Новая\ папка/CryptoKeyFinder_Android/
    
    echo "✅ APK готов к установке на Android!"
    echo "📁 Расположение: bin/ и в папке Windows"
else
    echo "❌ APK не создан. Проверьте логи выше."
    echo "Попробуйте запустить команды по отдельности:"
    echo "1. ./fix_buildozer_network.sh"
    echo "2. buildozer android debug -v"
fi