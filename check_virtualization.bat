@echo off
REM Проверка поддержки виртуализации

echo 🔍 ПРОВЕРКА ПОДДЕРЖКИ ВИРТУАЛИЗАЦИИ
echo ===================================

echo 1. Проверяем поддержку Hyper-V...
systeminfo | findstr /C:"Hyper-V"

echo.
echo 2. Проверяем процессор...
wmic cpu get name,virtualizationfirmwareenabled

echo.
echo 3. Проверяем компоненты Windows...
dism /online /get-features | findstr -i "subsystem\|virtual\|hyper"

echo.
echo 4. Проверяем WSL...
wsl --status

echo.
echo 📋 ИНТЕРПРЕТАЦИЯ РЕЗУЛЬТАТОВ:
echo ============================
echo ✅ Если "VirtualizationFirmwareEnabled: TRUE" - виртуализация включена в BIOS
echo ❌ Если "VirtualizationFirmwareEnabled: FALSE" - нужно включить в BIOS
echo.
echo ✅ Если компоненты "Enabled" - Windows компоненты включены
echo ❌ Если компоненты "Disabled" - нужно включить компоненты
echo.

pause