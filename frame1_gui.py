from tkinter import *  # python 3
from tkinter import font  as tkfont
from smbus2 import SMBus, i2c_msg
import RPi.GPIO as GPIO
import time
import xlrd
from tkinter import messagebox

addr1 = 0x07  # PORT 1
bus = SMBus(1)
status = 0
test_status = 0


class PageTwo1(Frame):

    def __init__(self, parent, controller, pages):
        Frame.__init__(self, parent)  # inheritence
        self.controller = controller
        labels_f1 = Label(self, text="CONFIRM settings", font=('Helvetica', 20), bg="sea green", fg="white")
        labels_f1.pack(side="top", fill="x", pady=5)
        button_f1 = Button(self, text="Back", command=lambda: controller.show_frame(pages[1]), height=2, width=10)
        button_f1.place(x=40, y=600)

        cn1_f1 = Label(self, text="Vehicle Name", width=20, font=('Helvetica', 20), bg="coral", fg="white")
        cn1_f1.place(x=70, y=100)
        cn2_f1 = Label(self, text="     Battery Rated Voltage    ", width=20, font=('Helvetica', 20), bg="coral",
                       fg="white")
        cn2_f1.place(x=320, y=100)
        cn3_f1 = Label(self, text="     Battery Current rating   ", width=20, font=('Helvetica', 20), bg="coral",
                       fg="white")
        cn3_f1.place(x=615, y=100)
        cn4_f1 = Label(self, text="  Battery Type  ", width=20, font=('Helvetica', 20), bg="coral", fg="white")
        cn4_f1.place(x=900, y=100)
        self.label01_f1 = Label(self, width=20, font=('Helvetica', 20), bg="PeachPuff2", fg="black")
        self.label01_f1.place(x=70, y=140)

        self.battery_type01_f1 = Label(self, font=('Helvetica', 20), bg="PeachPuff2", fg="black", width=20)
        self.battery_rating01_f1 = Label(self, font=('Helvetica', 20), bg="PeachPuff2", fg="black", width=20)
        self.battery_voltage01_f1 = Label(self, font=('Helvetica', 20), bg="PeachPuff2", fg="black", width=20)
        self.battery_voltage01_f1.place(x=320, y=140)
        self.battery_rating01_f1.place(x=615, y=140)
        self.battery_type01_f1.place(x=900, y=140)

        txt_f1 = StringVar()
        cn5_f1 = Label(self, textvariable=txt_f1, height=3, width=30, font=('Times', 20), bg="RoyalBlue4", fg="white")
        cn5_f1.place(x=500, y=400)

        button02_f1 = Button(self, text="Test Charging", command=lambda: arduino_testcharge1("T"), height=2, width=15, )
        button02_f1.place(x=400, y=600)
        button03_f1 = Button(self, text="Start Charging", command=lambda: arduino_startcharge1("S"), height=2,
                             width=15, )
        button03_f1.place(x=700, y=600)
        button04_f1 = Button(self, text="Stop Charging", command=lambda: popsup1(self), height=2, width=15, )
        button04_f1.place(x=1000, y=600)
        button03_f1.config(state=DISABLED)
        button04_f1.config(state=DISABLED)

        def arduino_testcharge1(self):

            bus.write_byte(addr1, ord(self))

            # self.test_status_p2=1
            # txt.set("TESTING...")

            def ack_testcharge1(self):
                # self.status=status

                y = bus.read_byte(addr1)
                return y

            code1 = chr(ack_testcharge1(1))
            print(code1)
            if (code1 == "t"):
                time.sleep(2)
                txt_f1.set("TESTING NOW.")
                button03_f1.config(state=ACTIVE)
                button_f1.config(state=DISABLED)

        def arduino_startcharge1(self):
            # if(self.test_status==1):
            # status=1
            bus.write_byte(addr1, ord(self))

            def ack_startcharge1(self):
                z = bus.read_byte(addr1)
                return z

            code2 = chr(ack_startcharge1(1))
            print(code2)
            if (code2 == "s"):
                time.sleep(2)
                txt_f1.set("CHARGING NOW.")
                button04_f1.config(state=ACTIVE)
                button_f1.config(state=DISABLED)

        def popsup1(self):
            # if (self.status==1):

            txt_f1.set("STOP operation")
            MsgBox = messagebox.askquestion('Stop charging', 'Are you sure you want to STOP', icon='warning')

            if MsgBox == 'yes':
                bus.write_byte(addr1, ord("E"))
                time.sleep(1)
                q = bus.read_byte(addr1)
                code3 = chr(q)
                print(code3)
                button_f1.config(state=ACTIVE)
                txt_f1.set("")

                controller.show_frame(pages[0])

            else:
                messagebox.showinfo('Return', 'You will now return to the application screen')
                bus.write_byte(addr1, ord("O"))
                txt_f1.set("Continue charging...")

