import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

import time
from apscheduler.schedulers.blocking import BlockingScheduler


def program():
    import random
    ticker_speed=2
    #recommended buypresent 0.01
    buypresent=1
    sellpresent=1
    cash=(10000)
    phone_num=4436083406
    end_time=160000

    #for testing only
    counter=0
    #for testing only


    t = time.localtime()
    current_time = time.strftime("%H%M%S", t)



    headers={"User Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    url="https://finance.yahoo.com/quote/%5EGSPC?p=%5EGSPC"

    r=requests.get(url)

    soup=BeautifulSoup(r.text,"html.parser")
    price=soup.find("div",{"class":"D(ib) Mend(20px)"}).find_all("span")[0].text
    change=soup.find("div",{"class":"D(ib) Mend(20px)"}).find_all("span")[1].text

    print(change, price)

    price = price.replace(',', '')
    price=float(price)
    changenum = change[:-9]
    upordown=change[:-5]
    change_present=change[7:]


    curentprice=(price)
    setlow=(price)
    temppricelow=(price)
    buy_or_sell=(5)
    temppricehigh=(price)
    sethigh=(price)
    setmid=0


    #0 out put is to sell and 1 output is to buy
    #calculate weather to buy or sell, output will either be 1 or 0

    current_time=int(current_time)
    print(current_time)

    while current_time<end_time:
        print("Working. . .")
        t = time.localtime()
        current_time = time.strftime("%H%M%S", t)
        current_time = int(current_time)

        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[0].text
        change = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[1].text

        price = price.replace(',', '')
        price = float(price)
        #changenum = change[:-9]
        #upordown = change[:-5]
        #change_present = change[7:]

        curentprice = (price)



        # stock market going up or down
        if curentprice*(buypresent)>=setlow or current_time>end_time:
                buy_or_sell=1
        if curentprice*(sellpresent)<setlow or current_time>end_time:
                buy_or_sell=0
# When the stock market is going up
        while curentprice>temppricehigh:
            temppricehigh=curentprice

            t = time.localtime()
            current_time = time.strftime("%H%M%S", t)
            current_time = int(current_time)
            r = requests.get(url)

            soup = BeautifulSoup(r.text, "html.parser")
            price = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[0].text
            change = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[1].text

            price = price.replace(',', '')
            price = float(price)

            curentprice = (price)

            if current_time > end_time:
                break
                print("left while loop")
        if curentprice < temppricehigh or current_time>end_time:
                    sethigh = temppricehigh
                    buy_or_sell=1
 #Creating a new setlow/base
        while sethigh>curentprice:

            t = time.localtime()
            current_time = time.strftime("%H%M%S", t)
            current_time = int(current_time)
            r = requests.get(url)

            soup = BeautifulSoup(r.text, "html.parser")
            price = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[0].text
            change = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[1].text

            price = price.replace(',', '')
            price = float(price)

            curentprice = (price)

            setmid=curentprice

            if current_time > end_time:
                break

            if curentprice>setmid:
                setlow=setmid
                buy_or_sell = 1
                print('Loop ends')
                break
#When the stock market is going down
        while curentprice<setlow:
                temppricelow=curentprice

                t = time.localtime()
                current_time = time.strftime("%H%M%S", t)
                current_time = int(current_time)
                r = requests.get(url)

                soup = BeautifulSoup(r.text, "html.parser")
                price = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[0].text
                change = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[1].text

                price = price.replace(',', '')
                price = float(price)

                curentprice = (price)
                if current_time>end_time:
                    break
                    print("left while loop")
        if curentprice > temppricelow or current_time>end_time:
                    setlow = temppricelow
                    buy_or_sell=1


        time.sleep(ticker_speed)
        print(buy_or_sell)
        print('$ '+str(curentprice))
        print(cash)
        print(counter)
        print('this is the set low price '+str(setlow))
        print('This is the temp low price '+str(temppricelow))
        print("This is the current time "+str(current_time))
        print('This is the temp high price ' + str(temppricehigh))
        print('This is the set high price ' + str(sethigh))



        #Fake stocks
        while buy_or_sell==1 and cash>curentprice:
            cash=cash-curentprice
            counter=counter+1
        while buy_or_sell==0:
            counter=counter-1
            for a in range(counter):
                cash=cash+curentprice
    if counter > 0:
        total = counter * curentprice + cash
    else:
        total = cash

# text at the end of the day
    account_sid = 'ACcd146ac97a80c0b4e95d8ec7e1a7ace5' # Found on Twilio Console Dashboard
    auth_token = '4008ffff74a746d462447f03d1072f98' # Found on Twilio Console Dashboard

    myPhone = phone_num # Phone number you used to verify your Twilio account
    TwilioNumber = '+15163622603' # Phone number given to you by Twilio

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=myPhone,
        from_=TwilioNumber,
        body='Your current cash in you MoneyMaker account is $' + str(total))






sched = BlockingScheduler()
sched.add_job(program, 'cron', day_of_week='mon-fri', hour=9, minute=30)
sched.start()
