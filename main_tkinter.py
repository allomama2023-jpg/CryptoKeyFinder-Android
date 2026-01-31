#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CryptoKeyFinder - Tkinter версия (альтернатива Kivy)
Работает на любой версии Python без дополнительных зависимостей
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import os
import json
from datetime import datetime
import logging

# Импорт наших криптографических утилит
from crypto_utils_android import AndroidBitcoinUtils, AndroidEthereumUtils, AndroidCryptoScanner

class CryptoKeyFinderTkinter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CryptoKeyFinder Mobile (Tkinter)")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Переменные состояния
        self.is_running = False
        self.total_checked = 0
        self.found_wallets = 0
        self.start_time = None
        self.found_wallets_list = []
        
        # Настройки
        self.delay_between_requests = 2.0
        self.max_threads = 2
        
        self.setup_ui()
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Главное меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="О программе", command=self.show_about)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка сетки
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="CryptoKeyFinder Mobile (Tkinter версия)", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Создаем notebook для вкладок
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.rowconfigure(1, weight=1)
        
        # Вкладка 1: Автоматический поиск
        search_frame = ttk.Frame(notebook, padding="10")
        notebook.add(search_frame, text="Поиск")
        self.create_search_tab(search_frame)
        
        # Вкладка 2: Тест ключа
        test_frame = ttk.Frame(notebook, padding="10")
        notebook.add(test_frame, text="Тест ключа")
        self.create_test_tab(test_frame)
        
        # Вкладка 3: Найденные кошельки
        wallets_frame = ttk.Frame(notebook, padding="10")
        notebook.add(wallets_frame, text="Кошельки")
        self.create_wallets_tab(wallets_frame)
        
        # Статистика внизу
        stats_frame = ttk.LabelFrame(main_frame, text="Статистика", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.create_stats(stats_frame)
        
        # Запуск обновления статистики
        self.update_stats()
        
    def create_search_tab(self, parent):
        """Создание вкладки поиска"""
        # Выбор криптовалюты
        crypto_frame = ttk.Frame(parent)
        crypto_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(crypto_frame, text="Криптовалюта:").grid(row=0, column=0, sticky=tk.W)
        self.crypto_var = tk.StringVar(value="Bitcoin")
        crypto_combo = ttk.Combobox(crypto_frame, textvariable=self.crypto_var, 
                                   values=["Bitcoin", "Ethereum"], state="readonly")
        crypto_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Настройки
        settings_frame = ttk.LabelFrame(parent, text="Настройки", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(settings_frame, text="Потоков:").grid(row=0, column=0, sticky=tk.W)
        self.threads_var = tk.StringVar(value="2")
        threads_spin = ttk.Spinbox(settings_frame, from_=1, to=5, textvariable=self.threads_var, width=10)
        threads_spin.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(settings_frame, text="Задержка (сек):").grid(row=1, column=0, sticky=tk.W)
        self.delay_var = tk.StringVar(value="2.0")
        delay_spin = ttk.Spinbox(settings_frame, from_=1.0, to=10.0, increment=0.5, 
                                textvariable=self.delay_var, width=10)
        delay_spin.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Кнопки управления
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(buttons_frame, text="Начать поиск", command=self.start_search)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(buttons_frame, text="Остановить", command=self.stop_search, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Лог
        log_label = ttk.Label(parent, text="Лог операций:")
        log_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(parent, height=10, width=70)
        self.log_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        parent.rowconfigure(5, weight=1)
        
        self.log_message("Программа запущена. Готова к поиску кошельков.")
        
    def create_test_tab(self, parent):
        """Создание вкладки тестирования ключа"""
        # Поле ввода ключа
        key_label = ttk.Label(parent, text="Приватный ключ (64 символа hex):")
        key_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.private_key_var = tk.StringVar()
        key_entry = ttk.Entry(parent, textvariable=self.private_key_var, width=70, font=("Consolas", 9))
        key_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Кнопки
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        test_button = ttk.Button(buttons_frame, text="Проверить ключ", command=self.test_private_key)
        test_button.grid(row=0, column=0, padx=(0, 10))
        
        generate_button = ttk.Button(buttons_frame, text="Сгенерировать", command=self.generate_key)
        generate_button.grid(row=0, column=1, padx=(0, 10))
        
        clear_button = ttk.Button(buttons_frame, text="Очистить", command=self.clear_key)
        clear_button.grid(row=0, column=2)
        
        # Результаты
        results_label = ttk.Label(parent, text="Результаты:")
        results_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(parent, height=15, width=70)
        self.results_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        parent.rowconfigure(4, weight=1)
        
    def create_wallets_tab(self, parent):
        """Создание вкладки найденных кошельков"""
        # Информация
        info_frame = ttk.Frame(parent)
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(info_frame, text="Найдено кошельков:").grid(row=0, column=0, sticky=tk.W)
        self.found_count_label = ttk.Label(info_frame, text="0", foreground="green", font=("Arial", 12, "bold"))
        self.found_count_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Кнопки
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        refresh_button = ttk.Button(buttons_frame, text="Обновить", command=self.refresh_wallets)
        refresh_button.grid(row=0, column=0, padx=(0, 10))
        
        export_button = ttk.Button(buttons_frame, text="Экспорт", command=self.export_wallets)
        export_button.grid(row=0, column=1, padx=(0, 10))
        
        clear_button = ttk.Button(buttons_frame, text="Очистить", command=self.clear_wallets)
        clear_button.grid(row=0, column=2)
        
        # Список кошельков
        wallets_label = ttk.Label(parent, text="Список найденных кошельков:")
        wallets_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.wallets_text = scrolledtext.ScrolledText(parent, height=15, width=70)
        self.wallets_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        parent.rowconfigure(3, weight=1)
        
    def create_stats(self, parent):
        """Создание панели статистики"""
        # Проверено ключей
        ttk.Label(parent, text="Проверено ключей:").grid(row=0, column=0, sticky=tk.W)
        self.checked_label = ttk.Label(parent, text="0")
        self.checked_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 20))
        
        # Найдено кошельков
        ttk.Label(parent, text="Найдено кошельков:").grid(row=0, column=2, sticky=tk.W)
        self.found_label = ttk.Label(parent, text="0", foreground="green")
        self.found_label.grid(row=0, column=3, sticky=tk.W, padx=(10, 20))
        
        # Время работы
        ttk.Label(parent, text="Время работы:").grid(row=1, column=0, sticky=tk.W)
        self.time_label = ttk.Label(parent, text="00:00:00")
        self.time_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 20))
        
        # Скорость
        ttk.Label(parent, text="Скорость:").grid(row=1, column=2, sticky=tk.W)
        self.speed_label = ttk.Label(parent, text="0 ключей/мин")
        self.speed_label.grid(row=1, column=3, sticky=tk.W, padx=(10, 0))
        
    def start_search(self):
        """Запуск поиска"""
        if self.is_running:
            return
        
        self.is_running = True
        self.total_checked = 0
        self.found_wallets = 0
        self.start_time = time.time()
        
        # Обновление UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress.start()
        
        # Получение настроек
        crypto_type = self.crypto_var.get()
        num_threads = int(self.threads_var.get()) if self.threads_var.get() else 2
        self.delay_between_requests = float(self.delay_var.get()) if self.delay_var.get() else 2.0
        
        self.log_message(f"Начинаем поиск {crypto_type} кошельков...")
        self.log_message(f"Потоков: {num_threads}, Задержка: {self.delay_between_requests}с")
        
        # Запуск потоков поиска
        for i in range(num_threads):
            thread = threading.Thread(target=self.search_worker, args=(crypto_type, i+1))
            thread.daemon = True
            thread.start()
    
    def stop_search(self):
        """Остановка поиска"""
        self.is_running = False
        
        # Обновление UI
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        
        self.log_message("Поиск остановлен пользователем")
    
    def search_worker(self, crypto_type: str, worker_id: int):
        """Рабочий поток для поиска"""
        self.log_message(f"Поток {worker_id} запущен для {crypto_type}")
        
        while self.is_running:
            try:
                if crypto_type == "Bitcoin":
                    private_key = AndroidBitcoinUtils.generate_private_key()
                    address = AndroidBitcoinUtils.private_key_to_address(private_key)
                    balance = AndroidBitcoinUtils.check_balance(address)
                elif crypto_type == "Ethereum":
                    private_key = AndroidEthereumUtils.generate_private_key()
                    address = AndroidEthereumUtils.private_key_to_address(private_key)
                    balance = AndroidEthereumUtils.check_balance(address)
                else:
                    continue
                
                self.total_checked += 1
                
                if self.total_checked % 5 == 0:
                    self.log_message(f"Поток {worker_id}: проверено {self.total_checked} адресов...")
                
                if balance is not None and balance > 0:
                    self.found_wallets += 1
                    self.save_found_wallet(private_key, address, str(balance), crypto_type)
                    self.log_message(f"🎉 НАЙДЕН КОШЕЛЕК! Адрес: {address}, Баланс: {balance} {crypto_type}")
                
                time.sleep(self.delay_between_requests)
                
            except Exception as e:
                self.log_message(f"Ошибка в потоке {worker_id}: {str(e)}")
                time.sleep(5)
        
        self.log_message(f"Поток {worker_id} завершен")
    
    def test_private_key(self):
        """Тестирование приватного ключа"""
        private_key = self.private_key_var.get().strip()
        
        if not private_key:
            messagebox.showerror("Ошибка", "Введите приватный ключ!")
            return
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Проверяется...\n")
        
        thread = threading.Thread(target=self._test_key_worker, args=(private_key,))
        thread.daemon = True
        thread.start()
    
    def _test_key_worker(self, private_key):
        """Рабочий поток для тестирования ключа"""
        try:
            results = "=== РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ===\n\n"
            
            if not AndroidBitcoinUtils.validate_private_key(private_key):
                results += "❌ Невалидный ключ\n"
                self.root.after(0, lambda: self.results_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.results_text.insert(tk.END, results))
                return
            
            results += "✅ Валидный ключ\n\n"
            
            # Bitcoin
            btc_address = AndroidBitcoinUtils.private_key_to_address(private_key)
            results += f"Bitcoin адрес:\n{btc_address}\n\n"
            
            btc_balance = AndroidBitcoinUtils.check_balance(btc_address)
            if btc_balance is not None:
                results += f"Bitcoin баланс: {btc_balance} BTC"
                if btc_balance > 0:
                    results += " 🎉"
                results += "\n\n"
            else:
                results += "Bitcoin баланс: Ошибка API\n\n"
            
            # Ethereum
            eth_address = AndroidEthereumUtils.private_key_to_address(private_key)
            results += f"Ethereum адрес:\n{eth_address}\n\n"
            
            eth_balance = AndroidEthereumUtils.check_balance(eth_address)
            if eth_balance is not None:
                results += f"Ethereum баланс: {eth_balance} ETH"
                if eth_balance > 0:
                    results += " 🎉"
                results += "\n\n"
            else:
                results += "Ethereum баланс: Ошибка API\n\n"
            
            if (btc_balance and btc_balance > 0) or (eth_balance and eth_balance > 0):
                results += "🎉 НАЙДЕН КОШЕЛЕК С БАЛАНСОМ!\n"
                
                if btc_balance and btc_balance > 0:
                    self.save_found_wallet(private_key, btc_address, str(btc_balance), "Bitcoin")
                
                if eth_balance and eth_balance > 0:
                    self.save_found_wallet(private_key, eth_address, str(eth_balance), "Ethereum")
            
            self.root.after(0, lambda: self.results_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.results_text.insert(tk.END, results))
            
        except Exception as e:
            error_text = f"Ошибка тестирования ключа: {str(e)}\n"
            self.root.after(0, lambda: self.results_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.results_text.insert(tk.END, error_text))
    
    def generate_key(self):
        """Генерация нового приватного ключа"""
        new_key = AndroidBitcoinUtils.generate_private_key()
        self.private_key_var.set(new_key)
        self.log_message(f"Сгенерирован новый ключ: {new_key[:16]}...")
    
    def clear_key(self):
        """Очистка поля ключа"""
        self.private_key_var.set("")
        self.results_text.delete(1.0, tk.END)
    
    def refresh_wallets(self):
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
        
        self.wallets_text.delete(1.0, tk.END)
        self.wallets_text.insert(tk.END, wallets_text)
        self.found_count_label.config(text=str(len(self.found_wallets_list)))
    
    def export_wallets(self):
        """Экспорт найденных кошельков"""
        if not self.found_wallets_list:
            messagebox.showinfo("Информация", "Нет найденных кошельков для экспорта")
            return
        
        try:
            filename = f"found_wallets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=== ЭКСПОРТ НАЙДЕННЫХ КОШЕЛЬКОВ (TKINTER) ===\n")
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
            
            messagebox.showinfo("Успех", f"Кошельки экспортированы в файл:\n{filename}")
            self.log_message(f"Экспортировано {len(self.found_wallets_list)} кошельков")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта: {str(e)}")
            self.log_message(f"Ошибка экспорта кошельков: {str(e)}")
    
    def clear_wallets(self):
        """Очистка списка найденных кошельков"""
        if not self.found_wallets_list:
            messagebox.showinfo("Информация", "Список найденных кошельков уже пуст")
            return
        
        result = messagebox.askyesno("Подтверждение", 
                                   f"Удалить все {len(self.found_wallets_list)} найденных кошельков?\n"
                                   "Это действие нельзя отменить!")
        
        if result:
            self.found_wallets_list.clear()
            self.refresh_wallets()
            self.log_message("Список найденных кошельков очищен")
    
    def save_found_wallet(self, private_key: str, address: str, balance: str, crypto_type: str):
        """Сохранение найденного кошелька"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            wallet_info = {
                "date": timestamp,
                "crypto_type": crypto_type,
                "private_key": private_key,
                "address": address,
                "balance": balance
            }
            self.found_wallets_list.append(wallet_info)
            
            filename = f"found_wallets_{crypto_type.lower()}.txt"
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"=== НАЙДЕН КОШЕЛЕК (TKINTER) ===\n")
                f.write(f"Дата: {timestamp}\n")
                f.write(f"Криптовалюта: {crypto_type}\n")
                f.write(f"Приватный ключ: {private_key}\n")
                f.write(f"Адрес: {address}\n")
                f.write(f"Баланс: {balance} {crypto_type}\n")
                f.write(f"{'='*50}\n\n")
                
            self.log_message(f"Кошелек сохранен в файл: {filename}")
            
        except Exception as e:
            self.log_message(f"Ошибка сохранения кошелька: {str(e)}")
    
    def update_stats(self):
        """Обновление статистики"""
        if self.is_running and self.start_time:
            elapsed_time = time.time() - self.start_time
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=time_str)
            
            if elapsed_time > 0:
                speed = (self.total_checked / elapsed_time) * 60
                self.speed_label.config(text=f"{speed:.1f} ключей/мин")
        
        self.checked_label.config(text=str(self.total_checked))
        self.found_label.config(text=str(self.found_wallets))
        
        # Планирование следующего обновления
        self.root.after(1000, self.update_stats)
    
    def log_message(self, message: str):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Ограничиваем размер лога
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete(1.0, f"{len(lines)-100}.0")
    
    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
CryptoKeyFinder Mobile (Tkinter версия) v1.0

Программа для поиска криптовалютных кошельков 
с положительным балансом.

✅ ТОЛЬКО РЕАЛЬНАЯ ПРОВЕРКА БЛОКЧЕЙНА
• Корректная генерация приватных ключей
• Правильное вычисление адресов
• Реальная проверка балансов через API

⚠️ ВНИМАНИЕ: Программа создана исключительно 
в образовательных целях!

Поддерживаемые криптовалюты:
• Bitcoin (BTC)
• Ethereum (ETH)

Версия: Tkinter (работает без дополнительных зависимостей)
        """
        messagebox.showinfo("О программе", about_text)
    
    def run(self):
        """Запуск приложения"""
        self.log_message("Tkinter версия запущена. Готова к поиску кошельков.")
        self.root.mainloop()

if __name__ == '__main__':
    app = CryptoKeyFinderTkinter()
    app.run()