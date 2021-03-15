import warnings
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from datetime import datetime
plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')

stockname="JNJ"

total_df=yf.download(stockname, period="1000d", interval="1d")
total_df.to_csv ('STONKS.csv', index = False, header=True)


#Define Indcators

def SMA(*args):
    df = yf.download(stockname, period="1000d", interval="1d")

    AAPL=df


    SMA30=pd.DataFrame()
    SMA100=pd.DataFrame()
    SMA30['Adj Close Price']=AAPL['Adj Close'].rolling(window=30).mean()
    SMA100['Adj Close Price'] = AAPL['Adj Close'].rolling(window=100).mean()

    data=pd.DataFrame()
    data['AAPL']=AAPL['Adj Close']
    data['SMA30']=SMA30
    data['SMA100']=SMA100

    #Buy or Sell
    def buy_sell(data):
        sigPriceBuy=[]
        sigPriceSell=[]
        flag=-1

        for i in range(len(data)):
            if data['SMA30'][i]<data['SMA100'][i]:
                if flag!=1:
                    sigPriceBuy.append(data['AAPL'][i])
                    sigPriceSell.append(np.nan)
                    flag=1
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            elif data['SMA30'][i]>data['SMA100'][i]:
                if flag!=0:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(data['AAPL'][i])
                    flag=0
                else:
                    sigPriceSell.append(np.nan)
                    sigPriceBuy.append(np.nan)
            else:
                sigPriceSell.append(np.nan)
                sigPriceBuy.append(np.nan)

        return (sigPriceBuy,sigPriceSell)
    buy_sell=buy_sell(data)
    data['Buy_Signal_Price']=buy_sell[0]
    data['Sell_Signal_Price']=buy_sell[1]
    #add data to larger df
    total_df['SMA Buy'] = buy_sell[0]
    total_df['SMA Sell'] = buy_sell[1]
    return total_df


    #Plot
    plt.figure(figsize=(12.5, 4.5))
    plt.plot(data['AAPL'], label='AAPL',alpha=0.35)
    plt.plot(data['SMA30'], label='SMA30',alpha=0.35)
    plt.plot(data['SMA100'], label='SMA100',alpha=0.35)
    plt.scatter(data.index,data['Buy_Signal_Price'], label="Buy",marker='^',color='green')
    plt.scatter(data.index, data['Sell_Signal_Price'], label="Sell", marker='v', color='red')
    plt.title('SMA Buy or Sell')
    plt.xlabel('Date')
    plt.ylabel9=('Adj Close Price')
    plt.legend(loc='upper left')
    plt.show()



def Bollinger_Lines(*args):
    df = yf.download(stockname, period="1000d", interval="1d")
    period = 20
    df['SMA'] = df['Close'].rolling(window=period).mean()
    df['STD'] = df['Close'].rolling(window=period).std()
    df['Upper'] = df['SMA'] + (df['STD'] * 2)
    df['Lower'] = df['SMA'] - (df['STD'] * 2)

    column_list = ['Close', 'SMA', 'Upper', 'Lower']
    new_df=df[period-1:]

    def get_signal(data):
        buy_signal=[]
        sell_signal=[]

        for i in range(len(data['Close'])):
            if data['Close'][i]>data['Upper'][i]:
                buy_signal.append(np.nan)
                sell_signal.append(data['Close'][i])
            elif data['Close'][i]<data['Lower'][i]:
                buy_signal.append(data['Close'][i])
                sell_signal.append(np.nan)
            else:
                buy_signal.append(np.nan)
                sell_signal.append(np.nan)

        return (buy_signal,sell_signal)

    new_df['Boll Buy']=get_signal(new_df)[0]
    new_df['Boll Sell']=get_signal(new_df)[1]
    #add data to larger df

    return new_df

    #Plot Data
    fig=plt.figure(figsize=(12.2,6.4))
    ax=fig.add_subplot(1,1,1)
    x_axis=new_df.index
    ax.fill_between(x_axis,new_df['Upper'], new_df['Lower'], color='grey')
    #
    ax.plot(x_axis,new_df['Close'], color='gold', lw=3,label='Close Price',alpha=0.5)
    ax.plot(x_axis, new_df['SMA'], color='blue', lw=3, label='Simple Moving Average', alpha=0.5)
    ax.scatter(x_axis, new_df['Boll Buy'], color='green', lw=3, label='Buy', marker='^', alpha=1)
    ax.scatter(x_axis, new_df['Boll Sell'], color='red', lw=3, label='Sell', marker='v', alpha=1)
    ax.set_title('Bollinger Band')
    ax.set_xlabel('Date')
    ax.set_ylabel('USD Price')
    plt.xticks(rotation=45)
    ax.legend()
    plt.show()

def RSI(*args):
    FB=yf.download(stockname, period="1000d", interval="1d")
    delta=FB['Adj Close'].diff(1)
    delta=delta.dropna()
    up=delta.copy()
    dowm=delta.copy()
    up[up<0]=0
    dowm[dowm>0]=0
    period =14
    AVG_Gain=up.rolling(window=period).mean()
    AVG_Loss=abs(dowm.rolling(window=period).mean())
    RS=AVG_Gain/AVG_Loss
    RSI=100.0-(100.0/(1.0+RS))
    new_df=pd.DataFrame()
    new_df['Adj Close']=FB['Adj Close']
    new_df['RSI']=RSI
    data=new_df

    #Buy or Sell
    def get_signal(data):
        buy_signal=[]
        sell_signal=[]

        for i in range(len(data['Adj Close'])):
            if data['RSI'][i]>70:
                buy_signal.append(np.nan)
                sell_signal.append(data['Adj Close'][i])
            elif data['RSI'][i]<30:
                buy_signal.append(data['Adj Close'][i])
                sell_signal.append(np.nan)
            else:
                buy_signal.append(np.nan)
                sell_signal.append(np.nan)

        return (buy_signal,sell_signal)

    data['RSI Buy Low'] = get_signal(new_df)[0]
    data['RSI Sell Low'] = get_signal(new_df)[1]

    def get_signal(data):
        buy_signal=[]
        sell_signal=[]

        for i in range(len(data['Adj Close'])):
            if data['RSI'][i]>80:
                buy_signal.append(np.nan)
                sell_signal.append(data['Adj Close'][i])
            elif data['RSI'][i]<20:
                buy_signal.append(data['Adj Close'][i])
                sell_signal.append(np.nan)
            else:
                buy_signal.append(np.nan)
                sell_signal.append(np.nan)

        return (buy_signal,sell_signal)

    data['RSI Buy Mid'] = get_signal(new_df)[0]
    data['RSI Sell Mid'] = get_signal(new_df)[1]

    def get_signal(data):
        buy_signal=[]
        sell_signal=[]

        for i in range(len(data['Adj Close'])):
            if data['RSI'][i]>90:
                buy_signal.append(np.nan)
                sell_signal.append(data['Adj Close'][i])
            elif data['RSI'][i]<10:
                buy_signal.append(data['Adj Close'][i])
                sell_signal.append(np.nan)
            else:
                buy_signal.append(np.nan)
                sell_signal.append(np.nan)

        return (buy_signal,sell_signal)

    data['RSI Buy High'] = get_signal(new_df)[0]
    data['RSI Sell High'] = get_signal(new_df)[1]

    return data

    #Plotting DATA
    plt.figure(figsize=(12.2,4.5))
    plt.plot(new_df.index, new_df['Adj Close'])
    plt.title('Adj. Close Price History')
    plt.legend(new_df.columns.values, loc='upper left')
    plt.show()

    plt.figure(figsize=(12.2,4.5))
    plt.title(['RSI Plot'])
    plt.plot(new_df.index,new_df['RSI'])
    plt.axhline(0, linestyle='--', alpha=0.5, color='gray')
    plt.axhline(10, linestyle='--', alpha=0.5, color='orange')
    plt.axhline(20, linestyle='--', alpha=0.5, color='blue')
    plt.axhline(30, linestyle='--', alpha=0.5, color='red')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(80, linestyle='--', alpha=0.5, color='blue')
    plt.axhline(90, linestyle='--', alpha=0.5, color='orange')
    plt.axhline(100, linestyle='--', alpha=0.5, color='gray')
    plt.show()

def OBV(*args):
    df = yf.download(stockname, period="1000d", interval="1d")
    OBV=[]
    OBV.append(0)
    for i in range(1,len(df.Close)):
        if df.Close[i]>df.Close[i-1]:
            OBV.append(OBV[-1]+df.Volume[i])
        elif df.Close[i]<df.Close[i-1]:
            OBV.append(OBV[-1]-df.Volume[i])
        else:
            OBV.append(OBV[-1])
    df['OBV']=OBV
    df['OBV_EMA']=df['OBV'].ewm(span=20).mean()

    #function to by and sell a stock
    def buy_sell(signal,col1,col2):
        sigPriceBuy=[]
        sigPriceSell=[]
        flag=-1

        for i in range(0,len(signal)):
            if signal[col1][i]>signal[col2][i] and flag!=1:
                sigPriceBuy.append(signal['Close'][i])
                sigPriceSell.append(np.nan)
                flag=1
            elif signal[col1][i]<signal[col2][i] and flag!=0:
                sigPriceSell.append(signal['Close'][i])
                sigPriceBuy.append(np.nan)
                flag=0
            else:
                sigPriceSell.append(np.nan)
                sigPriceBuy.append(np.nan)
        return (sigPriceBuy,sigPriceSell)

    x=buy_sell(df,'OBV','OBV_EMA')
    df['OBV Buy']=x[0]
    df['OBV Sell']=x[1]
    #Add data to larger df
    return df

    #Plot Data
    plt.figure(figsize=(12.2,4.5))
    plt.plot(df['Close'],label='Close',alpha=0.35)
    plt.scatter(df.index,df['OBV Buy'], label='Buy_Signal',marker='^',alpha=1, color='green')
    plt.scatter(df.index, df['OBV Sell'], label='Sell_Signal', marker='v', alpha=1,color='red')
    plt.title('Buy and Sell Signals')
    plt.legend(loc='upper left')
    plt.show()

def MACD(*args):
    df = yf.download(stockname, period="1000d", interval="1d")
    ShortEMA=df.Close.ewm(span=12,adjust=False).mean()
    LongEMA=df.Close.ewm(span=26,adjust=False).mean()
    MACD=ShortEMA-LongEMA
    signal=MACD.ewm(span=9, adjust=False).mean()
    df['MACD']=MACD
    df['Signal Line']=signal
    def buy_sell(signal):
        Buy=[]
        Sell=[]
        flag=-1

        for i in range(0,len(signal)):

            if signal['MACD'][i]<signal['Signal Line'][i] and flag!=1:
                Sell.append(np.nan)
                Buy.append(signal['Close'][i])
                flag=1


            elif signal['MACD'][i]>signal['Signal Line'][i] and flag!=0:
                Buy.append(np.nan)
                Sell.append(signal['Close'][i])
                flag=0

            else:
                Sell.append(np.nan)
                Buy.append(np.nan)

        return (Buy,Sell)


    a=pd.DataFrame()
    a=buy_sell(df)


    df['Macd Buy'] = a[0]
    df['Macd Sell'] = a[1]
    return df



    #Plot Data
    plt.figure(figsize=(12.2,4.5))
    plt.scatter(df.index, df['Macd Buy'],color='green',label='Buy',marker='^',alpha=1)
    plt.scatter(df.index, df['Macd Sell'], color='red', label='Sell', marker='v', alpha=1)
    plt.plot(df['Close'],label='Close Price',alpha=0.35)
    plt.title('Close Price Buy and Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Close Price USD')
    plt.legend(loc='upper left')
    plt.show()

def MFI(*args):
    df = yf.download(stockname, period="1013d", interval="1d")
    typical_price=(df['Close']+df['High']+df['Low'])/3
    period=14
    money_flow=typical_price*df['Volume']
    positive_flow=[]
    negative_flow=[]

    for i in range(1,len(typical_price)):
        if typical_price[i]>typical_price[i-1]:
            positive_flow.append(money_flow[i-1])
            negative_flow.append(0)
        elif typical_price[i]<typical_price[i-1]:
            negative_flow.append(money_flow[i-1])
            positive_flow.append(0)
        else:
            positive_flow.append(0)
            negative_flow.append(0)
    positive_mf=[]
    negative_mf=[]

    for i in range(period-1,len(positive_flow)):
        positive_mf.append(sum(positive_flow[i+1-period:i-1]))
    for i in range(period-1,len(negative_flow)):
        negative_mf.append(sum(negative_flow[i+1-period:i-1]))
    mfi=100*(np.array(positive_mf)/(np.array(positive_mf)+(np.array(negative_mf))))
    new_df=pd.DataFrame
    new_df=df[period:]
    new_df['MFI']=mfi

    #Buy and Sell signals
    def get_signal(data,high,low):
        buy_signal=[]
        sell_signal=[]

        for i in range(len(data['MFI'])):
            if data['MFI'][i]>high:
                buy_signal.append(np.nan)
                sell_signal.append(data['Close'][i])
            elif data['MFI'][i]<low:
                buy_signal.append(data['Close'][i])
                sell_signal.append(np.nan)
            else:
                sell_signal.append(np.nan)
                buy_signal.append(np.nan)

        return (buy_signal,sell_signal)
    new_df['MFI Buy']=get_signal(new_df,80,20)[0]
    new_df['MFI Sell'] = get_signal(new_df, 80, 20)[1]
    return new_df

    #plot data
    plt.figure(figsize=(12.2, 4.5))
    plt.scatter(new_df.index, new_df['MFI Buy'], color='green', label='Buy Signal', marker='^', alpha=1)
    plt.scatter(new_df.index, new_df['MFI Sell'], color='red', label='Sell Signal', marker='v', alpha=1)
    plt.plot(df['Close'], label='Close Price', alpha=0.5)
    plt.title('Close Price Buy and Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Close Price USD')
    plt.legend(loc='upper left')
    plt.show()

def Buy_Sell(*args,**kwargs):
    df = yf.download(stockname, period="1000d", interval="1d")
#--------risk_ratio--------#
    num=3
#--------------------------#
    macd=MACD().replace(np.nan,0)
    df['Macd Buy']=macd['Macd Buy']
    df['Macd Sell']=macd['Macd Sell']
    mfi=MFI().replace(np.nan,0)
    df['MFI Buy']=mfi['MFI Buy']
    df['MFI Sell'] = mfi['MFI Sell']
    boll=Bollinger_Lines().replace(np.nan,0)
    df['Boll Buy']=boll['Boll Buy']
    df['Boll Sell'] = boll['Boll Sell']
    rsi=RSI().replace(np.nan,0)
    df['RSI Buy Low']=rsi['RSI Buy Low']
    df['RSI Sell Low']=rsi['RSI Sell Low']

    df['RSI Buy Mid']=rsi['RSI Buy Mid']
    df['RSI Sell Mid']=rsi['RSI Sell Mid']

    df['RSI Buy High']=rsi['RSI Buy High']
    df['RSI Sell High']=rsi['RSI Sell High']

    sma=SMA().replace(np.nan,0)
    df['SMA Buy']=sma["SMA Buy"]
    df['SMA Sell'] = sma["SMA Sell"]
    obv=OBV().replace(np.nan,0)
    df['OBV Buy']=obv['OBV Buy']
    df['OBV Sell'] = obv['OBV Sell']

    rsi_buy_high=0
    rsi_sell_high=0
    rsi_sell_mid=0
    rsi_buy_mid=0
    rsi_sell_low=0
    rsi_buy_low=0
    boll_buy=0
    boll_sell=0

    buy=[]
    sell=[]

    running_total_buy=0
    running_total_sell=0

#   on = 1 off = 0

    for i in range(0,len(df)):

        if df['Macd Buy'][i]>df['Macd Sell'][i]:
            running_total_buy=running_total_buy+1
        elif df['Macd Buy'][i]<df['Macd Sell'][i]:
            running_total_sell=running_total_sell+1

        if df['SMA Buy'][i]>df['SMA Sell'][i]:
            running_total_buy=running_total_buy+1
        elif df['SMA Buy'][i]<df['SMA Sell'][i]:
            running_total_sell=running_total_sell+1
        '''
        if df['OBV Buy'][i]>df['OBV Sell'][i]:
            running_total_buy=running_total_buy+1
        elif df['OBV Buy'][i]<df['OBV Sell'][i]:
            running_total_sell=running_total_sell+1
        '''
        if df['Boll Buy'][i]>df['Boll Sell'][i] and boll_buy==0 and boll_sell==0:
            running_total_buy=running_total_buy+1
            boll_buy=1
        elif df['Boll Buy'][i]<df['Boll Sell'][i]:
            running_total_sell=running_total_sell+1
            boll_sell=1

        if df['MFI Buy'][i]>df['MFI Sell'][i]:
            running_total_buy=running_total_buy+1
        elif df['MFI Buy'][i]<df['MFI Sell'][i]:
            running_total_sell=running_total_sell+1

        if df['RSI Buy Low'][i]>df['RSI Sell Low'][i] and rsi_sell_low==0 and rsi_buy_low==0:
            running_total_buy=running_total_buy+1
            rsi_buy_low=1
        elif df['RSI Buy Low'][i]<df['RSI Sell Low'][i]:
            running_total_sell=running_total_sell+1
            rsi_sell_low=1

        if df['RSI Buy Mid'][i]>df['RSI Sell Mid'][i] and rsi_sell_mid==0 and rsi_buy_mid==0:
            running_total_buy=running_total_buy+1
            rsi_buy_mid=1
        elif df['RSI Buy Mid'][i]<df['RSI Sell Mid'][i]:
            running_total_sell=running_total_sell+1
            rsi_sell_mid=1

        if df['RSI Buy High'][i]>df['RSI Sell High'][i] and rsi_buy_high==0 and rsi_sell_high==0:
            running_total_buy=running_total_buy+1
            rsi_buy_high=1
        elif df['RSI Buy High'][i]<df['RSI Sell High'][i]:
            running_total_sell=running_total_sell+1
            rsi_sell_high=1

    #-------others--------#
        if running_total_buy>=num or running_total_sell>=num:
            if running_total_buy>=num:
                buy.append(df['Close'][i])
                sell.append(np.nan)
                running_total_buy=0
                running_total_sell=0
                rsi_buy_high = 0
                rsi_sell_high = 0
                rsi_sell_mid = 0
                rsi_buy_mid = 0
                rsi_sell_low = 0
                rsi_buy_low = 0
                boll_buy = 0
                boll_sell = 0
            if running_total_sell>=num:
                sell.append(df['Close'][i])
                buy.append(np.nan)
                running_total_buy=0
                running_total_sell=0
                boll_buy = 0
                boll_sell = 0
        else:
            buy.append(np.nan)
            sell.append(np.nan)

    a=buy
    b=sell
    df['Buy'] = a
    df['Sell'] = b
    return df

def Profit(df):
    find_buy=0
    find_sell=0
    buy=0
    sell=0
    total_profit=0
    for i in range(0,len(df)):
        if df['Buy'][i]>0 and find_buy==0:
            find_buy=1
            buy=df['Buy'][i]
        if df['Sell'][i]>0 and find_sell==0:
            find_sell=1
            sell=df['Sell'][i]
        if find_buy==1 and find_sell==1:
            subtotal=sell-buy
            total_profit=total_profit+subtotal
            find_buy=0
            find_sell=0

    return total_profit


df=(Buy_Sell())

print('Potential Profit $'+str(Profit(df)))
long_term_profit=df["Close"][999]-df['Close'][1]
print('Long Term Holding Profit $'+str(long_term_profit))
print('Difrence is $'+str(Profit(df)-(long_term_profit)))

#Plot All the Data
plt.figure(figsize=(12.2,4.5))
plt.scatter(df.index, df['Buy'],color='green',label='Buy',marker='^',alpha=1)
plt.scatter(df.index, df['Sell'], color='red', label='Sell', marker='v', alpha=1)
plt.plot(df['Close'],label='Close Price',alpha=0.35)
plt.title('Over All Buy & Sell')
plt.xlabel('Date')
plt.ylabel('Close Price USD')
plt.legend(loc='upper left')
plt.show()

