
import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_order_book(order_book, pair='BTC/USDT', save_path=None):
    """Построение и сохранение графика стакана ордеров"""
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

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
