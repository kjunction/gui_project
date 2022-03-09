from tkinter import *  # python 3
from tkinter import font  as tkfont
from PIL import Image, ImageTk
from smbus2 import SMBus, i2c_msg
import RPi.GPIO as GPIO
import frame1  # frame for port
import frame2  # frame for port 2
import xlrd  # module for getting excel file
import time  # module for providing delay
from tkinter import messagebox

# define location of excel sheet location
file = "/home/pi/Desktop/Book1.xlsx" #full address
workbook1 = xlrd.open_workbook(file)
sheet = workbook1.sheet_by_index(0)
status = 0

addr1 = 0x07  # PORT 1
addr2 = 0x0c  # PORT 2
bus = SMBus(1)


class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='verdana', size=30, weight="bold", slant="italic")

        container = Frame(self)  # container is bunch where frames are stacked
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.pages = (StartPage, PageOnePort1, PageOnePort2, frame1.PageTwo1, frame2.PageTwo2)
        for F in self.pages:
            frame = F(container, self, self.pages)
            # stacking frames one over other
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        '''Show a frame for the given page name'''
        frame = self.frames[cont]
        frame.tkraise()
        frame.config(bg="ghost white")
        return True


# passes text to the window SecondPage
#     def pass_on_text2(self, text):
#         self.frames[self.pages[2]].get_text(text)


class StartPage(Frame):

    def __init__(self, parent, controller, pages):
        Frame.__init__(self, parent)
        self.controller = controller
        self.pages = pages
        # IMAGE ICON
        im = Image.open("/home/pi/Downloads/abc.png") #picture 1 address
        tkimage = ImageTk.PhotoImage(im)
        l1 = Label(self, image=tkimage, bg="ghost white")
        l1.image = tkimage
        l1.place(y=10, x=150)

        im1 = Image.open('/home/pi/Downloads/def.png')#picture 2 address
        tkimage = ImageTk.PhotoImage(im1)
        l2 = Label(self, image=tkimage, bg="ghost white")
        l2.image = tkimage
        l2.place(y=10, x=1000)

        # INTRODUCTION
        self.label = Label(self, text="SOLAR EV CHARGING STATION \n  ",
                           font=controller.title_font,
                           bg="dark sea green")
        self.label.pack(side="top", fill="both", pady=250)

        # Button for PORT1
        button1 = Button(self, text="Port 1", command=lambda: controller.show_frame(pages[1]), height=1,
                         width=10, font=('Helvetica', 16), bg="aquamarine", fg="black", relief="ridge")
        button1.place(x=100, y=600)
        # Button for PORT2
        button2 = Button(self, text="Port 2", command=lambda: controller.show_frame(pages[2]), height=1,
                         width=10, font=('Helvetica', 16), bg="aquamarine", fg="black", relief="ridge")

        button2.place(x=450, y=600)


class PageOnePort1(Frame):

    def __init__(self, parent, controller, pages):
        Frame.__init__(self, parent)
        self.controller = controller
        self.pages = pages

        # FUNCTION selection- it performs function of getting selected values from excel file and send message packet
        # to slave device for I2C communication
        def selection():
            detail = variable.get()
            name.set(str(detail))
            arr = []
            # read values from excel file
            for row in range(sheet.nrows):
                if sheet.cell_value(row, 0) == detail:
                    for col in range(sheet.ncols):
                        arr.append(sheet.cell_value(row, col))  # make an Array for e.g.,arr=[I,A,28.0]
            if arr[0] == "I":
                battery_type.set("Lithium ion battery")
            else:
                battery_type.set("Lead acid battery")
            if arr[1] == "A":
                battery_voltage.set("48 V")
            elif arr[1] == "B":
                battery_voltage.set("60 V")
            else:
                battery_voltage.set("72 V")
            KEY = str(int(arr[2])) + str("  A-hr")
            battery_rating.set(KEY)
            # set values in page two of PORT 1
            controller.frames[pages[2]].label01_f1.config(text=detail)
            # make Array arrs for ALPHABETS
            arrs = [arr[0], arr[1]]
            print(arrs)

            # METHOD(function) packet returns the string packet of alphabets
            def packet(arrs):
                result = ''
                for e in arrs:
                    result += str(e)
                return result

            msg = packet(arrs)
            # I2C FUNCTION sends message
            msg1 = i2c_msg.write(addr1, msg)
            bus.i2c_rdwr(msg1)

            # I2C FUNCTION sends current rating integer value
            msg2 = i2c_msg.write(addr1, [arr[2]])
            bus.i2c_rdwr(msg2)

            # I2C FUNCTION receives acknowledgement message
            read = i2c_msg.read(addr1, 3)
            bus.i2c_rdwr(read)

            a1 = []
            # received acknowledgement array
            for value in read:
                a1.append(value)
                i = i + 1
                print(value)

            print(chr(a1[0]))
            print(chr(a1[1]))
            print(a1[2])
            # set DISPLAY settings for ACKNOWLEDGED VALUES
            if (chr(a1[0]) == "i"):
                controller.frames[pages[3]].battery_type01.config(text="Lithium ion battery")
            elif (chr(a1[0]) == "l"):
                controller.frames[pages[3]].battery_type01.config(text="Lead acid battery")
            else:
                controller.frames[pages[3]].battery_type01.config(text="    ERROR    ")
            if (chr(a1[1]) == "a"):
                controller.frames[pages[3]].battery_voltage01.config(text=" 48 V")
            elif (chr(a1[1]) == "b"):
                controller.frames[pages[3]].battery_voltage01.config(text=" 60 V")
            elif (chr(a1[1]) == "c"):
                controller.frames[pages[3]].battery_voltage01.config(text=" 72 V")
            else:
                controller.frames[pages[3]].battery_voltage01.config(text="   ERROR   ")

            controller.frames[pages[3]].battery_rating01.config(text=a1[2] + ' Ah')

            # window widgets settings

        self.label = Label(self, text="Port 1", font=('Helvetica', 20), bg="sea green", fg="white")
        self.label.pack(side="top", fill="x", pady=5)
        button = Button(self, text=" Back", command=lambda: controller.show_frame(pages[0]), height=2, width=10)
        button.place(x=40, y=600)

        button2 = Button(self, text="NEXT", bg="red", fg="white", command=lambda: controller.show_frame(pages[3]),
                         height=2, width=10)
        button2.place(x=1000, y=600)

        self.label_drop = Label(self, text="Select vehicle:", font=('verdana', 18), bg="ghost white", fg="black")
        self.label_drop.place(y=100, x=400)
        OptionList = ["      ***      ",
                      "honda flash",
                      "yo",
                      "honda optima",
                      "other"]
        variable = StringVar(self)
        variable.set(OptionList[0])
        opt = OptionMenu(self, variable, *OptionList)
        opt.config(width=19, font=('Helvetica', 16))
        opt.place(y=100, x=600)

        vehicle_name = Label(self, text="Vehicle Name:", font=('Helvetica', 18), bg="ghost white", fg="black")
        vehicle_name.place(x=400, y=200)
        go = Button(self, text="OK", height=1, command=selection)
        go.place(x=900, y=107)
        name = StringVar()
        entryName = Entry(self, textvariable=name, width=22, state="disabled", font=('Helvetica', 18))
        entryName.config(disabledforeground="black")
        entryName.place(x=600, y=200)
        battery_type = StringVar()
        vehicle_battery = Label(self, text="Battery Type:", font=('Helvetica', 18), bg="ghost white", fg="black")
        vehicle_battery.place(x=400, y=240)
        battery = Entry(self, textvariable=battery_type, width=22, state="disabled", font=('Helvetica', 18))
        battery.config(disabledforeground="black")
        battery.place(x=600, y=240)

        battery_rating = StringVar()
        battery_rate = Label(self, text="Battery Current:\n rating", font=('Helvetica', 18), bg="ghost white",
                             fg="black")
        battery_rate.place(x=400, y=280)
        battery_rating_entry = Entry(self, textvariable=battery_rating, width=22, state="disabled",
                                     font=('Helvetica', 18),
                                     bg="white", fg="black")
        battery_rating_entry.config(disabledforeground="black")
        battery_rating_entry.place(x=600, y=280)

        battery_voltage = StringVar()
        battery_volt = Label(self, text="Battery voltage", font=('Helvetica', 18), bg="ghost white", fg="black")
        battery_volt.place(x=400, y=337)
        battery_volt_entry = Entry(self, textvariable=battery_voltage, width=22, state="disabled",
                                   font=('Helvetica', 18))
        battery_volt_entry.config(disabledforeground="black")
        battery_volt_entry.place(x=600, y=337)


class PageOnePort2(Frame):

    def __init__(self, parent, controller, pages):
        Frame.__init__(self, parent)
        self.controller = controller
        self.pages = pages

        # FUNCTION selection- it performs function of getting selected values from excel file and send message packet
        # to slave device for I2C communication
        def selection_p2():
            detail_p2 = variable_p2.get()
            name_p2.set(str(detail_p2))
            arr_p2 = []
            # read values from excel file
            for row in range(sheet.nrows):
                if sheet.cell_value(row, 0) == detail_p2:
                    for col in range(sheet.ncols):
                        arr_p2.append(sheet.cell_value(row, col))
            if arr_p2[1] == "I":
                battery_type_p2.set("Lithium ion battery")
            else:
                battery_type_p2.set("Lead acid battery")
            if arr_p2[2] == "A":
                battery_voltage_p2.set("48 V")
            elif arr_p2[2] == "B":
                battery_voltage_p2.set("60 V")
            else:
                battery_voltage_p2.set("72 V")
            KEY_p2 = str((arr_p2[3])) + str("  A-hr")
            battery_rating_p2.set(KEY_p2)
            controller.frames[pages[4]].label01_f2.config(text=detail_p2)

            # set values in page two of PORT 2
            arrs_p2 = [arr_p2[1], arr_p2[2]]
            print(arrs_p2)

            # METHOD(function) packet returns the string packet of alphabets
            def packet_p2(arrs_p2):
                result = ''
                for e in arrs_p2:
                    result += str(e)
                print(result)
                return result

            msg_p2 = packet_p2(arrs_p2)
            # I2C FUNCTION sends message
            msg1_p2 = i2c_msg.write(addr2, msg_p2)
            bus.i2c_rdwr(msg1_p2)

            # I2C FUNCTION sends current rating integer value
            msg2_p2 = i2c_msg.write(addr2, [int(arr_p2[3])])
            bus.i2c_rdwr(msg2_p2)

            a1_p2 = []
            # received acknowledgement array
            read_p2 = i2c_msg.read(addr2, 3)
            bus.i2c_rdwr(read_p2)

            for value in read_p2:
                a1_p2.append(value)
                print(value)

            print(chr(a1_p2[0]))
            print(chr(a1_p2[1]))
            print(a1_p2[2])

            # set DISPLAY settings for ACKNOWLEDGED VALUES
            if (chr(a1_p2[0]) == "i"):
                controller.frames[pages[4]].battery_type01_f2.config(text="Lithium ion battery")
            elif (chr(a1_p2[0]) == "l"):
                controller.frames[pages[4]].battery_type01_f2.config(text="Lead acid battery")
            else:
                controller.frames[pages[4]].battery_type01_f2.config(text="    ERROR    ")
            if (chr(a1_p2[1]) == "a"):
                controller.frames[pages[4]].battery_voltage01_f2.config(text=" 48 V")
            elif (chr(a1_p2[1]) == "b"):
                controller.frames[pages[4]].battery_voltage01_f2.config(text=" 60 V")
            elif (chr(a1_p2[1]) == "c"):
                controller.frames[pages[4]].battery_voltage01_f2.config(text=" 72 V")
            else:
                controller.frames[pages[4]].battery_voltage01_f2.config(text="   ERROR   ")

            controller.frames[pages[4]].battery_rating01_f2.config(text=str(a1_p2[2]) + ' Ah')

        self.label_p2 = Label(self, text="Port 2", font=('Helvetica', 20), bg="sea green", fg="white")
        self.label_p2.pack(side="top", fill="x", pady=5)
        button_p2 = Button(self, text=" Back", command=lambda: controller.show_frame(pages[0]), height=2, width=10)
        button_p2.place(x=40, y=600)

        button2_p2 = Button(self, text="NEXT", bg="red", fg="white", command=lambda: controller.show_frame(pages[4]),
                            height=2, width=10)
        button2_p2.place(x=1000, y=600)

        self.label_drop_p2 = Label(self, text="Select vehicle:", font=('verdana', 18), bg="ghost white", fg="black")
        self.label_drop_p2.place(y=100, x=400)
        OptionList2 = ["      ***      ",
                       "honda flash",
                       "yo",
                       "honda optima",
                       "other"]
        variable_p2 = StringVar(self)
        variable_p2.set(OptionList2[0])
        opt_p2 = OptionMenu(self, variable_p2, *OptionList2)
        opt_p2.config(width=19, font=('Helvetica', 16))
        opt_p2.place(y=100, x=600)

        vehicle_name_p2 = Label(self, text="Vehicle Name:", font=('Helvetica', 18), bg="ghost white", fg="black")
        vehicle_name_p2.place(x=400, y=200)
        go_p2 = Button(self, text="OK", height=1, command=selection_p2)
        go_p2.place(x=900, y=107)
        name_p2 = StringVar()
        entryName_p2 = Entry(self, textvariable=name_p2, width=22, state="disabled", font=('Helvetica', 18))
        entryName_p2.config(disabledforeground="black")
        entryName_p2.place(x=600, y=200)
        battery_type_p2 = StringVar()
        vehicle_battery_p2 = Label(self, text="Battery Type:", font=('Helvetica', 18), bg="ghost white", fg="black")
        vehicle_battery_p2.place(x=400, y=240)
        battery_p2 = Entry(self, textvariable=battery_type_p2, width=22, state="disabled", font=('Helvetica', 18))
        battery_p2.config(disabledforeground="black")
        battery_p2.place(x=600, y=240)

        battery_rating_p2 = StringVar()
        battery_rate_p2 = Label(self, text="Battery Current:\n rating", font=('Helvetica', 18), bg="ghost white",
                                fg="black")
        battery_rate_p2.place(x=400, y=280)
        battery_rating_entry_p2 = Entry(self, textvariable=battery_rating_p2, width=22, state="disabled",
                                        font=('Helvetica', 18),
                                        bg="white", fg="black")
        battery_rating_entry_p2.config(disabledforeground="black")
        battery_rating_entry_p2.place(x=600, y=280)

        battery_voltage_p2 = StringVar()
        battery_volt_p2 = Label(self, text="Battery voltage", font=('Helvetica', 18), bg="ghost white", fg="black")
        battery_volt_p2.place(x=400, y=337)
        battery_volt_entry_p2 = Entry(self, textvariable=battery_voltage_p2, width=22, state="disabled",
                                      font=('Helvetica', 18))
        battery_volt_entry_p2.config(disabledforeground="black")
        battery_volt_entry_p2.place(x=600, y=337)


app = SampleApp()
app.geometry('600x600')
app.mainloop()
