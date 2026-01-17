import streamlit as st
import pandas as pd
from src.connector import conectar_exchange, fetch_ohlcv_raw
from src.proccessor import procesar_datos_ohlcv
from src.indicators import agregar_indicadores_basicos, obtener_señal

# Configuración de la interfaz para el usuario
st.set_page_config(page_title="Crypto Bot Pro", layout="wide")

st.title("📊 Crypto Assistant")
st.markdown("""
Configura los parámetros en el panel de la izquierda y presiona **Analizar Mercado**.
""")

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.header("Configuración")
    ex_id = st.selectbox("Exchange", ["binance", "kraken", "coinbase", "bitfinex"])
    symbol = st.text_input("Símbolo (Par)", value="BTC/USDT")
    tf = st.selectbox("Temporalidad", ["1m", "5m", "15m", "1h", "4h", "1d"], index=3)
    # Recomendamos al menos 50 velas para que los indicadores (SMA 20) tengan datos
    limit = st.slider("Cantidad de velas", 50, 1000, 100)
    
    boton_ejecutar = st.button("🚀 Analizar Mercado")

# --- FLUJO PRINCIPAL ---
if boton_ejecutar:
    with st.spinner(f'Obteniendo datos de {ex_id}...'):
        # 1. Conexión y Descarga
        exchange = conectar_exchange(ex_id)
        raw_data = fetch_ohlcv_raw(exchange, symbol, tf, limit)
        
        # 2. Procesamiento con Type Hint para evitar quejas de VS Code
        # Le decimos explícitamente que esto será un DataFrame o None
        df: pd.DataFrame = procesar_datos_ohlcv(raw_data)
        
        # Verificamos que el DataFrame exista y tenga datos
        if df is not None and not df.empty:
            
            # 3. Cálculo de Indicadores
            df = agregar_indicadores_basicos(df)
            
            # --- SECCIÓN 1: RECOMENDACIÓN ---
            st.divider()
            texto_señal, color_señal = obtener_señal(df)
            
            st.subheader("🤖 Recomendación del Asistente")
            if color_señal == "green": st.success(texto_señal)
            elif color_señal == "red": st.error(texto_señal)
            elif color_señal == "orange": st.warning(texto_señal)
            else: st.info(texto_señal)

            # --- SECCIÓN 2: MÉTRICAS CLAVE ---
            col1, col2, col3 = st.columns(3)
            # .iloc[-1] accede al último valor (el más reciente)
            precio_act = df['close'].iloc[-1]
            rsi_act = df['RSI_14'].iloc[-1]
            
            col1.metric("Precio Actual", f"{precio_act:,.2f} USDT")
            col2.metric("RSI (Fuerza de Mercado)", f"{rsi_act:.2f}")
            col3.metric("Puntos Analizados", len(df))

            # --- SECCIÓN 3: GRÁFICO VISUAL ---
            st.subheader("Gráfico de Tendencia (Precio vs Media Móvil)")
            
            # Limpiamos filas con valores vacíos para que el gráfico no empiece en cero
            df_plot = df.dropna(subset=['SMA_20']).copy()
            
            if not df_plot.empty:
                # Establecemos el tiempo como índice para que Streamlit lo use en el eje X
                df_plot = df_plot.set_index('timestamp')
                st.line_chart(df_plot[['close', 'SMA_20']])
            else:
                st.warning("Aún no hay suficientes datos para mostrar la línea de tendencia (SMA).")

            # --- SECCIÓN 4: DESCARGA DE DATOS ---
            with st.expander("Ver tabla de datos y opciones de exportación"):
                st.dataframe(df.tail(30), use_container_width=True)
                
                # Preparamos el CSV. Aquí df ya está garantizado que no es None por el 'if' inicial.
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar datos en CSV",
                    data=csv_data,
                    file_name=f"{symbol.replace('/','_')}.csv",
                    mime='text/csv',
                )
        else:
            st.error(f"No se encontraron datos para {symbol}. Revisa si el exchange soporta este par o si el formato es correcto.")

st.divider()