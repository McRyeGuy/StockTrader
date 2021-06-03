import yfinance as yf
import time
import pandas as pd
from datetime import datetime


def Run(stockname):
    #---SETTINGS--#
    pricedeviation=1.002
    takeprofit=1.003
    maxsafetyorder=10



    df = yf.download(stockname, period="2d", interval="1m")
    todaydata=pd.DataFrame(columns = ['Date/Time', 'Position','Price','SafetyOrder','Profit'])
    yesterdaysdata= pd.read_csv('DCA.csv')

    lastprice = yesterdaysdata["Price"].iloc[-1]
    lastposition = yesterdaysdata["Position"].iloc[-1]
    lastprofit=yesterdaysdata["Profit"].iloc[-1]
    safetyordernum = yesterdaysdata["SafetyOrder"].iloc[-1]
    currentprice = df['Close'][df.index[len(df)-1]]
    avarageprice=yesterdaysdata['Price'].tail(safetyordernum).mean()
    date_object = datetime.now()

    if safetyordernum==0:
        #First Buy
        print('First Buy')
        newsafetyordernum = 1
        todaydata.loc[len(df.index)] = [date_object, 'BUY', currentprice, newsafetyordernum,lastprofit]

    if currentprice*pricedeviation <= lastprice and safetyordernum < maxsafetyorder:
        #BUY
        newsafetyordernum=safetyordernum+1
        print('Number of safety orders '+str(newsafetyordernum))
        todaydata.loc[len(df.index)] = [date_object,'BUY',currentprice,newsafetyordernum,lastprofit]

    if avarageprice*takeprofit<currentprice:
        #SELL
        profit=currentprice-avarageprice
        print('Profit made $'+str(profit))
        finalprofit=lastprofit+profit
        newsafetyordernum = 0
        todaydata.loc[len(df.index)] = [date_object, 'SELL', currentprice, newsafetyordernum,finalprofit]

    todaydata.to_csv('DCA.csv', index=False, mode='a', header=None)

for i in range(100000):
    Run('BTC-USD')
    time.sleep(60)