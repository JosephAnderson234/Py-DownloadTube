from tkinter import *
from tkinter.ttk import Progressbar
import requests
import pafy
import os
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
import threading

varbg = "#ffdead"
varfg = "Red"
vartercer = "#98fb98"

class Descargar(Toplevel):
    def __init__(self,master=None, url=None, name=None, path=None):
        super(Descargar, self).__init__(master)
        self.url = url
        self.name = name
        self.path = path
        self.imagen = ""
        self.video_pafy = pafy.new(self.url)
        self.name_of_video =  self.video_pafy.title      
        self.video_best = self.video_pafy.getbest(preftype="mp4", ftypestrict=True)
        self.dif = 0
        self.master.configure(bg=varbg)     
        self.create_widgets()
        self.main = threading.Thread(target=self.donwload_main)
        self.main.start()
    
    def configure_characters(self):
        """Donwload the image fo miniatures"""
        try:
            os.remove("img_caché/youtube.jpg")
            url_miniature = self.video_pafy.thumb
            image_dw = requests.get(url_miniature)
            file = open("youtube.jpg", "wb")
            file.write(image_dw.content)
            file.close()
            """Create the local image"""
            self.imagen = PhotoImage(file="youtube.jpg")
        except:
            url_miniature = self.video_pafy.thumb
            image_dw = requests.get(url_miniature)
            file = open("youtube.jpg", "wb")
            file.write(image_dw.content)
            file.close()
            self.imagen = ImageTk.PhotoImage(Image.open("youtube.jpg"))  # PIL solution
    def up_description(self):
        self.description_label.config(state=NORMAL)
        self.description_label.delete(1.0, END)
        self.description_label.insert(END, self.video_pafy.description)
        self.description_label.config(state=DISABLED)
    def mycb(self, total, recvd, ratio, rate, eta):
        self.recvd_2 = (recvd*100/total)
        self.rate_2 = rate
        self.progress.step(self.recvd_2-self.dif)
        self.dif = self.recvd_2
        if self.recvd_2 == 100:
            messagebox.showinfo("Descarga Completa", "Descarga Completa")
            self.destroy()
    
    def donwload_main(self):
        try:
            self.video_best.download(filepath=self.path, quiet=True, callback=self.mycb)
        except KeyboardInterrupt:
            messagebox.showerror("Descarga Cancelada")
    def create_widgets(self):
        self.characters_img = threading.Thread(target=self.configure_characters())
        self.characters_img.start()
        """Create the label of image"""
        try:
            self.image_label = Label(self, image=self.imagen)
            self.image_label.place(x=13, y=69, width=231, height=130)
        except TclError:
            messagebox.showwarning("ERROR", "No se ha podido descargar la miniatura")
        """Create a title of video's Youtube"""
        self.title = Label(self, text=self.name_of_video[0:15], font=("Arial", 18), bg=vartercer, fg="red", anchor=CENTER)
        self.title.place(x=0, y=0, width=500, height=52)
        """Create the label of description"""
        self.description_label = Text(self, font=("Arial", 10), bg=vartercer, fg="red")
        self.description_label.config(state=DISABLED)
        self.description_label.place(x=265, y=66, width=216, height=133)
        """Update the description of video"""
        self.up_description()
        self.progress = Progressbar(self, orient=HORIZONTAL, length=100, mode='determinate')
        self.progress.place(x=17, y=216, width=465, height=24)

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=500, height=350)
        self.master = master
        self.config(bg=varbg)
        self.pack( fill=BOTH, expand=True)
        self.create_main()
    def create_main(self):
        """Titúlo"""
        self.title = Label(self, text="Free Donwload", font=("Cooper Black", 20), fg="red", bg=vartercer)
        self.title.place(x=0, y=0, width=500, height=50)
        
        """Eqitequeta de descripción para url_input"""
        self.nm_url = Label(self, text="URL:", font=("Arial", 10), fg="black", bg=varbg)
        self.nm_url.place(x=200, y=60, width=100, height=20)
        
        """Entrada del url"""
        self.url_input = Entry(self, width=70, bg=varbg, fg="black", font=("Arial", 10))
        self.url_input.place(x=50, y=100, width=400, height=20)
        
        """Etiqueta de descripción para name_input"""
        self.nm_name = Label(self, text="Nombre del video:", font=("Arial", 10), fg="black", bg=varbg)
        self.nm_name.place(x=150, y=140, width=200, height=20)
        
        """Entrada del nombre del archivo"""
        self.name_input = Entry(self, width=70, bg=varbg, fg="black", font=("Arial", 10))
        self.name_input.place(x=50, y=170, width=400, height=20)
        
        """Etiqueta de descripción para directory_input"""
        self.nm_directory = Label(self, text="Directorio:", font=("Arial", 10), fg="black", bg=varbg)
        self.nm_directory.place(x=150, y=210, width=200, height=20)
        
        """Entrada del directorio"""
        self.directory_input = Entry(self, width=70, bg=varbg, fg="black", font=("Arial", 10))
        self.directory_input.place(x=50, y=240, width=400, height=20)
        
        """Se sobreescribe el directorio por defecto(default) en directory_input"""
        self.directory_now = os.getcwd()
        self.directory_input.insert(0, self.directory_now)
        
        """Bloquear la edición el input"""
        self.directory_input.config(state="readonly")
        
        """Funcion para cambiar el directorio"""
        def change_directory_function():
            self.directory_input.config(state=NORMAL)
            dfile = filedialog.askdirectory(parent=self, title="Seleccione la carpeta de destino")
            self.directory_input.delete(0, END)
            self.directory_input.insert(0, dfile)
            self.directory_input.config(state="readonly")
        
        """Se crea el boton de cambiar directorio"""
        self.change_directory = Button(self, text="...", command=change_directory_function, bg=varbg, fg="black", font=("Arial", 10))
        self.change_directory.place(x=450, y=240, width=20, height=20)
        
        """Se crea el boton de descargar"""
        self.donwload_bt = Button(self, text="Descargar", command=self.comprobate, bg=varbg, fg="black", font=("Cooper Black", 14))
        self.donwload_bt.place(x=175, y=280, width=150, height=50)
    def comprobate(self):
        """Se comprueba que los campos estén llenos"""
        if self.url_input.get() == "":
            self.url_input.config(bg="red")
            messagebox.showerror("Error", "No se ha ingresado una URL")
        if self.name_input.get() == "":
            self.name_input.config(bg="red")
            messagebox.showerror("Error", "No se ha ingresado un nombre")
        if self.directory_input.get() == "":
            self.directory_input.config(bg="red")
            messagebox.showerror("Error", "No se ha ingresado un directorio")
        self.comprobate2()
    def comprobate2(self):
        try:
            test = pafy.new(self.url_input.get())
            print(test.title)
            self.newTop = Descargar(self.master, self.url_input.get(), self.name_input.get(), self.directory_input.get())
            self.newTop.resizable(width=False, height=False)
            self.newTop.configure(bg=varbg)
            self.newTop.geometry("500x300")
            self.newTop.geometry("500x300")
            self.newTop.grab_set() # Mantiene el foco de la venhtana hasta que se cierre y devuelve la interacción con la ventana principal el root en este caso.
            self.newTop.focus_set() # Mantiene el foco cuando se abre la ventana.
            self.newTop.mainloop()
        except ValueError:
            messagebox.showerror("Error", "No se ha ingresado una URL valida")
            self.url_input.delete(0, END)
        
        
"""Start with the GUI"""
window = Tk()
window.geometry("500x350")
window.configure(bg=varbg)
window.resizable(False, False)
window.iconbitmap("icon.ico")
window.title("Free Download")
app = App(window)
app.mainloop()