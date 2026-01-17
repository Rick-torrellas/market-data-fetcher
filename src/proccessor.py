import pandas as pd

def procesar_datos_ohlcv(ohlcv_crudo):
    if not ohlcv_crudo:
        return None
    columnas = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(ohlcv_crudo, columns=columnas)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df