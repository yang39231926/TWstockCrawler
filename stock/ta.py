import pandas as pd
import numpy as np

def get_MA(price, n, l):
    ma = 0.0
    mas = []
    for i in range(n):
        ma += price[i]
        mas.append(ma/(i+1))

    for i in range (n, l):
        ma += price[i] - price[i-n]
        mas.append(ma/n)
    return mas

def get_RSI(change, n, l):
    up, down = 0.0, 0.0
    rsi = []
    for i in range(n-1):
        rsi.append(0.0)
        if change[i] > 0:
            up += change[i]
        else:
            down += change[i]

    for i in range (n-1, l):
        if change[i] > 0:
            up += change[i]
        else:
            down += change[i]

        rsi.append(100 * up / (up - down)) # down < 0

        if change[i-n+1] > 0:
            up -= change[i-n+1]
        else:
            down -= change[i-n+1]

    return rsi

def get_RSV(data, n):
    rsv = [0.0 for _ in range(n-1)]
    # n_low, n_high = 0.0, 0.0
    for i in range(n-1, data.shape[0]):
        n_low = min(data['Low'][i-n+1:i+1])
        n_high = max(data['High'][i-n+1:i+1])
        rsv.append(100 * (data['Close'][i] - n_low) / (n_high - n_low))

    return rsv

def get_KD(data, n) -> dict:
    rsv = get_RSV(data, n)
    k = [0 for _ in range(n-1)]
    d = [0 for _ in range(n-1)]

    for i in range(n-1, data.shape[0]):
        k.append((2*k[i-1]+rsv[i])/3)
        d.append((2*d[i-1]+k[i])/3)

    return {'K': k, 'D': d}

def get_DIF(price, short, long, l):
    ma_short = get_MA(price, short, l)
    ma_long = get_MA(price, long, l)
    dif = np.subtract(ma_short, ma_long)
    return dif

def get_MACD(dif, n, l):
    macd = get_MA(dif, n, l)
    return macd

def get_analysis(data):
    l = data.shape[0]
    data['MA5'] = get_MA(data['Close'], 5, l)
    data['MA20'] = get_MA(data['Close'], 20, l)
    data['MA60'] = get_MA(data['Close'], 60, l)
    data['RSI'] = get_RSI(data['Change'], 14, l)
    kd = get_KD(data, 14)
    data['K'] = kd['K']
    data['D'] = kd['D']
    data['DIF'] = get_DIF(data['Close'], 12, 26, l)
    data['MACD'] = get_MACD(data['DIF'], 9, l)

    return data
