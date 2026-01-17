import ccxt

def conectar_exchange(exchange_id='binance'):
    try:
        exchange_class = getattr(ccxt, exchange_id)
        return exchange_class()
    except AttributeError:
        return None

def fetch_ohlcv_raw(exchange, simbolo, temporalidad, limite):
    return exchange.fetch_ohlcv(simbolo, timeframe=temporalidad, limit=limite)