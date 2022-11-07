import time
import requests
import pandas as pd
import datetime
import csv
import os

while(1):
    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()

    data = book['data']

    timestamp=data['timestamp']
    _date = datetime.datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S')


    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0
    bids['time']=_date

    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1
    asks['time']=_date
    df = bids.append(asks)
    print (df)

    should_write_header = os.path.exists("2022-11-05-bithumb-BTC-orderbook.csv")
    if should_write_header == False:
        df.to_csv("2022-11-05-bithumb-BTC-orderbook.csv", index=False, header=True, mode = 'a',encoding='utf-8-sig')
    else:
        df.to_csv("2022-11-05-bithumb-BTC-orderbook.csv", index=False, header=False, mode = 'a',encoding='utf-8-sig')

    time.sleep(1)
