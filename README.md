# 網路爬蟲個股資訊做技術分析並視覺化

## 一、設計此程式的動機
我把這個程式作為我期末報告的動機是因為我想到python這個語言最先想到的是它爬蟲很方便。再加上這門課是在叫做大數據與程式設計導論，老師課堂上也有教到爬蟲。因此我覺得做爬蟲相關程式會很貼合這門課的主題。又因金融相關的資料算是相對容易蒐集到大量數據的領域，本身也對股市有些興趣，也有在買股票。所以最後才把「網路爬蟲個股資訊做技術分析並視覺化」作為我的期末報告，之後看股票也能把這程式拿出來用用。

## 二、程式設計目標
撰寫Python程式，擷取指定期間的個股資訊，並把資料繪製出來。要爬的網站是台灣證交所的個股日收盤價及月平均收盤價(https://www.twse.com.tw/zh/trading/historical/stock-day.html)。進去該網址我發現當我按查詢時，網頁會 request 一個網址(如下圖)：
![image](https://hackmd.io/_uploads/BJPzh26U6.png)

而這個網址(https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=20231218&stockNo=2454)會點進去會是一個 json檔(如下圖)：
![image](https://hackmd.io/_uploads/r1aHn3aLa.png)



我們可以透過更改網址後面的stockNo與date取得不同時間的個股資訊。透過這個方法我只要輸入股票代號以及起訖時間就可以得到不同時間的個股資訊。(下圖為輸入畫面) 
![image](https://hackmd.io/_uploads/BJv83hTIp.png)

若輸入格式無誤則程式會先看這個時段有沒有爬過，有爬過就直接讀檔並繪製個股資訊，沒有的話程式會開始爬蟲，並把結果儲存在目前的目錄底下。(如下圖所示)
![image](https://hackmd.io/_uploads/HJZwhh6LT.png)


最後個股資訊呈現的結果如下圖，圖包含了日K，周、月、三月均線、成交量、KD以及MACD/DIF。
而儲存的資料有每日開/收盤價、每日最高最低價、漲跌、交易量、周、月、三月均線、成交量、KD以及MACD、DIF、RSI。
 
## 三、本程式所使用的套件功能介紹
本程式主要運用6個套件，2個自製套件，功能說明如下：

### ● pandas
用於資料操縱和分析的Python軟體庫。它建造在NumPy基礎上，並為操縱數值表格和時間序列，提供了資料結構和運算操作。在這個程式中我們使用了pandas 中的DataFrame 來存取資料，使用 read_csv() 讀取 csv檔。

### ● json
Python 的標準函式庫之一，提供了操作 json 檔案的方法，可以針對 json 檔案進行讀取、寫入或修改。在這個程式中我們使用它來讀爬蟲下來的json格式網頁。

### ● request
requests 是相當流行的 Python 外部函式庫，它具備了 GET、POST等各種 request 用法，透過 requests 能夠輕鬆抓取網頁的資料。在這個程式中我們使用了其中的 get() 函式，它的功能是向指定資源提交request。

### ● time
Python 的標準函式庫之一。提供不少處理時間的方法，除了可以取得目前的時間或轉換時間，也能夠透過像是 sleep() 的方法將程式暫停。由於我發現在短時間內連續向網頁 request 會被誤判成是駭客攻擊，所以我需要讓程式 request 的頻率降低一些，因此使用了其中的 sleep() 函式。
 
### ● numpy
NumPy是Python語言的一個擴充程式庫。支援高階大規模的多維陣列與矩陣運算，此外也針對陣列運算提供大量的數學函數函式庫。

### ● mplfinance
它是matplotlib(Python 科學繪圖的主要模組)旗下專門用於金融分析的繪圖模組。在我的程式中負責繪製爬下來的個股資訊。

### ● stock
是我自己做的小套件。包含以下幾個函式。


| **函式名稱**      | **功能**                          |
| ----------------- |---------------------------------- |
| get_monthly_stock | 取得特定月份的個股資訊            |
| get_stock         | 取得一段時間的個股資訊            |
| date_convert      | 將民國年轉成西元年                |
| get_analysis      | 輸入個股資料取得多種技術指標      |
| get_MA            | 輸入時間及資料取得相對應的均線    |
| get_RSI           | 輸入時間取得相對應時間為標準的RSI |
| get_RSV           | 輸入時間取得相對應時間為標準的RSV |
| get_KD            | 輸入時間取得相對應時間為標準的KD  |
| get_DIF           | 輸入時間取得相對應時間為標準的DIF |
| get_MACD          | 輸入時間取得相對應時間為準的MACD  |

 
### ● plotter
是我自己做的小套件。包含以下函式。
| **函式名稱** | **功能**     |
| ------------ | ------------ |
| plot_stock   | 繪製個股資訊 |

## 四、程式架構：
```
.
├── stock
│   ├── __init__.py
│   ├── stock.py
│   └── ta.py
├── plotter
│   ├── __init__.py
│   └── plotter.py
└── main.py
```