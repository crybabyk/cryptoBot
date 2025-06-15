
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from modules import data_fetcher, data_analyzer, visualizer, report_generator, settings

logging.basicConfig(level=logging.INFO)

class CryptoBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoBot")
        self.root.geometry("900x700")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Пара криптовалют
        ttk.Label(main_frame, text="Криптопара:").grid(row=0, column=0)
        self.pair_var = tk.StringVar(value=settings.DEFAULT_PAIR)
        pair_menu = ttk.Combobox(main_frame, textvariable=self.pair_var, values=settings.SUPPORTED_PAIRS)
        pair_menu.grid(row=0, column=1, pady=5)

        # Кнопка анализа
        ttk.Button(main_frame, text="Анализировать", command=self.analyze).grid(row=1, column=0, columnspan=2, pady=10)

        # Кнопка сохранения отчета
        ttk.Button(main_frame, text="Сохранить отчет", command=self.save_report).grid(row=2, column=0, columnspan=2)

        # Вывод результатов
        self.result_text = tk.Text(main_frame, wrap=tk.WORD)
        self.result_text.grid(row=3, column=0, columnspan=2, sticky="nsew")

        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def analyze(self):
        pair = self.pair_var.get()
        try:
            order_book = data_fetcher.get_order_book(pair)
            if not order_book:
                raise Exception("Не удалось получить данные")

            whales = data_analyzer.detect_whales(order_book, threshold=settings.WHALE_THRESHOLD)
            levels = data_analyzer.calculate_support_resistance(order_book, levels=settings.LEVEL_COUNT)
            stats = data_analyzer.volume_statistics(order_book)

            visualizer.plot_order_book(order_book, pair)

            self.current_report = report_generator.generate_text_report(pair, whales, levels, stats)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.current_report)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка анализа: {e}")

    def save_report(self):
        try:
            if hasattr(self, 'current_report'):
                path = report_generator.save_report_to_file(self.current_report)
                messagebox.showinfo("Сохранено", f"Отчет сохранен в: {path}")
            else:
                messagebox.showwarning("Нет данных", "Сначала выполните анализ.")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoBotApp(root)
    root.mainloop()
