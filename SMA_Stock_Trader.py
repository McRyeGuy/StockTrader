import warnings
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')
stockname = "GC=F"



df = yf.download(stockname, period="730d", interval="1h")


def SMA(pastdays):
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

def Calcuate_PastDays(*args):
    profitvalues=[]
    for i in range(25):
        data = SMA(pastdays=i)
        profitvalues.append(Profit(data))
    profitvalues=np.array(profitvalues)
    df = pd.DataFrame(profitvalues, columns= ['Price'])
    max_value = df['Price'].max()
    df=df[df['Price'] == max_value].index.values
    df=df.astype(np.int)
    return df




data=SMA(pastdays=int(Calcuate_PastDays()))
print('Profit $'+str(Profit(data)))
print('Pastdays is '+str(Calcuate_PastDays()))


plt.figure(figsize=(12.5, 4.5))
plt.plot(data['AAPL'], label='AAPL', alpha=0.35)
plt.plot(data['SMA30'], label='SMA30', alpha=0.35)
plt.plot(data['SMA100'], label='SMA100', alpha=0.35)
plt.plot(data['SMA10'], label='SMA10', alpha=0.35)
plt.scatter(data.index, data['Buy'], label="Buy", marker='^', color='green')
plt.scatter(data.index, data['Sell'], label="Sell", marker='v', color='red')
plt.title('SMA Buy or Sell')
plt.xlabel('Date')
plt.ylabel9 = ('Adj Close Price')
plt.legend(loc='upper left')
plt.show()
