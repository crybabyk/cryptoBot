import matplotlib.pyplot as plt
import pandas as pd


def show_order_book(order_book, pair='BTC/USDT'):
    """Отображение стакана ордеров"""
    if not order_book:
        return

    bids = pd.DataFrame(order_book['bids'], columns=['price', 'amount'])
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'amount'])

    plt.figure(figsize=(10, 6))
    plt.bar(bids['price'], bids['amount'], color='green', label='Bids')
    plt.bar(asks['price'], asks['amount'], color='red', label='Asks')
    plt.title(f'Order Book: {pair}')
    plt.xlabel('Price')
    plt.ylabel('Amount')
    plt.legend()
    plt.show()