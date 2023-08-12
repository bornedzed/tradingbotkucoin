from tkinter import *
import matplotlib.pyplot as plt
import ui
from kucoin.client import Client
import time
import pandas as pd
import sys

pd.set_option('display.max_rows', None)
api_key = "62ebcb23c4f17e0001855972"
api_secret = "7ea04aa6-3328-44c9-9f45-6cd7d9640854"
api_passphrase = "Amir@Tobeh!"
plt.style.use("dark_background")
client = Client(api_key, api_secret, passphrase=api_passphrase)
# symbol = 'BTC-USDT'
symbol = ui.order()
stg_back = ui.stg_order()

end = int(time.time())
start = end - ((86400 * 1000))
#print(start)
#print(end)

stat1 =2
stat2 =4
stat3 = 200
newsma10 =[]
newsma20 =[]
newsma1 = []

data = client.get_kline_data(symbol, '1day', start, end)
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'amount', 'volume'])
df['sma1'] = df.open.rolling(1).mean()



lens = len(df)
for x in range(len(df)):
    newsma1.append(df['sma1'].iloc[(lens - x)-1])


df['ams1'] = newsma1
df['sma2'] = df.ams1.rolling(stat1).mean()
df['sma4'] = df.ams1.rolling(stat2).mean()
df['sma200'] = df.ams1.rolling(stat3).mean()
# df['sma45'] = df.open.rolling(30).mean()
#print(df)


df = df.iloc[400:1000]

# print(df['open'])

#1btc when it was 20000

high =[]
low=[]
lastB = 0
trigger = 0 #1 cant buy and 0 can buy
b_garanty = 0
# for x in range(len(df)):
#     if df['sma2'].iloc[x] > df['sma4'].iloc[x] and trigger == 0 and df['ams1'].iloc[x] > df['sma200'].iloc[x]:
#         high.append(df['ams1'].iloc[x])
#         low.append(float('nan'))
#         trigger = 1
#         lastB = x
#         #print(x, 'higher')
#     elif df['sma4'].iloc[x] > df['sma2'].iloc[x] and trigger == 1 and df['ams1'].iloc[x] > df['sma200'].iloc[x]:
#         #print(x, 'lower')
#         if df['ams1'].iloc[lastB] * 1.05 <  df['ams1'].iloc[x] or df['ams1'].iloc[lastB] * 0.99 > df['ams1'].iloc[x]:
#             print("lastBis:", lastB)
#             low.append(df['ams1'].iloc[x])
#             high.append(float('nan'))
#             trigger = 0
#         else:
#             high.append(float('nan'))
#             low.append(float('nan'))
#
#
#     else:
#         high.append(float('nan'))
#         low.append(float('nan'))

def choosen_stg():
    if stg_back  == 1:
        back_test1()
    elif stg_back ==2:
        back_test2()
    elif stg_back ==3:
        back_test3()
    else:
        print("no back test here ")

def back_test1():
    global high
    global low
    global lastB
    global trigger
    for x in range(len(df)):
        if df['sma2'].iloc[x] > df['sma4'].iloc[x] and trigger == 0 and df['ams1'].iloc[x] > df['sma200'].iloc[x]:
            high.append(df['ams1'].iloc[x])
            low.append(float('nan'))
            trigger = 1
            lastB = x
            # print(x, 'higher')
        elif df['sma4'].iloc[x] > df['sma2'].iloc[x] and trigger == 1 and df['ams1'].iloc[x] > df['sma200'].iloc[x]:
            # print(x, 'lower')
            if df['ams1'].iloc[lastB] * 1.05 < df['ams1'].iloc[x] or df['ams1'].iloc[lastB] * 0.99 > df['ams1'].iloc[x]:
                print("lastBis:", lastB)
                low.append(df['ams1'].iloc[x])
                high.append(float('nan'))
                trigger = 0
            else:
                high.append(float('nan'))
                low.append(float('nan'))


        else:
            high.append(float('nan'))
            low.append(float('nan'))
    df['stat1'] = high
    df['stat2'] = low
    del df['timestamp']
    del df['low']
    del df['high']
    del df['amount']
    del df['volume']
    del df['close']
    plt.plot(df['ams1'], label=symbol, color='#ffffff', alpha=0.5)
    plt.plot(df['sma2'], label='sma10', color='#0000ff', linestyle='--', alpha=0.5)
    plt.plot(df['sma4'], label='sma20', color='pink', linestyle='--', alpha=0.5)
    plt.plot(df['sma200'], label='sma200', color='#7aeb34', linestyle='--', alpha=0.5)
    plt.scatter(df.index, df['stat1'], label='stat1', marker="^", c='#ff0000', lw=3)
    plt.scatter(df.index, df['stat2'], label='stat2', marker="v", c='#00ff00', lw=3)
    plt.legend(loc="upper right")
    plt.show()


def back_test2():

    print("start stg2 back test")
    global high
    global low
    global lastB
    global trigger
    for x in range(len(df)):
        if trigger == 0:
            high.append(df['ams1'].iloc[x])
            low.append(float('nan'))
            trigger = 1
            lastB = x
        elif trigger == 1 and df['ams1'].iloc[lastB]* 1.1 < df['ams1'].iloc[x]:
            print("lastBis:", lastB)
            low.append(df['ams1'].iloc[x])
            high.append(float('nan'))
            trigger = 0  #sold
        elif trigger == 1 and df['ams1'].iloc[lastB]* 0.97 > df['ams1'].iloc[x]:
            print("lastBis:", lastB)
            low.append(df['ams1'].iloc[x])
            high.append(float('nan'))
            trigger = 0  #sold
        else:
            high.append(float('nan'))
            low.append(float('nan'))


    df['stat1'] = high
    df['stat2'] = low
    del df['timestamp']
    del df['low']
    del df['high']
    del df['amount']
    del df['volume']
    del df['close']
    plt.plot(df['ams1'], label=symbol, color='#ffffff', alpha=0.5)
    # plt.plot(df['sma2'], label='sma10', color='#0000ff', linestyle='--', alpha=0.5)
    # plt.plot(df['sma4'], label='sma20', color='pink', linestyle='--', alpha=0.5)
    # plt.plot(df['sma200'], label='sma200', color='#7aeb34', linestyle='--', alpha=0.5)
    plt.scatter(df.index, df['stat1'], label='BUY', marker="^", c='#00ff00', lw=3)
    plt.scatter(df.index, df['stat2'], label='SELL', marker="v", c='#ff0000', lw=3)
    plt.legend(loc="upper right")
    plt.show()

def back_test3():
    print("start stg3 back tets safe hold")
    global high
    global low
    global lastB
    global trigger
    global b_garanty

    for x in range(len(df)):
        if trigger == 0 :
            if  b_garanty == 0:
                high.append(df['ams1'].iloc[x])
                low.append(float('nan'))
                trigger = 1
                lastB = x
                b_garanty = df['ams1'].iloc[x]
                print("must print 1 time")
            elif  b_garanty * 1.06 > df['ams1'].iloc[x] and b_garanty * 0.97 < df['ams1'].iloc[x]:
                high.append(df['ams1'].iloc[x])
                low.append(float('nan'))
                trigger = 1
                lastB = x
                print("buys after a sell")
            else:
                print("first else:/")

                high.append(float('nan'))
                low.append(float('nan'))

        elif trigger ==1 :
            if  b_garanty * 1.15< df['ams1'].iloc[x]:
                high.append(float('nan'))
                low.append(float('nan'))
                b_garanty = df['ams1'].iloc[x]#update garanty
                print("garanty updated to ", b_garanty)
            elif b_garanty * 0.95 > df['ams1'].iloc[x]:
                 # sell
                low.append(df['ams1'].iloc[x])
                high.append(float('nan'))#sell for safe hold
                trigger = 0  # sold
                print("sell for safe hold")
            else:
                print("second eles ://")
                high.append(float('nan'))
                low.append(float('nan'))

        else:
            print("third else :///")
            high.append(float('nan'))
            low.append(float('nan'))




    df['stat1'] = high
    df['stat2'] = low

    del df['timestamp']
    del df['low']
    del df['high']
    del df['amount']
    del df['volume']
    del df['close']
    plt.plot(df['ams1'], label=symbol, color='#ffffff', alpha=0.5)
    # plt.plot(df['sma2'], label='sma10', color='#0000ff', linestyle='--', alpha=0.5)
    # plt.plot(df['sma4'], label='sma20', color='pink', linestyle='--', alpha=0.5)
    # plt.plot(df['sma200'], label='sma200', color='#7aeb34', linestyle='--', alpha=0.5)
    plt.scatter(df.index, df['stat1'], label='BUY', marker="^", c='#00ff00', lw=3)
    plt.scatter(df.index, df['stat2'], label='SELL', marker="v", c='#ff0000', lw=3)
    plt.legend(loc="upper right")
    plt.show()



# df['stat1'] = high
# df['stat2'] = low

# del df['open']
# print(df)

choosen_stg()
print("market of :",symbol)
print("amount is :",ui.key,ui.address,ui.phrase,ui.percent_amount)
#
def dopass():
    print("robot waking up....")
    window2.destroy()
def exitt ():
    sys.exit("all gone for good ")
window2 = Tk()
window2.geometry("620x250")
window2.title("trading robot interface")
window2.config(background="#2C3639")


# header
label = Label(window2,background='#2C3639' , text="do you want to continue with this strategy ? ",font=('arial', 20 ,'bold'),fg='#c4c4c4' )
label.pack()

btn11 =Button(window2 ,text="NO" , width=30 , font=('Arial', 20 , 'bold'),fg= '#234567' , command=exitt)
# btn2 =Button(window ,text="exit" , width=30 , font=('Arial', 14 , 'bold'),fg= '#234567' , command=quit)
btn22=Button(window2, text="YES", width=30 , font=('Arial', 20 , 'bold'),fg= '#234567', command=dopass)
btn11.pack(side=BOTTOM)
btn22.pack(side=BOTTOM)
window2.mainloop()
# do =[]
#
# for x in range(len(df)):
#     if df['stat'].iloc[x] > df['stat'].iloc[x+1]:
#         do.append(df['stat'].iloc[x])
#         # low.append(float('0'))
#         #print(x, 'higher')
#     else:
#         #print(x, 'lower')
#         # low.append(df['sma10'].iloc[x])
#         do.append(float('0'))
#
# df['do'] = do



# df['sma20'] = low

# amir = df['stat'].iloc[101]
# if amir > 100000:
#     print(amir)
# for x in range(len(df)):
#     if df['stat'].iloc[x-1] > df['stat'].iloc[x] and df['stat'].iloc[x] == 0 :
#         buy.append(float('1'))
#         sell.append(float('nan'))


    # elif df['stat'].iloc[x-1] < df['stat'].iloc[x] and df['stat'].iloc[x-1] == 0 :
    #     sell.append(df['act'].iloc[x+1])
    #     buy.append(float('nan'))


# df['buying']= buy
# df['selling'] = sell



# plt.plot(df['sma1'], label= 'sma1', color='#ffffff', alpha=0.5)



# buy = []
# sell = []
#1 = have dolar 0 = does not have dolar
# dolar = 0
# loss_lim = (garanti/100)*98
# win_lim = (garanti/100)*102
# for x in range(len(df)):
#     if float(df['open'].iloc[x]) < loss_lim and dolar == 0:
#         sell.append(df['open'].iloc[x])
#         buy.append(float('nan'))
#         dolar = 1
#     elif float(df['open'].iloc[x]) >= loss_lim and dolar == 1:
#         buy.append(df['open'].iloc[x])
#         sell.append(float('nan'))
#         dolar = 0
#     else:
#         buy.append(float('nan'))
#         sell.append(float('nan'))
#
# df['buy_sig'] = buy
# df['sell_sig'] = sell

# print(df)
# plt.plot(df['sma1'], label= 'amir', color='#ffffff',alpha=0.5)
# plt.scatter(df.index, df['buy_sig'], label='buy sig', marker="^", color="#00ff00")
# plt.scatter(df.index, df['sell_sig'], label='sell sig', marker="v", color="#ff0000")
# plt.legend(loc="upper left")
# plt.show()

# print(df)

# print(garanti)
# print(loss_lim)
# print(win_lim)
# for x in range(len(df)):
#     print(float(df['open'].iloc[x]))
#
