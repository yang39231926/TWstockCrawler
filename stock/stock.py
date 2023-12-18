import pandas as pd
import json
import requests
import time
from .ta import *

data_key = ['Date', 'Open', 'High', 'Low', 'Close', 'Change', 'Volume', 'Order']

def get_monthly_stock(stockNo, year, month):
    url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={:d}{:02d}01&stockNo={:s}'.format(year, month, stockNo)
    time.sleep(3)
    data = json.loads(requests.get(url).text)['data']
    data = pd.DataFrame(data, columns=['Date', 'Volume', 'CashVolume', 'Open', 'High', 'Low', 'Close', 'Change', 'Order'])
    data = data[data_key]

    for key in data.columns:
        data[key] = data[key].str.replace(',', '')
    data['Change'] = data['Change'].str.replace('X', '')
    data = data.astype('float64', errors='ignore')
    # data['Volume'] = data['Volume']/1000.0
    return data

def date_convert(s): # 民國 to A.C.
    if not '/' in s: return s
    date = s.split('/')
    return f'{int(date[0])+1911}-{date[1]}-{date[2]}'    

def get_stock(stockNo: str, startYear: int, startMonth: int, endYear: int, endMonth: int, path: str):

    # checking input
    if startYear > endYear:
        raise Exception("Invald input: startYear > endYear.")
    elif startYear == endYear and startMonth > endMonth:
        raise Exception("Invald input: startMonth > endMonth while startYear == endYear.")

    file_name = "{:s}_{:d}{:02d}_{:d}{:02d}.csv".format(stockNo, startYear%100, startMonth, endYear%100, endMonth)
    datas = []

    # get data of each months
    if startYear < endYear:
        for m in range(startMonth, 13):
            datas.append(get_monthly_stock(stockNo, startYear, m))

        for y in range(startYear+1, endYear):
            for m in range(1, 13):
                datas.append(get_monthly_stock(stockNo, y, m))

        for m in range(1, endMonth+1):
            datas.append(get_monthly_stock(stockNo, endYear, m))
    else:
        for m in range(startMonth, endMonth+1):
            datas.append(get_monthly_stock(stockNo, endYear, m))
    datas = pd.concat(datas).reset_index()
    datas = datas.drop(['index'], axis=1)
    datas = get_analysis(datas)

    # write file
    with open(f'{path}/{file_name}', 'w') as f:
        title = ''
        for s in datas.columns: title += f'{s},'
        f.write(f'{title[:-1]}\n')
        qlen = datas.shape[1]
        for _, q in enumerate(datas.values):
            f.write(f'{date_convert(q[0])}')
            for j in range(1, qlen): f.write(f',{q[j]}')
            f.write('\n')

    print(f"檔案儲存在 {path}/{file_name}")