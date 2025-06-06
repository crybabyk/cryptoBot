import ccxt

def get_order_book(pair='BTC/USDT', limit=100):
    """Получение стакана ордеров с Binance"""
    try:
        exchange = ccxt.binance()
        return exchange.fetch_order_book(pair, limit)
    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return None