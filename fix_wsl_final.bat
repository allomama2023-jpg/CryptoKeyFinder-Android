@echo off
REM Финальное исправление WSL

echo 🔧 ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ WSL
echo ============================

echo ЗАПУСТИТЕ КАК АДМИНИСТРАТОР!
echo.

echo 1. Полная перезагрузка WSL...
wsl --shutdown
timeout /t 5

echo 2. Исправление сетевых настроек Windows...
netsh winsock reset
netsh int ip reset
ipconfig /flushdns

echo 3. Исправление WSL сети...
netsh interface ip set dns "vEthernet (WSL)" static 8.8.8.8
netsh interface ip add dns "vEthernet (WSL)" 8.8.4.4 index=2

echo 4. Перезапуск сетевых служб...
net stop winnat
net start winnat

echo 5. Запуск WSL с исправлениями...
wsl -d Ubuntu-22.04 bash -c "
sudo rm -f /etc/resolv.conf
echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf
echo 'nameserver 8.8.4.4' | sudo tee -a /etc/resolv.conf
sudo chattr +i /etc/resolv.conf
ping -c 2 google.com
"

if %errorlevel% equ 0 (
    echo ✅ WSL исправлен! Теперь попробуйте сборку APK.
    wsl -d Ubuntu-22.04
) else (
    echo ❌ WSL все еще не работает
    echo Используйте GitHub Actions или Docker методы
)

pause