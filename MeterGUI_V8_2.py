# V5 update: when remaining = 0 while online access happens, count down functions
# verification code fades after 5s
# when a spot is illegally occupied, the timer turns red and confirm button for this spot is disabled (now it is disabled if illegalOccupied = 0)
#V6 update: finished threading,  illegal occupying situation, clear position. Some bugs fixed


import tkinter as tk
import time
import json
import datetime
import random
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import qrcode
import  os
from PIL import Image, ImageTk
from firebase import firebase
from threading import Thread


cred = credentials.Certificate('C:\\Users\\Jonathan\\Desktop\\Python\\idpserver-75258-firebase-adminsdk-e66vk-3a68726e11.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://idpserver-75258.firebaseio.com/'})


firebase = firebase.FirebaseApplication(
     'https://idpserver-75258.firebaseio.com/', None)







location = 'Record'

timelist = ["00:00", "00:15", "00:30", "00:45", "01:00", "01:15", "01:30", "01:45", "02:00"]
selectTime1 = 0
selectTime2 = 0
selectExtraTime1 = 0
selectExtraTime2 = 0
spotSelected = 0
color1 = "yellow"
spotSelected = 2
counting1 = 0
counting2 = 0
remaining1 = 0
remaining2 = 0
currentParkTime1 = "0000000"
currentParkTime2 = "0000000"
onlineExtended1 = 0
onlineExtended2 = 0
code1 = 0
code2 = 0
occupied1 = 5
occupied2 = 5
illegalOccupied1 = 0
illegalOccupied2 = 0
paid1 = 0
paid2 = 0
status1 = 0
status2 = 0
beginning = 0
firstClear = 0
ready = 0


def chooseSpot0():
    global spotSelected
    spotSelected = 0
    if spotSelected == 0:
        b1.config(bg="gray")
        b2.config(bg="white")
    if spotSelected == 1:
        b1.config(bg="white")
        b2.config(bg="gray")
   

def chooseSpot1():
    global spotSelected
    spotSelected = 1
    if spotSelected == 0:
        b1.config(bg="gray")
        b2.config(bg="white")
    if spotSelected == 1:
        b1.config(bg="white")
        b2.config(bg="gray")
  

def addTime():
    global spotSelected
    global selectTime1, selectTime2
    global selectExtraTime1, selectExtraTime2
    global counting1 
    if spotSelected == 0:
        if counting1 == 0:
            selectTime1 = (selectTime1 + 1) % 9
            extratime1.config(text=timelist[selectTime1])
        else:
             selectExtraTime1 = (selectExtraTime1 + 1) % 9
             extratime1.config(text=timelist[selectExtraTime1])
    if spotSelected == 1:
        if counting2 == 0:
            selectTime2 = (selectTime2 + 1) % 9
            extratime2.config(text=timelist[selectTime2])
        else:
            selectExtraTime2 = (selectExtraTime2 + 1) % 9
            extratime2.config(text=timelist[selectExtraTime2])


def minusTime():
    global spotSelected
    global selectTime1, selectTime2
    global selectExtraTime1, selectExtraTime2
    if spotSelected == 0:
        if counting1 == 0:
            selectTime1 -= 1
            if(selectTime1 < 0):
                selectTime1 = 8
            extratime1.config(text=timelist[selectTime1])
        else:
             selectExtraTime1 -= 1
             if(selectExtraTime1 < 0):
                selectExtraTime1 = 8
             extratime1.config(text=timelist[selectExtraTime1])
            
    if spotSelected == 1:
        if counting2 == 0:
            selectTime2 -= 1
            if(selectTime2 < 0):
                selectTime2 = 8
            extratime2.config(text=timelist[selectTime2])
        else:
             selectExtraTime2 -= 1
             if(selectExtraTime2 < 0):
                selectExtraTime2 = 8
             extratime2.config(text=timelist[selectExtraTime2])
            
        
def countdown1():
    global remaining1
    global counting1 
    global selectExtraTime1
    global currentParkTime1
    if remaining1 > 0:
         mins, secs = divmod(remaining1, 60)
         timeformat = '{:02d}:{:02d}'.format(mins, secs)
         displaytime1.config(text=timeformat)
         remaining1 = remaining1 - 1
         counting1 = 1
         displaytime1.after(1000, countdown1)

    else:
         displaytime1.config(text=timelist[selectTime1])
         counting1 = 0
         selectExtraTime1 = 0
         code1 = 0
         data = {'date': currentParkTime1, 'duration': remaining1, "paid":counting1,"verification": 0, "extended":onlineExtended1, "occupied":0}
         result = firebase.put('', '0019', data)
         
def countdown2():
    global remaining2
    global counting2
    global selectExtraTime2
    global currentParkTime2
    if remaining2 > 0:
         mins, secs = divmod(remaining2, 60)
         timeformat = '{:02d}:{:02d}'.format(mins, secs)
         displaytime2.config(text=timeformat)
         remaining2 = remaining2 - 1
         counting2 = 1
         displaytime2.after(1000, countdown2)

    else:
         displaytime2.config(text=timelist[selectTime2])
         counting2 = 0
         selectExtraTime2 = 0
         code2 = 0
         data = {'date': currentParkTime2, 'duration': remaining2, "paid": counting2, "verification": 0, "extended":onlineExtended2,"occupied":0}
         result = firebase.put('', '0020', data)


def confirm():
    global spotSelected
    global selectTime1, selectTime2
    global selectExtraTime1, selectExtraTime2 
    global remaining1, remaining2
    global counting1, counting2
    global currentParkTime1, currentParkTime2
    global code1, code2
    global illegalOccupied1, illegalOccupied2
    global beginning
    global hkuimg
    global ready
    tryremaining1 = 0
    if spotSelected == 0:
        if illegalOccupied1 == 0:
            if counting1 == 0 and selectTime1 != 0:
                remaining1 = selectTime1 * 15
                t = time.time()
                currentParkTime1=datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')
                countdown1()
                code1 = verificaton()
                qrc = str(code1)
                img = qrcode.make(qrc)
                ph = ImageTk.PhotoImage(img)
                vericode.config(image=ph)
                vericode.image = ph
                ready = 1
            elif counting1 == 1 and selectExtraTime1 != 0:
                t = time.time()
                currentParkTime1 = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')
                if remaining1 < 15:
                    tryremaining1 = selectExtraTime1 * 15
                else:
                    tryremaining1 = remaining1 + selectExtraTime1 * 15
                if tryremaining1 <= 120:
                    remaining1 = tryremaining1
                else:
                    remaining1 = 120
                code1 = verificaton()
                qrc = str(code1)
                img = qrcode.make(qrc)
                ph = ImageTk.PhotoImage(img)
                vericode.config(image=ph)
                vericode.image = ph
                ready = 1

            data = {'date': currentParkTime1, 'duration': remaining1, "paid": 0,"verification": code1,"extended":onlineExtended1,"occupied":1}
            result = firebase.put('', '0019', data)
    if spotSelected == 1:
        if illegalOccupied2 == 0:
            if counting2 == 0 and selectTime2 != 0:
                remaining2 = selectTime2 * 15
                t = time.time()
                currentParkTime2=datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')
                countdown2()
                code2 = verificaton()
                qrc2 = str(code2)
                img2 = qrcode.make(qrc2)
                ph2 = ImageTk.PhotoImage(img2)
                vericode.config(image=ph2)
                vericode.image = ph2
                ready = 1
            elif counting2 == 1 and selectExtraTime2 != 0:
                t = time.time()
                currentParkTime2 = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')
                if remaining2 < 15:
                    tryremaining2 = selectExtraTime2 * 15
                else:
                    tryremaining2 = remaining2 + selectExtraTime2 * 15
                if tryremaining2 <= 120:
                    remaining2 = tryremaining2
                else:
                    remaining2 = 120
                code2 = verificaton()
                qrc2 = str(code2)
                img2 = qrcode.make(qrc2)
                ph2 = ImageTk.PhotoImage(img2)
                vericode.config(image=ph2)
                vericode.image = ph2
                ready = 1

            data = {'date': currentParkTime2, 'duration': remaining2, "paid": 0,"verification": code2,"extended":onlineExtended2,"occupied":1}
            result = firebase.put('', '0020', data)
    selectTime1 = 0
    selectTime2 = 0
    selectExtraTime1 = 0
    selectExtraTime2 = 0
    beginning = 1
    extratime1.config(text=timelist[selectExtraTime1])
    extratime2.config(text=timelist[selectExtraTime2])


def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)

def verificaton():
   x = random.randint(1000,9999)
   return x


def clearVeri():
    vericode.config(text="          ")

def serverUpdate():
    global onlineExtended1
    global onlineExtended2
    global remaining1
    global remaining2


    if onlineExtended1 == 1:
        ref2 = db.reference('0019/duration')
        remaining1 = ref2.get()
        mins1, secs1 = divmod(remaining1, 60)
        timeformat1 = '{:02d}:{:02d}'.format(mins1, secs1)
        displaytime1.config(text=timeformat1)
        onlineExtended1 = 0
        if counting1 == 0:
            countdown1()
        data2 = {'date': currentParkTime1, 'duration': remaining1, "paid": 1, "verification": 0,
         "extended": onlineExtended1,"occupied":1}
        result = firebase.put('', '0019', data2)

    if onlineExtended2 == 1:
        ref3 = db.reference('0020/duration')
        remaining2 = ref3.get()
        mins2, secs2 = divmod(remaining2, 60)
        timeformat2 = '{:02d}:{:02d}'.format(mins2, secs2)
        displaytime2.config(text=timeformat2)
        onlineExtended2 = 0
        if counting2 == 0:
            countdown2()
        data3 = {'date': currentParkTime2, 'duration': remaining2, "paid": 1, "verification": 0,
                 "extended": onlineExtended2,"occupied":1}
        result = firebase.put('', '0020', data3)
    displaytime1.after(500,serverUpdate)

def checkIllegalOccupied():
    global occupied1, occupied2
    global spotSelected
    global paid1, paid2
    global illegalOccupied1, illegalOccupied2
    if(occupied1 == 1 and paid1 == 0):
        displaytime1.config(bg="red")
        illegalOccupied1 = 1
    else:
        illegalOccupied1 = 0
        displaytime1.config(bg='green')

    if (occupied2 == 1 and paid2 == 0):
        displaytime2.config(bg="red")
        illegalOccupied2 = 1
    else:
        illegalOccupied2 = 0
        displaytime2.config(bg='green')

    displaytime1.after(3000,checkIllegalOccupied)


def updateLoop1():
    global onlineExtended1
    run = 1
    while run == 1:
        ref4 = db.reference('0019/extended')
        onlineExtended1 = ref4.get()
        time.sleep(1)



def updateLoop2():
    global onlineExtended2
    run = 1
    while run == 1:
        ref5 = db.reference('0020/extended')
        onlineExtended2 = ref5.get()
        time.sleep(1)

def checkLoop1():
    global paid1
    run = 1
    while run == 1:
        ref5 = db.reference('0019/paid')
        paid1 = ref5.get()
        time.sleep(1)

def checkLoop2():
    global paid2
    run = 1
    while run == 1:
        ref5 = db.reference('0020/paid')
        paid2 = ref5.get()
        time.sleep(1)

def clearPos():
    global remaining1,remaining2
    global occupied1,occupied2
    global firstClear
    global beginning
    #if xxx:
     #   displaytime1.after(2000,clearPos)
      #  return

    if remaining1 != 0 and occupied1 == 0:
            time.sleep(0.5)
            if remaining1 != 0 and occupied1 == 0:
                remaining1 = 0
                occupied1 = 0
                beginning = 0
                firstClear = 0
    if remaining2 != 0 and occupied2 == 0:
        time.sleep(0.5)
        if remaining2 != 0 and occupied2 == 0:
            remaining2 = 0
            occupied2 = 0
            beginning = 0
            firstClear = 0
    displaytime1.after(2000,clearPos)

def clearLoop1():
    global occupied1
    global remaining1
    run = 1
    while run == 1:
        ref2 = db.reference('0019/occupied')
        occupied1 = ref2.get()
        print(occupied1)
        time.sleep(0.1)


def clearLoop2():
    global occupied2
    global remaining2
    run = 1
    while run == 1:
        ref2 = db.reference('0020/occupied')
        occupied2 = ref2.get()
        time.sleep(0.1)

def pingLoop():
    run = 1
    while run == 1:
        data = {'ping':"OK"}
        result = firebase.put('', 'hardware/GUI', data)
        time.sleep(1)

def imageLoop():
    global ready
    global hkuimg
    run = 1
    while run == 1:
        if ready == 1:
            time.sleep(10)
            vericode.config(image=hkuimg)
            ready = 0
    time.sleep(1)


win = tk.Tk()
win.geometry("1600x900"+"0"+"0")
win.title("Meter")

Tops = tk.Frame(win, width=1600, height=50, bg="blue", relief=tk.SUNKEN)
Tops.pack(side=tk.TOP)

b1 = tk.Button(win, text="19", font=('calibri', 50, 'bold'), command=lambda: chooseSpot0())
b1.place(relx=0.1, rely=0.3, anchor=tk.CENTER)
b1.config(bg="white")

b2 = tk.Button(win, text="20", font=('calibri', 50, 'bold'), command=lambda: chooseSpot1())
b2.place(relx=0.9, rely=0.3, anchor=tk.CENTER)
b2.config(bg="white")

b3 = tk.Button(win, text="+", font=('calibri', 20, 'bold'), command=lambda: addTime())
b3.place(relx=0.25, rely=0.55, anchor=tk.CENTER)

b4 = tk.Button(win, text="-", font=('calibri', 20, 'bold'), command=lambda: minusTime())
b4.place(relx=0.75, rely=0.55, anchor=tk.CENTER)

confirmB = tk.Button(win, text="Confirm", font=('calibri', 20, 'bold'), command=lambda: confirm())
confirmB.place(relx=0.5, rely=0.8, anchor=tk.CENTER)


displaytime1 = tk.Label(win, font=('calibri', 30, 'bold'), fg="black", bg="green")
displaytime1.place(relx=0.1, rely=0.45, anchor=tk.CENTER)
displaytime1.config(text=timelist[selectTime1])

extratime1 = tk.Label(win, font=('calibri', 30, 'bold'), fg="black", bg="yellow")
extratime1.place(relx=0.1, rely=0.65, anchor=tk.CENTER)
extratime1.config(text=timelist[selectExtraTime1])

displaytime2 = tk.Label(win, font=('calibri', 30, 'bold'), fg="black", bg="green")
displaytime2.place(relx=0.9, rely=0.45, anchor=tk.CENTER)
displaytime2.config(text=timelist[selectTime2])

extratime2 = tk.Label(win, font=('calibri', 30, 'bold'), fg="black", bg="yellow")
extratime2.place(relx=0.9, rely=0.65, anchor=tk.CENTER)
extratime2.config(text=timelist[selectExtraTime2])

vericode = tk.Label(win, font=('calibri', 20, 'bold'), fg="black", bg="yellow")
vericode.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
script_dir = os.path.dirname(__file__)
rel_path = "C:\\Users\\So Tsz Kin\\Desktop\\Android App (Most updated with GUI)\\"
abs_file_path = os.path.join(script_dir, rel_path)
current_file ="HKU" +".jpg"
hkuimg = ImageTk.PhotoImage(Image.open(abs_file_path+current_file),'r')
vericode.config(image=hkuimg)



updateLoop1 = Thread(target=updateLoop1)
updateLoop2 = Thread(target=updateLoop2)
checkLoop1 = Thread(target=checkLoop1)
checkLoop2 = Thread(target=checkLoop2)
clearLoop1 = Thread(target=clearLoop1)
clearLoop2 = Thread(target=clearLoop2)
pingLoop = Thread(target=pingLoop)
imageLoop = Thread(target=imageLoop)

clock = tk.Label(win, font=('times', 20, 'bold'), bg="red")
clock.pack()
time1 = ''
tick()
serverUpdate()
checkIllegalOccupied()


updateLoop1.start()
updateLoop2.start()
checkLoop1.start()
checkLoop2.start()
clearLoop1.start()
clearLoop2.start()
pingLoop.start()
clearPos()
imageLoop.start()
win.mainloop()

