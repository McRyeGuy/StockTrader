import warnings
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
import threading
from multiprocessing import Process

plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')







def SMA(pastdays,stockname):
    df = yf.download(stockname, period="3d", interval="1m")
    AAPL = df.reset_index()
    # ratio
    """
    SMA30=3
    SMA100=20
    SMA10=5
    """

    SMA30 = pd.DataFrame()
    SMA100 = pd.DataFrame()
    SMA10 = pd.DataFrame()
    SMA30['Adj Close Price'] = AAPL['Close'].rolling(window=30).mean()
    SMA100['Adj Close Price'] = AAPL['Close'].rolling(window=200).mean()
    SMA10['Adj Close Price'] = AAPL['Close'].rolling(window=5).mean()

    data = pd.DataFrame()
    data['AAPL'] = AAPL['Close']
    data['SMA10'] = SMA10
    data['SMA30'] = SMA30
    data['SMA100'] = SMA100

    # Buy or Sell
    def buy_sell(data):
        sigPriceBuy = []
        sigPriceSell = []
        flag = -1

        for i in range(len(data)):

            # Test Past Data
            buy = -1
            sell = -1
            for x in range(pastdays):

                if data['AAPL'][i - x] < data['SMA100'][i - x] and data['AAPL'][i - x] < data['SMA30'][i - x]:

                    sell = 1

                else:
                    sell = -1
                    break

            for x in range(pastdays):
                if data['AAPL'][i - x] > data['SMA100'][i - x] and data['AAPL'][i - x] > data['SMA30'][i - x]:
                    buy = 1

                else:
                    buy = -1
                    break

            if data['AAPL'][i] < data['SMA100'][i] and data['SMA30'][i] < data['AAPL'][
                i] and flag != 1 or buy == 1 and flag != 1:  # BUY
                sigPriceBuy.append(data['AAPL'][i])
                sigPriceSell.append(np.nan)
                flag = 1

            elif data['AAPL'][i] > data['SMA100'][i] and data['SMA30'][i] > data['AAPL'][
                i] and flag != 0 or sell == 1 and flag != 0:  # SELL
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['AAPL'][i])
                flag = 0
            else:
                sigPriceSell.append(np.nan)
                sigPriceBuy.append(np.nan)

        return (sigPriceBuy, sigPriceSell)

    buy_sell = buy_sell(data)
    data['Buy'] = buy_sell[0]
    data['Sell'] = buy_sell[1]
    # add data to larger df
    return data

    # Plot
    plt.figure(figsize=(12.5, 4.5))
    plt.plot(data['AAPL'], label='AAPL', alpha=0.35)
    plt.plot(data['SMA30'], label='SMA30', alpha=0.35)
    plt.plot(data['SMA100'], label='SMA100', alpha=0.35)
    plt.plot(data['SMA10'], label='SMA10', alpha=0.35)
    plt.scatter(data.index, data['Buy_Signal_Price'], label="Buy", marker='^', color='green')
    plt.scatter(data.index, data['Sell_Signal_Price'], label="Sell", marker='v', color='red')
    plt.title('SMA Buy or Sell')
    plt.xlabel('Date')
    plt.ylabel9 = ('Adj Close Price')
    plt.legend(loc='upper left')
    plt.show()


def Profit(data):
    df = data
    find_buy = 0
    find_sell = 0
    buy = 0
    sell = 0
    total_profit = 0
    for i in range(0, len(df)):
        if df['Buy'][i] > 0 and find_buy == 0:
            find_buy = 1
            buy = df['Buy'][i]
        if find_buy == 1:
            if df['Sell'][i] > 0 and find_sell == 0:
                find_sell = 1
                sell = df['Sell'][i]
        if find_buy == 1 and find_sell == 1:
            subtotal = sell - buy
            total_profit = total_profit + subtotal
            find_buy = 0
            find_sell = 0

    return total_profit

def Calcuate_PastDays(stockname):
    profitvalues=[]
    for i in range(25):
        data = SMA(i,stockname)
        profitvalues.append(Profit(data))
    profitvalues=np.array(profitvalues)
    df = pd.DataFrame(profitvalues, columns= ['Price'])
    max_value = df['Price'].max()
    df=df[df['Price'] == max_value].index.values
    df=df.astype(np.int)
    return df

def Trade_LIVE(stockname):
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    x = int(Calcuate_PastDays(stockname))
    df = SMA(pastdays=x,stockname=stockname)
    buyandselldata = pd.DataFrame(columns = ['DateTime','Buy or Sell', 'Price','StockName','MovingProfit','RunningTotal'])
    def buy_or_sell(*args):

        for i in range(len(df)-1,0,-1):
            if df['Buy'][i] > 0:
                buyorsell = 1
                break

            if df['Sell'][i]>0:
                buyorsell = 0
                break

        return buyorsell
    total=0
    subtotal=0
    buyprice=0
    sellprice=0
    buynum=-1
    sellnum=-1
    flag=-1
    current_time=int(current_time)
    while current_time<163000:
        #REFRESH PAST DATA
        df = SMA(pastdays=x,stockname=stockname)
        buyorsell=buy_or_sell()
        now = datetime.now()
        current_time = now.strftime("%H%M%S")
        current_time = int(current_time)
        date_object = datetime.now()
        # REFRESH PAST DATA

        if buyorsell>0 and flag != 1:
            print('BUY')
            buyprice=df['AAPL'][df.index[len(df)-1]]
            buyandselldata.loc[len(df.index)] = [date_object,'BUY',buyprice,stockname,subtotal,total]
            buynum=1
            flag=1
        if buyorsell<1 and flag != 0 and buyprice>0:
            sellprice=df['AAPL'][df.index[len(df)-1]]
            buyandselldata.loc[len(df.index)] = [date_object,'Sell', sellprice, stockname,subtotal,total]
            sellnum=1
            print('Sell')
            flag=0
        if buynum>0 and sellnum>0:
            subtotal=sellprice-buyprice
            total=total+subtotal
            buynum=0
            sellnum=0
        print('Stock mame is '+str(stockname))
        print('Current price $'+str(df['AAPL'][df.index[len(df)-1]]))
        print('Current Time '+str(current_time))
        print('Current Profit $'+str(total))
        print('Pastdays is '+str(x))
        print('-------------------------------------')
        time.sleep(25)

    buyandselldata.to_csv('STONKS.csv', index=False, mode='a',header=None)
    print('DONE :)')
    return total

def Top_Stocks():
    table=pd.read_html('https://finance.yahoo.com/gainers/?offset=0&count=5')
    data=table[0]
    data=data['Symbol']
    data=data.to_numpy()
    data=list(data)
    return data #output is a numpy array

def Trade_LIVE_Multi():
    #makes you money much faster and makes code really complated
    topstocks=Top_Stocks()
    topstocks=['AAPL','AMZN','GOOGL','JNJ','ABC']

    if __name__ == "__main__":
        p1= Process(target=Trade_LIVE,args=['TSLA'])
        p2 = Process(target=Trade_LIVE,args=['MSFT'])
        p3 = Process(target=Trade_LIVE, args=['JNJ'])
        p4 = Process(target=Trade_LIVE, args=['AAPL'])
        p5 = Process(target=Trade_LIVE, args=['GME'])

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()






Trade_LIVE_Multi()
