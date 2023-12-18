import pandas as pd
import mplfinance as mpf

def plot_stock(filePath: str):
    # input file
    data = pd.read_csv(filePath, index_col='Date')
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d') # let index be date type
    osc = data['DIF']-data['MACD']
    ap = [mpf.make_addplot(data['MA5'], color='#FF4500', label='5MA'),
          mpf.make_addplot(data['MA20'], color='#9370DB', label='20MA'),
          mpf.make_addplot(data['MA60'], color='#1E90FF', label='60MA'),
          mpf.make_addplot(data['K'], color='orange', panel=2, ylabel='KD', label='K'),
          mpf.make_addplot(data['D'], color='#00BFFF', panel=2, label='D'),          
          mpf.make_addplot(osc, type='bar', panel=3, width=0.7, alpha=1, color=['red' if i > 0 else 'green' for i in osc], ylabel='OSC'),
          mpf.make_addplot(data['MACD'], color='orange', panel=3, label='MACD', ylabel='MACD'),
          mpf.make_addplot(data['DIF'], color='#7B68EE', panel=3, label='DIF'),]
    mystyle = mpf.make_mpf_style(base_mpf_style='binance', marketcolors=mpf.make_marketcolors(up='red', down='green', inherit=True)) # let the color be red and green
    mpf.plot(data, type = 'candle', style=mystyle, volume=True, addplot=ap) # draw