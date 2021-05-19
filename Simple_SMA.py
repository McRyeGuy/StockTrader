import yfinance as yf
import pandas as pd
import numpy as np
from multiprocessing import Process
from datetime import datetime
import time



def DestionMaker(stockname):
    df = yf.download(stockname, period="2d", interval="1m")

    AAPL = df.reset_index()



    SMA100=pd.DataFrame()
    SMA100['Adj Close Price'] = AAPL['Close'].rolling(window=25).mean()

    data=pd.DataFrame()
    data['AAPL']=AAPL['Adj Close'] #SMA5
    data['SMA100']=SMA100

    #Buy or Sell
    def buy_sell(data):
        sigPriceBuy=[]
        sigPriceSell=[]
        flag=-1

        for i in range(len(data)):
            if data['SMA100'][i]<data['AAPL'][i] and flag!=1:
                #BUY
                sigPriceBuy.append(data['AAPL'][i])
                sigPriceSell.append(np.nan)
                flag=1
            elif data['SMA100'][i]>data['AAPL'][i] and flag!=0:
                #SELL
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['AAPL'][i])
                flag=0

            else:
                sigPriceSell.append(np.nan)
                sigPriceBuy.append(np.nan)

        return (sigPriceBuy,sigPriceSell)
    buy_sell=buy_sell(data)
    data['Buy']=buy_sell[0]
    data['Sell']=buy_sell[1]
    return data



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

def TradeLive(stockname):
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    df = DestionMaker(stockname=stockname)
    buyandselldata = pd.DataFrame(columns = ['DateTime','Buy or Sell', 'Price','StockName','total','subtotal','buyprice','sellprice','buynum','sellnum','tradenum','marker'])
    def buy_or_sell(*args):

        for i in range(len(df)-1,0,-1):
            if df['Buy'][i] > 0:
                buyorsell = 1
                break

            if df['Sell'][i]>0:
                buyorsell = 0
                break

        return buyorsell


    #GET Yesterdays Data
    yesterdaysdata = pd.read_csv('STONKS.csv')

    total = yesterdaysdata["total"].iloc[-1]
    subtotal = yesterdaysdata["subtotal"].iloc[-1]
    buyprice = yesterdaysdata["buyprice"].iloc[-1]
    sellprice = yesterdaysdata["sellprice"].iloc[-1]
    buynum = yesterdaysdata["buynum"].iloc[-1]
    sellnum = yesterdaysdata["sellnum"].iloc[-1]
    tradenum = yesterdaysdata["tradenum"].iloc[-1]
    marker = yesterdaysdata["marker"].iloc[-1]

    #REFRESH PAST DATA
    df = DestionMaker(stockname=stockname)
    buyorsell=buy_or_sell()
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    current_time = int(current_time)
    date_object = datetime.now()
    # REFRESH PAST DATA

    if buyorsell>0 and marker != 1:
        print('BUY')
        buyprice=df['AAPL'][df.index[len(df)-1]]
        buynum=1
        tradenum=tradenum+1
        marker=1
        buyandselldata.loc[len(df.index)] = [date_object, 'BUY', buyprice, stockname, total, subtotal, buyprice,
                                                 sellprice, buynum, sellnum, tradenum, marker]

    if buyorsell<1 and marker != 0 and buyprice>0:
        sellprice=df['AAPL'][df.index[len(df)-1]]
        sellnum=1
        print('Sell')
        marker=0
        tradenum = tradenum + 1
        buyandselldata.loc[len(df.index)] = [date_object, 'Sell', sellprice, stockname, total, subtotal, buyprice,
                                                 sellprice, buynum, sellnum, tradenum, marker]

    if buynum>0 and sellnum>0:
        subtotal=sellprice-buyprice
        total=total+subtotal
        buynum=0
        sellnum=0
        buyandselldata.loc[len(df.index)] = [date_object, 'Sell', sellprice, stockname, total, subtotal, buyprice,
                                                 sellprice, buynum, sellnum, tradenum, marker]

    print('Stock mame is '+str(stockname))
    print('Current price $'+str(df['AAPL'][df.index[len(df)-1]]))
    print('Current Time '+str(current_time))
    print('Number of Trades: '+str(tradenum))
    print('Current Profit $'+str(total))
    print('-------------------------------------')
    buyandselldata.to_csv('STONKS.csv', index=False, mode='a',header=None)
    del buyandselldata
    buyandselldata = pd.DataFrame(
        columns=['DateTime', 'Buy or Sell', 'Price', 'StockName', 'total', 'subtotal', 'buyprice', 'sellprice',
                     'buynum', 'sellnum', 'tradenum', 'marker'])


    return total

#RUNNING CODE



if datetime.today().isoweekday() == 1 or datetime.today().isoweekday() == 2 or datetime.today().isoweekday() == 3 \
        or datetime.today().isoweekday() == 4 or datetime.today().isoweekday() == 5:

    for i in range(1000):
        TradeLive("BTC-USD")
        time.sleep(60)

else:
    print('#---Weekend---#')