import argparse
from src.connector import conectar_exchange, fetch_ohlcv_raw
from src.proccessor import procesar_datos_ohlcv

# --- EL MOTOR (La función reusable) ---
def ejecutar_consulta(simbolo='BTC/USDT', temporalidad='1h', limite=20, exchange_id='binance'):
    """
    Esta función es independiente. Tiene sus propios defaults 
    por si la llamas desde otro script de Python.
    """
    exchange = conectar_exchange(exchange_id)
    if not exchange: return None
    
    raw_data = fetch_ohlcv_raw(exchange, simbolo, temporalidad, limite)
    return procesar_datos_ohlcv(raw_data)


# --- LA INTERFAZ (El manejo de la terminal) ---
def main():
    parser = argparse.ArgumentParser()
    
    # Aquí NO es estrictamente necesario poner default si la función ya los tiene,
    # pero se suele poner para que aparezcan en el mensaje de --help
    parser.add_argument('-s', '--symbol', help='Símbolo')
    parser.add_argument('-t', '--timeframe', help='Temporalidad')
    parser.add_argument('-l', '--limit', type=int, help='Límite de velas')

    args = parser.parse_args()

    # Limpiamos los valores None que envía argparse si el usuario no escribe nada
    # Esto permite que la función 'ejecutar_consulta' use SUS PROPIOS valores por defecto
    params = {k: v for k, v in vars(args).items() if v is not None}

    # Llamamos a la función usando "unpacking" de diccionarios (**)
    datos = ejecutar_consulta(**params)
    
    print(datos)

if __name__ == "__main__":
    main()