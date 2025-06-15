import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import ta

# Judul
st.title("Visualisasi dan Edukasi Indikator Teknikal (RSI, Stochastic, MA, MACD, SAR)")

# Input saham
ticker = st.text_input("Masukkan simbol saham (misal: BTC-USD)", value="BTC-USD")

# Pilih rentang waktu
period = st.selectbox("Pilih periode data", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)
interval = st.selectbox("Pilih interval", ["1d", "1h", "15m"], index=0)

# Unduh data
data = yf.download(ticker, period=period, interval=interval)

if not data.empty:
    st.subheader("Data Harga Historis")
    st.line_chart(data['Close'])

    # Hitung indikator teknikal
    rsi = ta.momentum.RSIIndicator(close=data['Close']).rsi()
    stoch = ta.momentum.StochasticOscillator(high=data['High'], low=data['Low'], close=data['Close'])
    stoch_k = stoch.stoch()
    stoch_d = stoch.stoch_signal()
    macd = ta.trend.MACD(close=data['Close'])
    sar = ta.trend.PSARIndicator(high=data['High'], low=data['Low'], close=data['Close'])
    
    # Moving averages
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()

    # Plot RSI
    st.subheader("RSI")
    fig, ax = plt.subplots()
    ax.plot(rsi, label='RSI', color='purple')
    ax.axhline(70, color='red', linestyle='--', label='Overbought')
    ax.axhline(30, color='green', linestyle='--', label='Oversold')
    ax.set_title("Relative Strength Index")
    ax.legend()
    st.pyplot(fig)

    # Plot Stochastic
    st.subheader("Stochastic Oscillator")
    fig, ax = plt.subplots()
    ax.plot(stoch_k, label='%K', color='lime')
    ax.plot(stoch_d, label='%D', color='orange')
    ax.axhline(80, color='red', linestyle='--', label='Overbought')
    ax.axhline(20, color='green', linestyle='--', label='Oversold')
    ax.legend()
    st.pyplot(fig)

    # Plot MACD
    st.subheader("MACD")
    fig, ax = plt.subplots()
    ax.plot(macd.macd(), label='MACD', color='blue')
    ax.plot(macd.macd_signal(), label='Signal Line', color='red')
    ax.bar(data.index, macd.macd_diff(), label='Histogram', color='gray', alpha=0.3)
    ax.legend()
    st.pyplot(fig)

    # Plot Moving Averages
    st.subheader("Moving Averages")
    fig, ax = plt.subplots()
    ax.plot(data['Close'], label='Close')
    ax.plot(data['SMA50'], label='SMA 50', linestyle='--')
    ax.plot(data['SMA200'], label='SMA 200', linestyle='--')
    ax.legend()
    st.pyplot(fig)

    # Plot Parabolic SAR
    st.subheader("Parabolic SAR")
    fig, ax = plt.subplots()
    ax.plot(data['Close'], label='Close')
    ax.plot(sar.psar(), marker='.', linestyle='', label='Parabolic SAR', color='red')
    ax.legend()
    st.pyplot(fig)

    # Ringkasan
    st.markdown("""
    ### Penjelasan Singkat:
    - **RSI < 30**: kemungkinan oversold (peluang naik).
    - **Stochastic < 20**: oversold, tapi lebih sensitif dari RSI.
    - **MACD cross up**: sinyal beli.
    - **Golden Cross** (SMA50 naik lewati SMA200): sinyal tren naik.
    - **SAR di bawah harga**: tren naik.
    """)

else:
    st.error("Data tidak tersedia. Coba simbol lain atau ubah periode.")
