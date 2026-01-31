#!/bin/bash
# Офлайн сборка APK без интернета

echo "📱 ОФЛАЙН СБОРКА APK БЕЗ ИНТЕРНЕТА"
echo "================================="

echo "Создаем APK используя локальные инструменты..."

# Создаем структуру Android проекта
mkdir -p android_project/app/src/main/java/org/cryptokeyfinder/app
mkdir -p android_project/app/src/main/assets
mkdir -p android_project/app/src/main/res/values

# Копируем Python файлы в assets
cp *.py android_project/app/src/main/assets/

# Создаем AndroidManifest.xml
cat > android_project/app/src/main/AndroidManifest.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.cryptokeyfinder.app">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    
    <application
        android:label="CryptoKeyFinder"
        android:icon="@mipmap/ic_launcher">
        
        <activity android:name=".MainActivity"
            android:label="CryptoKeyFinder"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
EOF

# Создаем strings.xml
cat > android_project/app/src/main/res/values/strings.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">CryptoKeyFinder</string>
</resources>
EOF

# Создаем MainActivity.java
cat > android_project/app/src/main/java/org/cryptokeyfinder/app/MainActivity.java << 'EOF'
package org.cryptokeyfinder.app;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebSettings;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        WebView webView = new WebView(this);
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        
        // Загружаем HTML интерфейс с Python backend
        webView.loadUrl("file:///android_asset/app.html");
        
        setContentView(webView);
    }
}
EOF

# Создаем HTML интерфейс
cat > android_project/app/src/main/assets/app.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CryptoKeyFinder Mobile</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .tab { background: #f1f1f1; padding: 10px; margin: 5px 0; }
        button { padding: 10px 20px; margin: 5px; }
        input, textarea { width: 100%; padding: 10px; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>🔑 CryptoKeyFinder Mobile</h1>
    
    <div class="tab">
        <h2>🔍 Поиск кошельков</h2>
        <select id="crypto">
            <option>Bitcoin</option>
            <option>Ethereum</option>
        </select>
        <button onclick="startSearch()">Начать поиск</button>
        <button onclick="stopSearch()">Остановить</button>
        <textarea id="log" rows="10" readonly>Готов к поиску...</textarea>
    </div>
    
    <div class="tab">
        <h2>🔑 Тест ключа</h2>
        <input type="text" id="privateKey" placeholder="Приватный ключ (64 символа hex)">
        <button onclick="testKey()">Проверить ключ</button>
        <button onclick="generateKey()">Сгенерировать</button>
        <textarea id="results" rows="8" readonly>Результаты появятся здесь...</textarea>
    </div>
    
    <script>
        function startSearch() {
            document.getElementById('log').value += '\nНачинаем поиск кошельков...\n';
            // Здесь будет вызов Python кода через bridge
        }
        
        function stopSearch() {
            document.getElementById('log').value += '\nПоиск остановлен\n';
        }
        
        function testKey() {
            const key = document.getElementById('privateKey').value;
            if (key.length !== 64) {
                alert('Ключ должен содержать 64 символа!');
                return;
            }
            document.getElementById('results').value = 'Проверяем ключ: ' + key.substring(0, 16) + '...\n';
        }
        
        function generateKey() {
            // Генерируем случайный ключ
            const chars = '0123456789abcdef';
            let key = '';
            for (let i = 0; i < 64; i++) {
                key += chars[Math.floor(Math.random() * chars.length)];
            }
            document.getElementById('privateKey').value = key;
        }
    </script>
</body>
</html>
EOF

echo "✅ СТРУКТУРА ANDROID ПРОЕКТА СОЗДАНА!"
echo "📁 Папка: android_project/"
echo
echo "📋 СЛЕДУЮЩИЕ ШАГИ:"
echo "1. Скопируйте папку android_project в Android Studio"
echo "2. Откройте проект в Android Studio"
echo "3. Нажмите Build → Build APK"
echo "4. Получите готовый APK!"
echo
echo "Или используйте готовую Tkinter версию:"
echo "python3 main_tkinter.py"