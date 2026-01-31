@echo off
REM Docker сборка без предупреждений root

echo 🐳 DOCKER СБОРКА БЕЗ ROOT ПРЕДУПРЕЖДЕНИЙ
echo =========================================

echo Создаем оптимизированный buildozer.spec...
echo [app] > buildozer_docker.spec
echo title = CryptoKeyFinder Mobile >> buildozer_docker.spec
echo package.name = cryptokeyfinder >> buildozer_docker.spec
echo package.domain = org.cryptokeyfinder >> buildozer_docker.spec
echo source.dir = . >> buildozer_docker.spec
echo source.include_exts = py,png,jpg,kv,atlas,txt,md >> buildozer_docker.spec
echo version = 1.0 >> buildozer_docker.spec
echo requirements = python3,kivy,requests,ecdsa,base58,pycryptodome >> buildozer_docker.spec
echo orientation = portrait >> buildozer_docker.spec
echo fullscreen = 0 >> buildozer_docker.spec
echo. >> buildozer_docker.spec
echo [buildozer] >> buildozer_docker.spec
echo log_level = 2 >> buildozer_docker.spec
echo warn_on_root = 0 >> buildozer_docker.spec
echo build_dir = ./.buildozer >> buildozer_docker.spec
echo bin_dir = ./bin >> buildozer_docker.spec
echo. >> buildozer_docker.spec
echo android.api = 30 >> buildozer_docker.spec
echo android.minapi = 21 >> buildozer_docker.spec
echo android.ndk = 23b >> buildozer_docker.spec
echo android.sdk = 30 >> buildozer_docker.spec
echo android.archs = arm64-v8a >> buildozer_docker.spec
echo android.allow_backup = True >> buildozer_docker.spec
echo android.release_artifact = apk >> buildozer_docker.spec
echo android.debug_artifact = apk >> buildozer_docker.spec
echo android.accept_sdk_license = True >> buildozer_docker.spec

echo.
echo Создаем Dockerfile без root предупреждений...
echo FROM kivy/buildozer:latest > Dockerfile
echo WORKDIR /app >> Dockerfile
echo COPY . /app >> Dockerfile
echo ENV BUILDOZER_WARN_ON_ROOT=0 >> Dockerfile
echo RUN cp buildozer_docker.spec buildozer.spec >> Dockerfile
echo RUN buildozer android debug >> Dockerfile

echo.
echo Собираем APK без предупреждений...
docker build -t cryptokeyfinder-noroot .

echo.
echo Извлекаем APK...
docker create --name temp-noroot cryptokeyfinder-noroot
docker cp temp-noroot:/app/bin/. ./bin/ 2>nul
docker rm temp-noroot

echo.
if exist "bin\*.apk" (
    echo 🎉 APK УСПЕШНО СОЗДАН БЕЗ ПРЕДУПРЕЖДЕНИЙ!
    echo 📁 Расположение: bin\
    dir bin\*.apk
    echo.
    echo 📱 ГОТОВ К УСТАНОВКЕ НА ANDROID!
) else (
    echo ❌ Ошибка создания APK
    echo.
    echo 🚀 РЕКОМЕНДАЦИЯ: GITHUB ACTIONS
    echo ==============================
    echo GitHub Actions - самый надежный метод:
    echo 1. Откройте CREATE_APK_GITHUB.md
    echo 2. Следуйте инструкции
    echo 3. Получите APK за 25 минут
)

pause