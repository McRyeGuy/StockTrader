import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from multiprocessing import Process
from datetime import datetime
import time

def DestionMaker(stockname):
    df = yf.download(stockname, period="5d", interval="1m")

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
            if data['SMA100'][i]<data['AAPL'][i]: # and flag!=1:
                #BUY
                sigPriceBuy.append(data['AAPL'][i])
                sigPriceSell.append(np.nan)
                flag=1
            elif data['SMA100'][i]>data['AAPL'][i]: #and flag!=0:
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
    tradenum=0
    while True:#current_time<180000:

        #REFRESH PAST DATA
        df = DestionMaker(stockname=stockname)
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
            tradenum=tradenum+1
            flag=1
        if buyorsell<1 and flag != 0 and buyprice>0:
            sellprice=df['AAPL'][df.index[len(df)-1]]
            buyandselldata.loc[len(df.index)] = [date_object,'Sell', sellprice, stockname,subtotal,total]
            sellnum=1
            print('Sell')
            flag=0
            tradenum = tradenum + 1
        if buynum>0 and sellnum>0:
            subtotal=sellprice-buyprice
            total=total+subtotal
            buynum=0
            sellnum=0
        print('Stock mame is '+str(stockname))
        print('Current price $'+str(df['AAPL'][df.index[len(df)-1]]))
        print('Current Time '+str(current_time))
        print('Number of Trades: '+str(tradenum))
        print('Current Profit $'+str(total))
        print('-------------------------------------')
        time.sleep(15)

    buyandselldata.to_csv('STONKS.csv', index=False, mode='a',header=None)
    return total
def Trade_LIVE_Multi():
    #makes you money much faster and makes code really complated

    if __name__ == "__main__":
        print('')
        print('  /$$$$$$    /$$                            /$$')
        print(' /$$__  $$  | $$                           | $$')
        print('| $$  \__/ /$$$$$$     /$$$$$$    /$$$$$$$ | $$   /$$  /$$$$$$$')
        print('|  $$$$$$ |_  $$_/    /$$__  $$  /$$_____/ | $$  /$$/ /$$_____/')
        print(' \____  $$  | $$     | $$  \ $$ | $$       | $$$$$$/ |  $$$$$$')
        print(' /$$  \ $$  | $$ /$$ | $$  | $$ | $$       | $$_  $$  \____  $$')
        print('|  $$$$$$/  |  $$$$/ |  $$$$$$/ |  $$$$$$$ | $$ \  $$ /$$$$$$$/')
        print(' \______/    \____/   \______/   \_______/ |__/  \__/ _______/')
        print('Created by: Ryan Krueger')
        print('"Make your friends rich and your enemies rich and wait to see which is which"')
        print('')
        print('')

        p1= Process(target=TradeLive,args=['XLM-USD'])
        p2 = Process(target=TradeLive,args=['LINK-USD'])
        p3 = Process(target=TradeLive, args=['DOT1-USD'])
        p4 = Process(target=TradeLive, args=['USDT-USD'])
        p5 = Process(target=TradeLive, args=['ETH-USD'])
        p6 = Process(target=TradeLive, args=['DOGE-USD'])
        p7 = Process(target=TradeLive, args=['BTC-USD'])

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()

Trade_LIVE_Multi()
