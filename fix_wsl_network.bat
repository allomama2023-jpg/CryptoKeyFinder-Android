@echo off
REM Исправление сетевых проблем WSL

echo 🌐 ИСПРАВЛЕНИЕ СЕТЕВЫХ ПРОБЛЕМ WSL
echo ==================================

echo Запустите этот файл как АДМИНИСТРАТОР!
echo.

echo 1. Перезапускаем WSL...
wsl --shutdown
timeout /t 5

echo 2. Исправляем DNS в Windows...
netsh interface ip set dns "vEthernet (WSL)" static 8.8.8.8
netsh interface ip add dns "vEthernet (WSL)" 8.8.4.4 index=2

echo 3. Перезапускаем сетевые службы...
net stop winnat
net start winnat

echo 4. Запускаем WSL снова...
wsl -d Ubuntu-22.04

echo ✅ WSL перезапущен с исправленной сетью!
echo Теперь попробуйте команды в Ubuntu снова.

pause