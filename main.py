import tkinter as tk
from tkinter import ttk, messagebox
from modules.data_fetcher import get_order_book
from modules.data_analyzer import find_large_orders, find_key_levels
from modules.visualizer import show_order_book
import pandas as pd


class CryptoBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoBot")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        """Создание интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Выбор пары
        ttk.Label(main_frame, text="Криптопара:").grid(row=0, column=0)
        self.pair_var = tk.StringVar(value="BTC/USDT")
        pairs = ttk.Combobox(main_frame, textvariable=self.pair_var,
                             values=["BTC/USDT", "ETH/USDT", "BNB/USDT"])
        pairs.grid(row=0, column=1, pady=5)

        # Кнопка анализа
        ttk.Button(main_frame, text="Анализировать",
                   command=self.analyze).grid(row=1, column=0, columnspan=2, pady=10)

        # Вывод результатов
        self.result_text = tk.Text(main_frame, wrap=tk.WORD)
        self.result_text.grid(row=2, column=0, columnspan=2, sticky="nsew")

        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def analyze(self):
        """Анализ данных"""
        pair = self.pair_var.get()

        try:
            # Получаем данные
            order_book = get_order_book(pair)
            if not order_book:
                raise Exception("Не удалось получить данные")

            # Анализируем
            whales = find_large_orders(order_book)
            levels = find_key_levels(order_book)

            # Показываем график
            show_order_book(order_book, pair)

            # Формируем отчет
            report = self.generate_report(pair, whales, levels)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, report)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка анализа: {e}")

    def generate_report(self, pair, whales, levels):
        """Генерация отчета"""
        report = [
            f"Анализ пары: {pair}",
            "\n=== Крупные ордера ===",
            whales.to_string() if not whales.empty else "Крупные ордера не найдены",
            "\n=== Уровни поддержки ===",
            "\n".join(f"{x['price']:.2f} ({x['amount']:.4f})" for x in levels['support']),
            "\n=== Уровни сопротивления ===",
            "\n".join(f"{x['price']:.2f} ({x['amount']:.4f})" for x in levels['resistance'])
        ]
        return "\n".join(report)


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoBotApp(root)
    root.mainloop()