[app] 
title = CryptoKeyFinder Mobile 
package.name = cryptokeyfinder 
package.domain = org.cryptokeyfinder 
source.dir = . 
source.include_exts = py,png,jpg,kv,atlas,txt,md 
version = 1.0 
requirements = python3,kivy,requests,ecdsa,base58,pycryptodome 
orientation = portrait 
fullscreen = 0 
 
[buildozer] 
log_level = 2 
warn_on_root = 0 
build_dir = ./.buildozer 
bin_dir = ./bin 
 
android.api = 30 
android.minapi = 21 
android.ndk = 23b 
android.sdk = 30 
android.archs = arm64-v8a 
android.allow_backup = True 
android.release_artifact = apk 
android.debug_artifact = apk 
android.accept_sdk_license = True 
