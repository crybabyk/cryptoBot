
import os
from datetime import datetime

def generate_text_report(pair, whales, support_levels, resistance_levels, stats):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = f"Отчет по паре {pair} — {timestamp}\n"

    report += "\n=== Статистика объёмов ===\n"
    report += f"Максимальный объём ордера: {stats['max_volume']:.5f}\n"
    report += f"Минимальный объём: {stats['min_volume']:.5f}\n"
    report += f"Средний объём: {stats['avg_volume']:.2f}\n"

    report += "\n=== Крупные ордера (киты) ===\n"
    if whales is not None and not whales.empty:
        for _, row in whales.iterrows():
            pct = row['percent'] * 100
            report += f"Цена: {row['price']}, Объём: {row['amount']} ({pct:.2f}%)\n"
    else:
        report += "Крупные ордера не обнаружены.\n"

    report += "\n=== Уровни поддержки ===\n"
    for lvl in support_levels:
        report += f"{lvl['price']} — {lvl['amount']}\n"

    report += "\n=== Уровни сопротивления ===\n"
    for lvl in resistance_levels:
        report += f"{lvl['price']} — {lvl['amount']}\n"

    recommendations = []
    # 1. Анализ крупных ордеров
    if whales is not None and not whales.empty:
        top_whale = whales.iloc[0]

        if support_levels and top_whale['price'] <= support_levels[0]['price']:
            recommendations.append(
                "Крупный ордер на покупку находится на уровне поддержки. Возможно, стоит рассмотреть покупку, т.к. крупные игроки поддерживают этот уровень."
            )
        else:
            recommendations.append(
                "Присутствует крупный ордер на покупку выше уровня поддержки. Следите за движением цены к этому уровню для возможного отскока."
            )
    # 2. Ликвидность рынка
    if stats['avg_volume'] < stats['max_volume'] / 2:
        recommendations.append(
            "Средний объём ордеров менее половины максимального. Будьте осторожны — рынок может быть неликвидным, возможны резкие колебания цены."
        )
    # 3. Диапазон между поддержкой и сопротивлением
    if support_levels and resistance_levels:
        low = support_levels[0]['price']
        high = resistance_levels[0]['price']
        if high > low:
            width = (high - low) / low
            if width < 0.01:
                recommendations.append(
                    "Диапазон между поддержкой и сопротивлением узкий (<1%). Возможно, вскоре будет резкий рост или падение цены."
                )
    # Если нет явных сигналов
    if not recommendations:
        recommendations.append(
            "Явных сигналов для действий не обнаружено. Дождитесь более явных уровней или значительных объёмов."
        )

    report += "\n=== Рекомендации ===\n"
    for rec in recommendations:
        report += f"- {rec}\n"

    return report

def save_report_to_file(text, directory="reports", filename_prefix="report"):
    """Сохраняет текст отчета в файл"""
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(directory, f"{filename_prefix}_{timestamp}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    return filepath