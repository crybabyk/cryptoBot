
import matplotlib.pyplot as plt
import pandas as pd
from modules.data_analyzer import detect_whales, calculate_support_resistance

def plot_order_book(order_book, pair='BTC/USDT', save_path=None):
    """Построение и сохранение графика стакана ордеров"""
    if not order_book:
        return

    bids = pd.DataFrame(order_book['bids'], columns=['price', 'amount'])
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'amount'])

    support_levels, resistance_levels = calculate_support_resistance(order_book)
    whales = detect_whales(order_book)

    if support_levels and resistance_levels:
        low = support_levels[0]['price']
        high = resistance_levels[0]['price']
        width_pct = (high - low) / low * 100
    else:
        width_pct = 0

    plt.figure(figsize=(10, 6))
    plt.bar(bids['price'], bids['amount'], color='green', label='Покупки')
    plt.bar(asks['price'], asks['amount'], color='red', label='Продажи')
    plt.ticklabel_format(style='plain', axis='x', useOffset=False)
    plt.title(f'Стакан ордеров: {pair}', pad=20)
    plt.xlabel('Цена')
    plt.ylabel('Объём')

    tol = 0.02
    selected = []
    for _, row in whales.sort_values('price', ascending=False).iterrows():
        if not any(abs(row['price'] - picked['price']) < tol for picked in selected):
            selected.append(row)
    filtered_whales = pd.DataFrame(selected)

    ylim_max = plt.ylim()[1]

    support_shown = False
    for lvl in support_levels:
        label = 'Уровень поддержки' if not support_shown else None
        plt.axvline(lvl['price'], color='green', linestyle='--', label=label)
        plt.text(lvl['price'], ylim_max * 0.9, f"Поддержка {lvl['price']}", rotation=90, va='top', ha='right')
        support_shown = True

    resistance_shown = False
    for lvl in resistance_levels:
        label = 'Уровень сопротивления' if not resistance_shown else None
        plt.axvline(lvl['price'], color='red', linestyle='--', label=label)
        plt.text(lvl['price'], ylim_max * 0.9, f"Сопротивление {lvl['price']}", rotation=90, va='top')
        resistance_shown = True

    for _, row in filtered_whales.head(3).iterrows():
        plt.annotate(
            f"Кит: {row['price']} ({row['percent']*100:.1f}%)",
            xy=(row['price'], row['amount']),
            xytext=(row['price'], row['amount'] * 1.055),
            arrowprops=dict(arrowstyle='->'),
            ha='center'
        )

    plt.text(
        0.95, 0.95,
        f"Диапазон: {width_pct:.2f}%",
        transform=plt.gca().transAxes,
        ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.5)
    )

    plt.legend()

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
