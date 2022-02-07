
import pafy

url = "https://youtu.be/D9G1VOjN_84"
video = pafy.new(url)
streams = video.allstreams
number = len(streams)
stream = streams[int(round(number/2, 0))]
#stream.download()

#Print all the streams using a bucle for
"""for i in range(number):
    print("==========================================================")
    print(streams[i].resolution)"""
from tkinter import *
from tkinter import ttk


app = Tk()
app.geometry("500x500")

combobox = ttk.Combobox(app, state="readonly", values=streams)
combobox.pack()

boton = Button(app, text="Download", command=lambda: print(combobox.get()))
boton.pack()

app.mainloop()