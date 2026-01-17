import pandas as pd

def calcular_sma(df, periodo=20):
    """Calcula la Media Móvil Simple."""
    return df['close'].rolling(window=periodo).mean()

def calcular_rsi(df, periodo=14):
    """Calcula el Relative Strength Index (RSI)."""
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    
    # Evitar división por cero
    loss = loss.replace(0, 0.000001)
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def obtener_señal(df):
    """
    Analiza el RSI y el precio para dar una recomendación simple.
    Retorna: (mensaje, color_bootstrap)
    """
    if df is None or len(df) < 2:
        return "Esperando datos...", "gray"
    
    ultimo_rsi = df['RSI_14'].iloc[-1]
    precio_actual = df['close'].iloc[-1]
    sma = df['SMA_20'].iloc[-1]
    
    # Lógica de señales para el usuario
    if ultimo_rsi < 35 and precio_actual > sma:
        return "🚀 SEÑAL DE COMPRA: Activo en zona de descuento y tendencia alcista.", "green"
    elif ultimo_rsi > 70:
        return "⚠️ PRECAUCIÓN: Zona de sobrecompra (posible caída).", "red"
    elif precio_actual < sma:
        return "📉 TENDENCIA BAJISTA: El precio está por debajo de la media móvil.", "orange"
    else:
        return "⚖️ MERCADO NEUTRAL: No hay señales claras en este momento.", "blue"

def agregar_indicadores_basicos(df):
    """Añade los indicadores al DataFrame original sin modificarlo."""
    if df is None or df.empty:
        return None
    
    df = df.copy()
    df['SMA_20'] = calcular_sma(df, 20)
    df['RSI_14'] = calcular_rsi(df, 14)
    
    return df