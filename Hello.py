import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import ta
import streamlit as st

# Title of your app
st.title('BTC Analysis with RSI and EMA')

# User input for Len and Len_EMA
len = st.number_input('Input Len:', min_value=1,
                      value=14)  # Default value set to 14
len_ema = st.number_input('Input Len_EMA:', min_value=1,
                          value=10)  # Default value set to 10

# Download BTC data
btc_df = yf.download("BTC-USD", start="2018-01-01")

# Calculate RSI
btc_df['rsi'] = ta.momentum.RSIIndicator(btc_df['Close'], window=len).rsi()

# Calculate EMA of RSI
btc_df['rsi_ema'] = ta.trend.EMAIndicator(
    btc_df['rsi'], window=len_ema).ema_indicator()

# Conditions for Long and Short
btc_df['rsi_long'] = btc_df['rsi_ema'] > 50
btc_df['rsi_short'] = btc_df['rsi_ema'] < 50

# Plotting
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plotting the closing price of BTC-USD
axes[0].plot(btc_df.index, btc_df['Close'],
             label='BTCUSD Close Price', color='black')
axes[0].set_yscale('log')
axes[0].set_title('BTCUSD Close Price and RSI EMA Indicator')
axes[0].legend()

# Highlighting the areas where conditions are met
axes[0].fill_between(btc_df.index, btc_df['Close'], where=btc_df['rsi_long'],
                     color='green', alpha=0.3, label='Long Condition Met')
axes[0].fill_between(btc_df.index, btc_df['Close'], where=btc_df['rsi_short'],
                     color='red', alpha=0.3, label='Short Condition Met')

# Plotting RSI and its EMA on the second subplot
axes[1].plot(btc_df.index, btc_df['rsi'], label='RSI', color='#8F00FF')
axes[1].plot(btc_df.index, btc_df['rsi_ema'],
             label='EMA of RSI', color='orange', linestyle='-')
axes[1].hlines(50, btc_df.index[0], btc_df.index[-1],
               colors='grey', linestyles='--')

axes[1].set_title('RSI and EMA of RSI')
axes[1].legend()

# Showing the plot in Streamlit
st.pyplot(fig)
