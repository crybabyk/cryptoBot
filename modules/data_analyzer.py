
import pandas as pd

def detect_whales(order_book, threshold=0.1):
    """Определение крупных ордеров (китов)"""
    if not order_book:
        return pd.DataFrame()

    bids = pd.DataFrame(order_book['bids'], columns=['price', 'amount'])
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'amount'])
    df = pd.concat([bids, asks])

    total = df['amount'].sum()
    df['percent'] = df['amount'] / total
    return df[df['percent'] > threshold].sort_values('percent', ascending=False)


def calculate_support_resistance(order_book, levels=3):
    """Поиск ключевых уровней поддержки/сопротивления"""
    bids = pd.DataFrame(order_book['bids'], columns=['price', 'amount'])
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'amount'])

    return {
        'support': bids.nlargest(levels, 'amount').to_dict('records'),
        'resistance': asks.nlargest(levels, 'amount').to_dict('records')
    }


def volume_statistics(order_book):
    """Анализ объёмов: мин/макс/среднее"""
    bids = pd.DataFrame(order_book['bids'], columns=['price', 'amount'])
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'amount'])
    all_orders = pd.concat([bids, asks])

    return {
        'max_volume': all_orders['amount'].max(),
        'min_volume': all_orders['amount'].min(),
        'avg_volume': all_orders['amount'].mean()
    }
