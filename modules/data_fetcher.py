
import ccxt
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_order_book(pair='BTC/USDT', limit=100):
    """Получение стакана ордеров с Binance через REST API"""
    try:
        exchange = ccxt.binance()
        return exchange.fetch_order_book(pair, limit)
    except Exception as e:
        logger.error(f"Ошибка получения данных через REST: {e}")
        return None
