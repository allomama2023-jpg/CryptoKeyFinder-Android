#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CryptoKeyFinder Android - Мобильная версия
Поиск криптовалютных кошельков с положительным балансом
Версия для Android с Kivy
"""

import os
import sys
import threading
import time
import json
from datetime import datetime
from typing import Optional, Tuple
import logging

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.utils import platform
from kivy.logger import Logger

# Импорт наших криптографических утилит
from crypto_utils_android import AndroidBitcoinUtils, AndroidEthereumUtils, AndroidCryptoScanner

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CryptoKeyFinderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "CryptoKeyFinder Mobile"
        
        # Переменные состояния
        self.is_running = False
        self.total_checked = 0
        self.found_wallets = 0
        self.start_time = None
        self.found_wallets_list = []
        
        # Настройки
        self.delay_between_requests = 2.0  # Больше задержка для мобильного
        self.max_threads = 2  # Меньше потоков для мобильного
        
        # Инициализация утилит
        self.crypto_scanner = None
        
    def build(self):
        """Создание пользовательского интерфейса"""
        
        # Основной контейнер
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Заголовок
        title_label = Label(
            text='CryptoKeyFinder Mobile v1.0',
            size_hint_y=None,
            height=50,
            font_size=20,
            bold=True
        )
        main_layout.add_widget(title_label)
        
        # Создаем вкладки
        tab_panel = TabbedPanel(do_default_tab=False)
        
        # Вкладка 1: Автоматический поиск
        search_tab = TabbedPanelItem(text='Поиск')
        search_layout = self.create_search_tab()
        search_tab.add_widget(search_layout)
        tab_panel.add_widget(search_tab)
        
        # Вкладка 2: Тест ключа
        test_tab = TabbedPanelItem(text='Тест ключа')
        test_layout = self.create_test_tab()
        test_tab.add_widget(test_layout)
        tab_panel.add_widget(test_tab)
        
        # Вкладка 3: Найденные кошельки
        wallets_tab = TabbedPanelItem(text='Кошельки')
        wallets_layout = self.create_wallets_tab()
        wallets_tab.add_widget(wallets_layout)
        tab_panel.add_widget(wallets_tab)
        
        # Вкладка 4: Управление
        manage_tab = TabbedPanelItem(text='Управление')
        manage_layout = self.create_manage_tab()
        manage_tab.add_widget(manage_layout)
        tab_panel.add_widget(manage_tab)
        
        main_layout.add_widget(tab_panel)
        
        # Статистика внизу
        stats_layout = self.create_stats_layout()
        main_layout.add_widget(stats_layout)
        
        # Запуск обновления статистики
        Clock.schedule_interval(self.update_stats, 1.0)
        
        return main_layout
    
    def create_search_tab(self):
        """Создание вкладки автоматического поиска"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Выбор криптовалюты
        crypto_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        crypto_layout.add_widget(Label(text='Криптовалюта:', size_hint_x=0.4))
        self.crypto_spinner = Spinner(
            text='Bitcoin',
            values=['Bitcoin', 'Ethereum'],
            size_hint_x=0.6
        )
        crypto_layout.add_widget(self.crypto_spinner)
        layout.add_widget(crypto_layout)
        
        # Количество потоков
        threads_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        threads_layout.add_widget(Label(text='Потоков:', size_hint_x=0.4))
        self.threads_input = TextInput(
            text='2',
            multiline=False,
            input_filter='int',
            size_hint_x=0.6
        )
        threads_layout.add_widget(self.threads_input)
        layout.add_widget(threads_layout)
        
        # Задержка
        delay_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        delay_layout.add_widget(Label(text='Задержка (сек):', size_hint_x=0.4))
        self.delay_input = TextInput(
            text='2.0',
            multiline=False,
            input_filter='float',
            size_hint_x=0.6
        )
        delay_layout.add_widget(self.delay_input)
        layout.add_widget(delay_layout)
        
        # Кнопки управления
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        self.start_button = Button(text='Начать поиск', background_color=(0, 0.8, 0, 1))
        self.start_button.bind(on_press=self.start_search)
        buttons_layout.add_widget(self.start_button)
        
        self.stop_button = Button(text='Остановить', background_color=(0.8, 0, 0, 1), disabled=True)
        self.stop_button.bind(on_press=self.stop_search)
        buttons_layout.add_widget(self.stop_button)
        
        layout.add_widget(buttons_layout)
        
        # Прогресс бар
        self.progress_bar = ProgressBar(size_hint_y=None, height=20)
        layout.add_widget(self.progress_bar)
        
        # Лог
        log_label = Label(text='Лог операций:', size_hint_y=None, height=30, halign='left')
        layout.add_widget(log_label)
        
        self.log_text = TextInput(
            text='Программа запущена. Готова к поиску кошельков.\n',
            multiline=True,
            readonly=True,
            size_hint_y=0.4
        )
        layout.add_widget(self.log_text)
        
        return layout
    
    def create_test_tab(self):
        """Создание вкладки тестирования ключа"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Поле ввода ключа
        key_label = Label(text='Приватный ключ (64 символа hex):', size_hint_y=None, height=30)
        layout.add_widget(key_label)
        
        self.private_key_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size=12
        )
        layout.add_widget(self.private_key_input)
        
        # Кнопки
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        test_button = Button(text='Проверить ключ', background_color=(0, 0, 0.8, 1))
        test_button.bind(on_press=self.test_private_key)
        buttons_layout.add_widget(test_button)
        
        generate_button = Button(text='Сгенерировать', background_color=(0.8, 0.8, 0, 1))
        generate_button.bind(on_press=self.generate_key)
        buttons_layout.add_widget(generate_button)
        
        clear_button = Button(text='Очистить', background_color=(0.5, 0.5, 0.5, 1))
        clear_button.bind(on_press=self.clear_key)
        buttons_layout.add_widget(clear_button)
        
        layout.add_widget(buttons_layout)
        
        # Результаты
        results_label = Label(text='Результаты:', size_hint_y=None, height=30, halign='left')
        layout.add_widget(results_label)
        
        self.results_text = TextInput(
            text='Результаты тестирования появятся здесь...\n',
            multiline=True,
            readonly=True,
            size_hint_y=0.5
        )
        layout.add_widget(self.results_text)
        
        return layout
    
    def create_wallets_tab(self):
        """Создание вкладки найденных кошельков"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Информация
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        info_layout.add_widget(Label(text='Найдено кошельков:', size_hint_x=0.6))
        self.found_count_label = Label(text='0', size_hint_x=0.4, color=(0, 1, 0, 1))
        info_layout.add_widget(self.found_count_label)
        layout.add_widget(info_layout)
        
        # Кнопки управления
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        refresh_button = Button(text='Обновить', background_color=(0, 0.8, 0.8, 1))
        refresh_button.bind(on_press=self.refresh_wallets)
        buttons_layout.add_widget(refresh_button)
        
        export_button = Button(text='Экспорт', background_color=(0.8, 0.8, 0, 1))
        export_button.bind(on_press=self.export_wallets)
        buttons_layout.add_widget(export_button)
        
        clear_button = Button(text='Очистить', background_color=(0.8, 0, 0, 1))
        clear_button.bind(on_press=self.clear_wallets)
        buttons_layout.add_widget(clear_button)
        
        layout.add_widget(buttons_layout)
        
        # Список кошельков
        wallets_label = Label(text='Список найденных кошельков:', size_hint_y=None, height=30)
        layout.add_widget(wallets_label)
        
        self.wallets_text = TextInput(
            text='Найденные кошельки появятся здесь...\n',
            multiline=True,
            readonly=True,
            size_hint_y=0.6
        )
        layout.add_widget(self.wallets_text)
        
        return layout
    
    def create_manage_tab(self):
        """Создание вкладки управления кошельком"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Подключение к кошельку
        connect_label = Label(text='Подключение к кошельку:', size_hint_y=None, height=30)
        layout.add_widget(connect_label)
        
        # Приватный ключ для подключения
        self.wallet_key_input = TextInput(
            hint_text='Приватный ключ кошелька...',
            multiline=False,
            size_hint_y=None,
            height=40,
            password=True
        )
        layout.add_widget(self.wallet_key_input)
        
        # Выбор криптовалюты для кошелька
        wallet_crypto_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        wallet_crypto_layout.add_widget(Label(text='Криптовалюта:', size_hint_x=0.4))
        self.wallet_crypto_spinner = Spinner(
            text='Bitcoin',
            values=['Bitcoin', 'Ethereum'],
            size_hint_x=0.6
        )
        wallet_crypto_layout.add_widget(self.wallet_crypto_spinner)
        layout.add_widget(wallet_crypto_layout)
        
        # Кнопки подключения
        connect_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        self.connect_button = Button(text='Подключиться', background_color=(0, 0.8, 0, 1))
        self.connect_button.bind(on_press=self.connect_wallet)
        connect_buttons_layout.add_widget(self.connect_button)
        
        self.disconnect_button = Button(text='Отключиться', background_color=(0.8, 0, 0, 1), disabled=True)
        self.disconnect_button.bind(on_press=self.disconnect_wallet)
        connect_buttons_layout.add_widget(self.disconnect_button)
        
        layout.add_widget(connect_buttons_layout)
        
        # Информация о кошельке
        wallet_info_label = Label(text='Информация о кошельке:', size_hint_y=None, height=30)
        layout.add_widget(wallet_info_label)
        
        self.wallet_info_text = TextInput(
            text='Кошелек не подключен\n',
            multiline=True,
            readonly=True,
            size_hint_y=0.4
        )
        layout.add_widget(self.wallet_info_text)
        
        return layout
    
    def create_stats_layout(self):
        """Создание панели статистики"""
        stats_layout = GridLayout(cols=2, size_hint_y=None, height=80, spacing=5)
        
        # Проверено ключей
        stats_layout.add_widget(Label(text='Проверено:', halign='left'))
        self.checked_label = Label(text='0', halign='right')
        stats_layout.add_widget(self.checked_label)
        
        # Найдено кошельков
        stats_layout.add_widget(Label(text='Найдено:', halign='left'))
        self.found_label = Label(text='0', halign='right', color=(0, 1, 0, 1))
        stats_layout.add_widget(self.found_label)
        
        # Время работы
        stats_layout.add_widget(Label(text='Время:', halign='left'))
        self.time_label = Label(text='00:00:00', halign='right')
        stats_layout.add_widget(self.time_label)
        
        # Скорость
        stats_layout.add_widget(Label(text='Скорость:', halign='left'))
        self.speed_label = Label(text='0 ключей/мин', halign='right')
        stats_layout.add_widget(self.speed_label)
        
        return stats_layout
    
    def start_search(self, instance):
        """Запуск поиска"""
        if self.is_running:
            return
        
        self.is_running = True
        self.total_checked = 0
        self.found_wallets = 0
        self.start_time = time.time()
        
        # Обновление UI
        self.start_button.disabled = True
        self.stop_button.disabled = False
        
        # Получение настроек
        crypto_type = self.crypto_spinner.text
        num_threads = int(self.threads_input.text) if self.threads_input.text else 2
        self.delay_between_requests = float(self.delay_input.text) if self.delay_input.text else 2.0
        
        self.log_message(f"Начинаем поиск {crypto_type} кошельков...")
        self.log_message(f"Потоков: {num_threads}, Задержка: {self.delay_between_requests}с")
        
        # Запуск потоков поиска
        for i in range(num_threads):
            thread = threading.Thread(target=self.search_worker, args=(crypto_type, i+1))
            thread.daemon = True
            thread.start()
    
    def stop_search(self, instance):
        """Остановка поиска"""
        self.is_running = False
        
        # Обновление UI
        self.start_button.disabled = False
        self.stop_button.disabled = True
        
        self.log_message("Поиск остановлен пользователем")
    
    def search_worker(self, crypto_type: str, worker_id: int):
        """Рабочий поток для поиска"""
        self.log_message(f"Поток {worker_id} запущен для {crypto_type}")
        
        # Инициализируем сканер для этого потока
        scanner = AndroidCryptoScanner(crypto_type, self.delay_between_requests)
        
        while self.is_running:
            try:
                # Используем только реальную проверку блокчейна
                if crypto_type == "Bitcoin":
                    private_key = AndroidBitcoinUtils.generate_private_key()
                    address = AndroidBitcoinUtils.private_key_to_address(private_key)
                    balance = AndroidBitcoinUtils.check_balance(address)
                    
                elif crypto_type == "Ethereum":
                    private_key = AndroidEthereumUtils.generate_private_key()
                    address = AndroidEthereumUtils.private_key_to_address(private_key)
                    balance = AndroidEthereumUtils.check_balance(address)
                    
                else:
                    self.log_message(f"Криптовалюта {crypto_type} не поддерживается", "ERROR")
                    time.sleep(5)
                    continue
                
                self.total_checked += 1
                
                # Логируем каждый 5-й проверенный адрес (реже для мобильного)
                if self.total_checked % 5 == 0:
                    self.log_message(f"Поток {worker_id}: проверено {self.total_checked} адресов...")
                
                # Проверяем найден ли баланс
                if balance is not None and balance > 0:
                    self.found_wallets += 1
                    self.save_found_wallet(private_key, address, str(balance), crypto_type)
                    self.log_message(
                        f"🎉 НАЙДЕН КОШЕЛЕК! Адрес: {address}, Баланс: {balance} {crypto_type}"
                    )
                
                # Задержка между запросами
                time.sleep(self.delay_between_requests)
                    
            except Exception as e:
                self.log_message(f"Ошибка в потоке {worker_id}: {str(e)}")
                time.sleep(5)
                
        self.log_message(f"Поток {worker_id} завершен")
    
    def test_private_key(self, instance):
        """Тестирование приватного ключа"""
        private_key = self.private_key_input.text.strip()
        
        if not private_key:
            self.show_popup("Ошибка", "Введите приватный ключ!")
            return
        
        self.results_text.text = "Проверяется...\n"
        
        # Запуск в отдельном потоке
        thread = threading.Thread(target=self._test_key_worker, args=(private_key,))
        thread.daemon = True
        thread.start()
    
    def _test_key_worker(self, private_key):
        """Рабочий поток для тестирования ключа"""
        try:
            results = "=== РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ===\n\n"
            
            # Проверка валидности ключа
            if not AndroidBitcoinUtils.validate_private_key(private_key):
                results += "❌ Невалидный ключ\n"
                Clock.schedule_once(lambda dt: setattr(self.results_text, 'text', results))
                return
            
            results += "✅ Валидный ключ\n\n"
            
            # Генерация Bitcoin адреса
            btc_address = AndroidBitcoinUtils.private_key_to_address(private_key)
            results += f"Bitcoin адрес:\n{btc_address}\n\n"
            
            # Генерация Ethereum адреса
            eth_address = AndroidEthereumUtils.private_key_to_address(private_key)
            results += f"Ethereum адрес:\n{eth_address}\n\n"
            
            # Проверка Bitcoin баланса
            results += "Проверка Bitcoin баланса...\n"
            btc_balance = AndroidBitcoinUtils.check_balance(btc_address)
            if btc_balance is not None:
                btc_text = f"Bitcoin баланс: {btc_balance} BTC"
                if btc_balance > 0:
                    btc_text += " 🎉"
                results += btc_text + "\n\n"
            else:
                results += "Bitcoin баланс: Ошибка API\n\n"
            
            # Проверка Ethereum баланса
            results += "Проверка Ethereum баланса...\n"
            eth_balance = AndroidEthereumUtils.check_balance(eth_address)
            if eth_balance is not None:
                eth_text = f"Ethereum баланс: {eth_balance} ETH"
                if eth_balance > 0:
                    eth_text += " 🎉"
                results += eth_text + "\n\n"
            else:
                results += "Ethereum баланс: Ошибка API\n\n"
            
            if (btc_balance and btc_balance > 0) or (eth_balance and eth_balance > 0):
                results += "🎉 НАЙДЕН КОШЕЛЕК С БАЛАНСОМ!\n"
                
                # Сохраняем найденные кошельки
                if btc_balance and btc_balance > 0:
                    self.save_found_wallet(private_key, btc_address, str(btc_balance), "Bitcoin")
                
                if eth_balance and eth_balance > 0:
                    self.save_found_wallet(private_key, eth_address, str(eth_balance), "Ethereum")
            
            Clock.schedule_once(lambda dt: setattr(self.results_text, 'text', results))
                
        except Exception as e:
            error_text = f"Ошибка тестирования ключа: {str(e)}\n"
            Clock.schedule_once(lambda dt: setattr(self.results_text, 'text', error_text))
    
    def generate_key(self, instance):
        """Генерация нового приватного ключа"""
        new_key = AndroidBitcoinUtils.generate_private_key()
        self.private_key_input.text = new_key
        self.log_message(f"Сгенерирован новый ключ: {new_key[:16]}...")
    
    def clear_key(self, instance):
        """Очистка поля ключа"""
        self.private_key_input.text = ""
        self.results_text.text = "Результаты тестирования появятся здесь...\n"
    
    def refresh_wallets(self, instance):
        """Обновление списка найденных кошельков"""
        wallets_text = "=== НАЙДЕННЫЕ КОШЕЛЬКИ ===\n\n"
        
        if not self.found_wallets_list:
            wallets_text += "Пока не найдено кошельков с балансом\n"
        else:
            for i, wallet in enumerate(self.found_wallets_list, 1):
                wallets_text += f"=== КОШЕЛЕК #{i} ===\n"
                wallets_text += f"Дата: {wallet['date']}\n"
                wallets_text += f"Криптовалюта: {wallet['crypto_type']}\n"
                wallets_text += f"Адрес: {wallet['address']}\n"
                wallets_text += f"Баланс: {wallet['balance']} {wallet['crypto_type']}\n"
                wallets_text += f"Ключ: {wallet['private_key'][:16]}...\n"
                wallets_text += "-" * 30 + "\n\n"
        
        self.wallets_text.text = wallets_text
        self.found_count_label.text = str(len(self.found_wallets_list))
    
    def export_wallets(self, instance):
        """Экспорт найденных кошельков"""
        if not self.found_wallets_list:
            self.show_popup("Информация", "Нет найденных кошельков для экспорта")
            return
        
        try:
            # Определяем путь для сохранения (Android)
            if platform == 'android':
                from android.storage import primary_external_storage_path
                storage_path = primary_external_storage_path()
                filename = os.path.join(storage_path, f"found_wallets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            else:
                filename = f"found_wallets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=== ЭКСПОРТ НАЙДЕННЫХ КОШЕЛЬКОВ (MOBILE) ===\n")
                f.write(f"Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Всего кошельков: {len(self.found_wallets_list)}\n\n")
                
                for i, wallet in enumerate(self.found_wallets_list, 1):
                    f.write(f"=== КОШЕЛЕК #{i} ===\n")
                    f.write(f"Дата находки: {wallet['date']}\n")
                    f.write(f"Криптовалюта: {wallet['crypto_type']}\n")
                    f.write(f"Приватный ключ: {wallet['private_key']}\n")
                    f.write(f"Адрес: {wallet['address']}\n")
                    f.write(f"Баланс: {wallet['balance']} {wallet['crypto_type']}\n")
                    f.write("=" * 50 + "\n\n")
            
            self.show_popup("Успех", f"Кошельки экспортированы в:\n{filename}")
            self.log_message(f"Экспортировано {len(self.found_wallets_list)} кошельков")
            
        except Exception as e:
            self.show_popup("Ошибка", f"Ошибка экспорта: {str(e)}")
            self.log_message(f"Ошибка экспорта кошельков: {str(e)}")
    
    def clear_wallets(self, instance):
        """Очистка списка найденных кошельков"""
        if not self.found_wallets_list:
            self.show_popup("Информация", "Список найденных кошельков уже пуст")
            return
        
        # Создаем popup для подтверждения
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=f'Удалить все {len(self.found_wallets_list)} найденных кошельков?\nЭто действие нельзя отменить!'))
        
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        yes_button = Button(text='Да', background_color=(0.8, 0, 0, 1))
        no_button = Button(text='Нет', background_color=(0, 0.8, 0, 1))
        
        buttons_layout.add_widget(yes_button)
        buttons_layout.add_widget(no_button)
        content.add_widget(buttons_layout)
        
        popup = Popup(title='Подтверждение', content=content, size_hint=(0.8, 0.4))
        
        def confirm_clear(instance):
            self.found_wallets_list.clear()
            self.refresh_wallets(None)
            self.log_message("Список найденных кошельков очищен")
            popup.dismiss()
        
        def cancel_clear(instance):
            popup.dismiss()
        
        yes_button.bind(on_press=confirm_clear)
        no_button.bind(on_press=cancel_clear)
        
        popup.open()
    
    def connect_wallet(self, instance):
        """Подключение к кошельку"""
        private_key = self.wallet_key_input.text.strip()
        crypto_type = self.wallet_crypto_spinner.text
        
        if not private_key:
            self.show_popup("Ошибка", "Введите приватный ключ!")
            return
        
        # Запуск в отдельном потоке
        thread = threading.Thread(target=self._connect_wallet_worker, args=(private_key, crypto_type))
        thread.daemon = True
        thread.start()
    
    def _connect_wallet_worker(self, private_key, crypto_type):
        """Рабочий поток для подключения к кошельку"""
        try:
            # Проверяем валидность ключа
            if crypto_type == "Bitcoin":
                if not AndroidBitcoinUtils.validate_private_key(private_key):
                    Clock.schedule_once(lambda dt: self.show_popup("Ошибка", "Невалидный Bitcoin приватный ключ!"))
                    return
                address = AndroidBitcoinUtils.private_key_to_address(private_key)
                balance = AndroidBitcoinUtils.check_balance(address)
                currency = "BTC"
            elif crypto_type == "Ethereum":
                if not AndroidEthereumUtils.validate_private_key(private_key):
                    Clock.schedule_once(lambda dt: self.show_popup("Ошибка", "Невалидный Ethereum приватный ключ!"))
                    return
                address = AndroidEthereumUtils.private_key_to_address(private_key)
                balance = AndroidEthereumUtils.check_balance(address)
                currency = "ETH"
            else:
                Clock.schedule_once(lambda dt: self.show_popup("Ошибка", "Неподдерживаемая криптовалюта!"))
                return
            
            # Обновляем интерфейс
            wallet_info = f"=== ПОДКЛЮЧЕННЫЙ КОШЕЛЕК ===\n\n"
            wallet_info += f"Статус: Подключен\n"
            wallet_info += f"Криптовалюта: {crypto_type}\n"
            wallet_info += f"Адрес: {address}\n"
            wallet_info += f"Баланс: {balance} {currency}\n"
            wallet_info += f"Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            if balance > 0:
                wallet_info += "🎉 Кошелек имеет положительный баланс!\n"
            else:
                wallet_info += "⚠️ Кошелек пустой\n"
            
            Clock.schedule_once(lambda dt: setattr(self.wallet_info_text, 'text', wallet_info))
            Clock.schedule_once(lambda dt: setattr(self.connect_button, 'disabled', True))
            Clock.schedule_once(lambda dt: setattr(self.disconnect_button, 'disabled', False))
            
            self.log_message(f"Подключен к {crypto_type} кошельку: {address}")
            self.log_message(f"Баланс: {balance} {currency}")
            
            if balance > 0:
                Clock.schedule_once(lambda dt: self.show_popup("Успех", f"Подключение успешно!\nАдрес: {address}\nБаланс: {balance} {currency}"))
            else:
                Clock.schedule_once(lambda dt: self.show_popup("Подключено", f"Подключение успешно!\nАдрес: {address}\nБаланс: 0 {currency}"))
                
        except Exception as e:
            error_msg = f"Ошибка подключения к кошельку: {str(e)}"
            Clock.schedule_once(lambda dt: self.show_popup("Ошибка", error_msg))
            self.log_message(error_msg)
    
    def disconnect_wallet(self, instance):
        """Отключение от кошелька"""
        self.wallet_info_text.text = "Кошелек не подключен\n"
        self.connect_button.disabled = False
        self.disconnect_button.disabled = True
        self.log_message("Отключен от кошелька")
        self.show_popup("Отключено", "Кошелек отключен")
    
    def save_found_wallet(self, private_key: str, address: str, balance: str, crypto_type: str):
        """Сохранение найденного кошелька"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Добавляем в список для отображения в GUI
            wallet_info = {
                "date": timestamp,
                "crypto_type": crypto_type,
                "private_key": private_key,
                "address": address,
                "balance": balance
            }
            self.found_wallets_list.append(wallet_info)
            
            # Сохраняем в файл
            if platform == 'android':
                from android.storage import primary_external_storage_path
                storage_path = primary_external_storage_path()
                filename = os.path.join(storage_path, f"found_wallets_{crypto_type.lower()}.txt")
            else:
                filename = f"found_wallets_{crypto_type.lower()}.txt"
            
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"=== НАЙДЕН КОШЕЛЕК (MOBILE) ===\n")
                f.write(f"Дата: {timestamp}\n")
                f.write(f"Криптовалюта: {crypto_type}\n")
                f.write(f"Приватный ключ: {private_key}\n")
                f.write(f"Адрес: {address}\n")
                f.write(f"Баланс: {balance} {crypto_type}\n")
                f.write(f"{'='*50}\n\n")
                
            self.log_message(f"Кошелек сохранен в файл: {filename}")
            
        except Exception as e:
            self.log_message(f"Ошибка сохранения кошелька: {str(e)}")
    
    def update_stats(self, dt):
        """Обновление статистики"""
        if self.is_running and self.start_time:
            elapsed_time = time.time() - self.start_time
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.text = time_str
            
            # Скорость проверки
            if elapsed_time > 0:
                speed = (self.total_checked / elapsed_time) * 60
                self.speed_label.text = f"{speed:.1f} ключей/мин"
        
        # Обновление счетчиков
        self.checked_label.text = str(self.total_checked)
        self.found_label.text = str(self.found_wallets)
        self.found_count_label.text = str(len(self.found_wallets_list))
    
    def log_message(self, message: str, level: str = "INFO"):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        # Обновляем лог в главном потоке
        Clock.schedule_once(lambda dt: self._update_log(log_entry))
        
        # Логирование в файл
        logging.info(message)
    
    def _update_log(self, log_entry):
        """Обновление лога в главном потоке"""
        self.log_text.text += log_entry
        # Ограничиваем размер лога для мобильного устройства
        lines = self.log_text.text.split('\n')
        if len(lines) > 100:
            self.log_text.text = '\n'.join(lines[-100:])
    
    def show_popup(self, title: str, message: str):
        """Показать всплывающее окно"""
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message, text_size=(300, None), halign='center'))
        
        close_button = Button(text='OK', size_hint_y=None, height=50)
        content.add_widget(close_button)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.6))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    CryptoKeyFinderApp().run()