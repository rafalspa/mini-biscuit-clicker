import tkinter as tk
from tkinter import messagebox
import pathlib
import threading
import atexit

#Open config file and assign line 1 to amount of biscuits, line 2 to BPS, line 3 to auto BPS price
config = []
f = open('config.txt')
for line in f.readlines():
    config.append(int(line))
f.close()

biscuits = config[0]
bps = config[1]
autobpsprice = config[2]

#At exit save biscuits, BPS and auto BPS price to config file
def save_config():
    con = str(biscuits) + "\n" + str(bps) + "\n" + str(autobpsprice)
    with open('config.txt', 'w') as the_file:
        the_file.write(con)

atexit.register(save_config)

#Define increase and decrease functions
def increase():
    value = int(lbl_value["text"])
    global biscuits
    lbl_value["text"] = f"{value + 1}"
    biscuits = f"{value + 1}"

def decrease():
    value = int(lbl_value["text"])
    value2 = int(lbl_value2["text"])
    global autobpsprice
    autobpsprice = int(autobpsprice)
    if value >= autobpsprice:
        lbl_value["text"] = f"{value - autobpsprice}"
        global biscuits
        global bps
        biscuits = f"{value - autobpsprice}"
        lbl_value2["text"] = f"{value2 + 1}"
        bps = f"{value2 + 1}"
        autobpsprice = autobpsprice * 2
        btn_buyauto1["text"] = "Buy Auto click (+1 Bps)\nPrice: " + str(autobpsprice) + " biscuits"
    else:
        messagebox.showerror('No money, no honey', 'You don\'t have enough biscuits to buy this upgrade!')

def autobps():
    t = threading.Timer(1, autobps)
    t.daemon = True
    t.start()
    (lbl_value["text"]) = int((lbl_value["text"])) + int(lbl_value2["text"])
    global biscuits
    biscuits = int((lbl_value["text"]))
    save_config()

window = tk.Tk()
window.title("Mini Biscuit Clicker")
window.eval('tk::PlaceWindow . center')
window.rowconfigure([0, 1], minsize=50, weight=1)
window.rowconfigure([2], minsize=100, weight=1)
window.columnconfigure([0, 1], minsize=100, weight=1)

#Top row labels
lbl_biscuits = tk.Label(master=window, text="Biscuits:")
lbl_biscuits.grid(row=0, column=0)
lbl_value = tk.Label(master=window, text=biscuits)
lbl_value.grid(row=0, column=1)
lbl_autobiscuits = tk.Label(master=window, text="Auto Bps:")
lbl_autobiscuits.grid(row=1, column=0)
lbl_value2 = tk.Label(master=window, text=bps)
lbl_value2.grid(row=1, column=1)

#Biscuit button
photo = tk.PhotoImage(file =str(pathlib.Path().absolute()) + "/biscuit.png")
photoimage = photo.subsample(1, 1)
btn_increase = tk.Button(master=window, image = photoimage ,command=increase)
btn_increase.grid(row=2, column=0, sticky="nsew")

#Auto click button
btn_buyauto1 = tk.Button(master=window, text="Buy Auto click (+1 Bps)\nPrice: " + str(autobpsprice) + " biscuits", command=decrease)
btn_buyauto1.grid(row=2, column=1, sticky="nsew")

#Add auto bps every second
autobps()

#Render the window
window.mainloop()
