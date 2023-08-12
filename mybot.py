import schedule
from kucoin.client import Client
import time
import pandas as pd

import ui

#pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# ts stores the time in seconds
ts = int(time.time())
sma_5min_100times =ts - (300 * 100)

api_key = '63b93a07d132fa0001db87e0'
api_secret = '9efa0cad-971f-4117-998e-1795cb7ee699'
api_passphrase = 'amirmohammadrezvani'
# symbol = 'BTC-USDT'
# stg = 1
# amount_of_assets =0.5# 0.00 to 1.00 as percentage

####if UI is running
# api_key = ui.key
# api_secret = ui.address
# api_passphrase = ui.phrase
stg = ui.stg_order()
symbol=ui.order()
amount_of_assets = ui.percent_amount

client = Client(api_key, api_secret, api_passphrase)




garanty = 0 # stg2 safe hold garanty
baze_mosbat=1.01
baze_manfi=0.99
target_win = 3 # win limit percent
target_loss = -1
####accounts = client.get_accounts()
####with upper comment u can get all accounts details and id to get the acc id beeded in the next line
acc_data = client.get_accounts()
# print(acc_data[0]['id'])
#account id is :'62f298dcf2673b0001929483'
account_id =acc_data[0]['id']
#print(account_id)
account = client.get_account(account_id)
acc_balance = float(account['balance'])

data = client.get_ticker(symbol)['price']
#####################add new stuff

stat1 =2
stat2 =4
stat3 = 50

newsma1 = []
end = int(time.time())
start = end - ((86400 * 1000))
data_for_df = client.get_kline_data(symbol, '1day', start, end)
df = pd.DataFrame(data_for_df, columns=['timestamp', 'open', 'high', 'low', 'close', 'amount', 'volume'])
df['sma1'] = df.open.rolling(1).mean()
end = int(time.time())
lens = len(df)
for x in range(len(df)):
    newsma1.append(df['sma1'].iloc[(lens - x)-1])
df['ams1'] = newsma1
df['sma2'] = df.ams1.rolling(stat1).mean()
df['sma4'] = df.ams1.rolling(stat2).mean()
df['sma50'] = df.ams1.rolling(stat3).mean()
high =[]
low=[]
lastB = 0
lastS = 0
df = df.iloc[0:100]

def sma2():
    df['sma2'] = df.sma1.rolling(stat1).mean()
    return df['sma2'][1]
def sma4():
    df['sma4'] = df.sma1.rolling(stat2).mean()
    return df['sma4'][3]
def sma50():
    df['sma'] = df.sma1.rolling(stat3).mean()
    return df['sma50'][49]

###############################
def symbol_price():
    symbol_price = round(float(client.get_ticker(symbol)['price']), 2)
    # print('target :', symbol_price)
    return symbol_price
sp1 = symbol_price()
print('sp1 :', sp1)

size_of_order = str(round((float(acc_balance)/float(sp1))*amount_of_assets, 7))
TorF = False

# ######## STG SECTION #################
def stg1():
    # win/loss
    global TorF

    print('starting stg1...')
    if TorF == True:

        # order = client.get_order('62f55305432538000112cf64')
        order = client.get_orders(symbol)
        print('check to sell or not')
        buy_price = round((1 / float(order['items'][0]['dealSize']) * float(order['items'][0]['dealFunds'])), 2)

        print('buy_price: ', buy_price)
        #sp_func = sp1
        print('@@symbol_price() :', symbol_price())
        print('data price', round(float(data), 2))
        def my_prof():
            prof = round(((symbol_price()/buy_price)*100)-100, 2)
            return prof
        my_profit = my_prof()
        print('my prof is :', my_profit, '%')
        print('left to win :', float(target_win -my_prof()), '%')
        if my_prof() >= target_win:
            this_size = order['items'][0]['dealSize']
            client.create_market_order(symbol, Client.SIDE_SELL, size=this_size)
            time.sleep(10)
            TorF = False
        elif my_prof() < target_loss:
            print('sleeping 10 sec')
            this_size = order['items'][0]['dealSize']
            client.create_market_order(symbol, Client.SIDE_SELL, size=this_size)
            time.sleep(10)

    else:
        print('time to buy one')
        ####valid size for btc is equal or less than 8 decimals
        market_order = client.create_market_order(symbol, Client.SIDE_BUY, size=size_of_order)
        print("market order value is this: ", market_order)
        TorF = True

def stg2():
    # safe hold
    global TorF
    global garanty

    print("STG2 is runing... ")
    if TorF == True:

        # order = client.get_order('62f55305432538000112cf64')
        order = client.get_orders(symbol)

        print('garanty is this : ', garanty)
        #sp_func = sp1
        print('@@symbol_price() :', symbol_price())
        print('data price', round(float(data), 2))
        def my_prof():
            prof = round(((symbol_price()/garanty)*100)-100, 2)
            return prof
        my_profit = my_prof()
        print('my prof is :', my_profit, '%')
        print('left to win :', float(target_win -my_prof()), '%')
        if my_prof() >= target_win:
            print("only update garanty value")
            garanty= symbol_price()

        elif my_prof() < target_loss:
            print(' target loss of garanty so  SELL ==>sleeping 10 sec')
            this_size = order['items'][0]['dealSize']
            client.create_market_order(symbol, Client.SIDE_SELL, size=this_size)
            time.sleep(10)
            TorF = False

    else:
        print('time to buy  and set garanty')
        if garanty == 0  and TorF == False:
            print("first time buy ")
            client.create_market_order(symbol, Client.SIDE_BUY, size=size_of_order)
            order = client.get_orders(symbol)
            print('set garanty after firs buy ')
            garanty = round((1 / float(order['items'][0]['dealSize']) * float(order['items'][0]['dealFunds'])), 2)
            TorF = True
        elif garanty > 0 and TorF == False:
            print("cheking baze garanty for rebuy")
            if garanty*baze_mosbat > symbol_price() and garanty*baze_manfi < symbol_price():
                print("rebuy for pomp")
                client.create_market_order(symbol, Client.SIDE_BUY, size=size_of_order)

                TorF = True
####valid size for btc is equal or less than 8 decimals

#### STG3 ############################
trigger = 0  # 1 cant buy and 0 can buy

#def stg3():
#     print("STG3 is running...")
#     global trigger
#
#     if sma2() > sma4() and trigger == 0 and symbol_price() > sma50():
#
#         market_order = client.create_market_order(symbol, Client.SIDE_BUY, size=size_of_order)
#         trigger = 1
#
#     elif sma4() > sma2() and trigger == 1 and symbol_price() > sma50():
#         if df['ams1'].iloc[lastB] * 1.05 < df['ams1'].iloc[x] or df['ams1'].iloc[lastB] * 0.99 > df['ams1'].iloc[x]:
#             lastB = x
#
#             print("lastSELis:", lastB , "at ", df['ams1'].iloc[lastB])
#             low.append(df['ams1'].iloc[x])
#             high.append(float('nan'))
#                 trigger = 0
#
#         else:
#             high.append(float('nan'))
#             low.append(float('nan'))
#
#
#     else:
#         high.append(float('nan'))
#         low.append(float('nan'))
#     df['stat1'] = high
#     df['stat2'] = low
#     print(sma4())

def stg3() :

    global TorF
    print("STG3 is runing... ")
    if TorF == True :


        print("have coin")
        if sma4() > sma2()  and symbol_price() > sma50():
            print("calculate prof")
            time.sleep(5)
            order = client.get_orders(symbol)
            buy_price = round((1 / float(order['items'][0]['dealSize']) * float(order['items'][0]['dealFunds'])), 2)

            def my_prof():
                prof = round(((symbol_price() / buy_price) * 100) - 100, 2)
                return prof
            my_profit = my_prof()

            print('my prof is :', my_profit, '%')
            #
            if my_prof() >= target_win:
                print("sell to win")
                this_size = order['items'][0]['dealSize']
                client.create_market_order(symbol, Client.SIDE_SELL, size=this_size)
                TorF=False
                time.sleep(10)
            elif my_prof() < target_loss:
                print("sell to loss")
                this_size = order['items'][0]['dealSize']
                client.create_market_order(symbol, Client.SIDE_SELL, size=this_size)
                TorF = False
                time.sleep(10)
        time.sleep(10)

    else:
        if sma2() > sma4() and symbol_price() > sma50():
            print("buy coin")
            client.create_market_order(symbol, Client.SIDE_BUY, size=size_of_order)
            TorF=True
            time.sleep(10)


shomar = 0
def stg_test():
    global shomar
    shomar+=1
    print("try ", shomar)

# main ################################
if stg == 2 :
    #normal
    schedule.every(10).seconds.do(stg1)
elif stg == 3 :
    #safe hold
    schedule.every(10).seconds.do(stg2)
elif stg ==1 :
    #SMA
    schedule.every(10).seconds.do(stg3)
else :
    schedule.every(10).seconds.do(stg_test)
    print("no strategy defined yet :(")
#######################################




while True:
    try:
        schedule.run_pending()
    except:
        print('!!! maybe network problem ')
        time.sleep(30)

