import stock
import plotter
import pandas as pd

stockNo = '2454'
startYear, startMonth, endYear, endMonth = 2022, 12, 2023, 11

# stockNo     = input("請輸入股票代號： ")
# startYear   = int(input("請輸入起始年份： "))
# startMonth  = int(input("請輸入起始月份： "))
# endYear     = int(input("請輸入結束年份： "))
# endMonth    = int(input("請輸入結束月份： "))
print("尋找資料中，請稍後...")

file_name = "{:s}_{:d}{:02d}_{:d}{:02d}.csv".format(stockNo, startYear%100, startMonth, endYear%100, endMonth)

try: # check if the file is exist
    pd.read_csv(file_name)
    print('檔案已儲存在 ./' + file_name)
except: # if not, then get the file
    stock.get_stock(stockNo, startYear, startMonth, endYear, endMonth, '.')

plotter.plot_stock(file_name)