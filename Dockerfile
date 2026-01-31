# Используем специальный образ для Android сборки 
FROM cimg/android:2023.12 
 
# Устанавливаем рабочую директорию 
WORKDIR /app 
 
# Копируем файлы проекта 
COPY . /app 
 
# Устанавливаем Python зависимости 
RUN sudo apt-get update && sudo apt-get install -y python3-pip 
RUN pip3 install --user buildozer cython 
 
# Создаем оптимизированный buildozer.spec 
RUN echo '[app]' > buildozer.spec 
RUN echo 'title = CryptoKeyFinder Mobile' >> buildozer.spec 
RUN echo 'package.name = cryptokeyfinder' >> buildozer.spec 
RUN echo 'package.domain = org.cryptokeyfinder' >> buildozer.spec 
RUN echo 'source.dir = .' >> buildozer.spec 
RUN echo 'version = 1.0' >> buildozer.spec 
RUN echo 'requirements = python3,kivy,requests' >> buildozer.spec 
RUN echo 'orientation = portrait' >> buildozer.spec 
RUN echo '[buildozer]' >> buildozer.spec 
RUN echo 'log_level = 1' >> buildozer.spec 
RUN echo 'warn_on_root = 0' >> buildozer.spec 
RUN echo 'android.api = 28' >> buildozer.spec 
RUN echo 'android.minapi = 21' >> buildozer.spec 
RUN echo 'android.archs = arm64-v8a' >> buildozer.spec 
 
# Настраиваем переменные окружения 
ENV PATH="/home/circleci/.local/bin:$PATH" 
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64" 
 
# Собираем APK 
RUN buildozer android debug 
