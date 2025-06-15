
import os
from datetime import datetime

def generate_text_report(pair, whales_df, levels, stats):
    """Создание текстового отчета"""
    report = [
        f"Анализ пары: {pair}",
        f"Дата и время: {datetime.now()}",
        "\n=== Статистика объёмов ===",
        f"Максимум: {stats['max_volume']:.4f}",
        f"Минимум: {stats['min_volume']:.4f}",
        f"Среднее: {stats['avg_volume']:.4f}",
        "\n=== Крупные ордера ===",
        whales_df.to_string() if not whales_df.empty else "Крупные ордера не найдены",
        "\n=== Уровни поддержки ===",
        "\n".join(f"{x['price']:.2f} ({x['amount']:.4f})" for x in levels['support']),
        "\n=== Уровни сопротивления ===",
        "\n".join(f"{x['price']:.2f} ({x['amount']:.4f})" for x in levels['resistance'])
    ]
    return "\n".join(report)


def save_report_to_file(text, directory="reports", filename_prefix="report"):
    """Сохраняет текст отчета в файл"""
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(directory, f"{filename_prefix}_{timestamp}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    return filepath
