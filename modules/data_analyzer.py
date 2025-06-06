import pandas as pd


def find_large_orders(order_book, threshold=0.1):
    """Поиск крупных ордеров (китов)"""
    if not order_book:
        return pd.DataFrame()

    bids = pd.DataFrame(order_book['bids'], columns=['price', 'amount'])
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'amount'])
    df = pd.concat([bids, asks])

    total = df['amount'].sum()
    df['percent'] = df['amount'] / total
    return df[df['percent'] > threshold].sort_values('percent', ascending=False)


def find_key_levels(order_book, levels=3):
    """Поиск ключевых уровней поддержки/сопротивления"""
    bids = pd.DataFrame(order_book['bids'], columns=['price', 'amount'])
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'amount'])

    return {
        'support': bids.nlargest(levels, 'amount').to_dict('records'),
        'resistance': asks.nlargest(levels, 'amount').to_dict('records')
    }