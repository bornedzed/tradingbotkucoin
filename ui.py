from tkinter import *

window = Tk()
window.geometry("420x550")
window.title("trading robot interface")
window.config(background="#2C3639")


# header
label = Label(window,background='#2C3639' , text="TRADE BOT",font=('arial', 36 ,'bold'),fg='#c4c4c4' )
label.pack()
###var
coins = ["BTCUSDT","ETHUSDT","BCHUSDT"]
stgnum = ["SMA","Normal","Safe Hold"]
x =IntVar()
x2 =IntVar()
###
###funcs
def order():
    if (x.get()  == 0):
        print("BTCUSDT")
        symbol = 'BTC-USDT'
        return symbol
    elif(x.get()  == 1):
        print("ETHUSDT")
        symbol = 'ETH-USDT'
        return symbol
    elif(x.get() == 2):
        print("BCHUSDT")
        symbol = 'BCH-USDT'
        return symbol
    else:
        print("wrong ??")
    # print(coins[int(str(x)[-1])])
key =''
address = ''
phrase = ''
percent_amount = 0
def setter1():
    global key
    key = entry1.get()

def setter2():
    global address
    address = entry2.get()


def setter3():
    global phrase
    phrase = entry3.get()

def setter4():
    global percent_amount
    percent_amount = entry4.get()
    percent_amount = (float(percent_amount)/100)


def stg_order():
    if (x2.get()  == 0):
        print("STG1 set in UI")
        stgn = 1
        return stgn
    elif(x2.get()  == 1):
        print("STG2 set in UI")
        stgn = 2
        return stgn
    elif(x2.get() == 2):
        print("STG3 set in UI")
        stgn = 3
        return stgn
    else:
        print("wrong ??")
####
def sub():
    print("submitted :)")
### widges
for index in range (len(coins)):
    radio= Radiobutton(window, text=coins[index] , font=('arial', 14 ,'italic'),#add text to buttons
                         variable=x,#groups
                         value= index,
                         command = order,
                         fg = '#DCD7C9',
                       background='#2C3639')#give value to each button
    radio.pack()
label1=Label(window, text="API key",font=('arial', 16 ,'bold'),background='#2C3639',fg='#DCD7C9')
label2=Label(window, text="API Adress",font=('arial', 16 ,'bold'),background='#2C3639',fg='#DCD7C9')
label3=Label(window, text="Phrase",font=('arial', 16 ,'bold'),background='#2C3639',fg='#DCD7C9')
label4=Label(window, text="Amount %",font=('arial', 16 ,'bold'),background='#2C3639',fg='#DCD7C9')
entry1 =Entry(window ,width=20 ,font=('Arial' , 16))
entry2 =Entry(window,width=20 ,font=('Arial' , 16))
entry3 =Entry(window,width=20 ,font=('Arial' , 16))
entry4 =Entry(window,width=20 ,font=('Arial' , 16))
btn1 =Button(window ,text="submit" , width=10 , font=('Arial', 14 , 'bold'),fg= '#234567' , command=lambda:[setter1(),setter2(),setter3(),setter4(),sub() ])
# btn2 =Button(window ,text="exit" , width=10 , font=('Arial', 14 , 'bold'),fg= '#234567' , command=quit)
btn2=Button(window, text="Quit", width=10 , font=('Arial', 14 , 'bold'),fg= '#234567', command=window.destroy)
for index in range (len(coins)):
    radio2= Radiobutton(window, text=stgnum[index] , font=('arial', 14 ,'italic'),#add text to buttons
                         variable=x2,#groups
                         value= index,
                         command = stg_order,
                         fg = '#DCD7C9',
                       background='#2C3639')#give value to each button
    radio2.pack(side=LEFT)
#####


##### packing

entry1.place(x =10 , y =170)
label1.place(x =300 , y =170)
entry2.place(x =10 , y =220)
label2.place(x =300 , y =220)
entry3.place(x =10 , y =270)
label3.place(x =300 , y =270)
entry4.place(x =10 , y =320)
label4.place(x =300 , y =320)
btn1.place(x =150 , y =420)
btn2.place(x =150 , y =460)



window.mainloop()