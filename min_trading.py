import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import math

stockname='JNJ'

#create pd and csv file:
df_total = pd.DataFrame(columns = ['Close', 'SMA_7', 'SMA_2', 'Set_Low'])

df_total.to_csv ('STONKS.csv', index = False, header=True)
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def Current_Close(*args,**kwargs):
    url='https://finance.yahoo.com/quote/'+str(stockname)+'?p='+str(stockname)+'&.tsrc=fin-srch'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    price = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[0].text
    change = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[1].text

    price = price.replace(',', '')
    price=str(price)

    return price
def SMA_7(*args,**kwargs):
    data = yf.download(stockname, period="7d", interval="1m")
    df = data['Close']
    df_total = pd.read_csv('STONKS.csv')
    df_total=df_total['Close']
    df.append(df_total)

    num_rows=df.shape[0]

    sum_rows= df.sum(axis=0)
    outputsma=sum_rows/num_rows
    return outputsma

def SMA_2(*args,**kwargs):
    data = yf.download(stockname, period="2d", interval="1m")
    df = data['Close']
    df_total = pd.read_csv('STONKS.csv')
    df_total=df_total['Close']
    df.append(df_total)

    num_rows=df.shape[0]

    sum_rows= df.sum(axis=0)
    outputsma=sum_rows/num_rows
    return outputsma
def SMA_today(*args,**kwargs):
    df = pd.read_csv('STONKS.csv')
    df=df['Close']
    df.append(df)

    num_rows=df.shape[0]

    sum_rows= df.sum(axis=0)
    outputsma=sum_rows/num_rows
    return outputsma

def AddDatatoDF(*args,**kwargs):
    # create dataframe
    df_total = pd.read_csv('STONKS.csv')

    new_row = {'Close': dataset, 'SMA_7':sma7, 'SMA_2': sma2,'Set_Low': low}
    # append row to the dataframe
    df_total = df_total.append(new_row, ignore_index=True)
    df_total.to_csv('STONKS.csv', index=False, header=True)

def SetLow():
    #this code finds the last lowest dip in the df
    setlowpresent=1.

    df= pd.read_csv('STONKS.csv')
    df=df['Close']
    last_close=df.tail(1)
    #last_close=float(last_close)
    count=0
    num_rows = df.shape[0]
    #finding...
    for i in range(num_rows):
        count=count+1
        changing_num_row=df.tail(count)
        changing_num_row=changing_num_row.head(1)
        changing_num_row=float(changing_num_row)
        # This will cause problems
        changing_num_row=round_up(changing_num_row, 2)
        if changing_num_row*(setlowpresent)<last_close:
            templow=changing_num_row
            while templow>0:
                count = count + 1
                changing_num_row = df.tail(count)
                changing_num_row = changing_num_row.head(1)
                changing_num_row = float(changing_num_row)
        #This will cause problems
                changing_num_row = round_up(changing_num_row, 2)
                if count>num_rows:
                    return 0
                if changing_num_row > templow:
                    setlow=changing_num_row
                    return setlow





dataset=Current_Close()
sma7=SMA_7()
sma2=SMA_2()
low=SetLow()
AddDatatoDF()
