#Return all the code of the last scrip in this file
import pafy
from colorama import init, Fore, Back, Style, Cursor

link = "https://www.youtube.com/watch?v=czKFHqlH158"
video = pafy.new(link)
best = video.getbest()

def XD(total,recvd,ratio,rate,eta):
    msg = "Se descargó "+str(round(recvd/1000000, 2))+" de "+str(round(total/1000000, 2))+" Mg a una velocidad de "+str(int(rate))+" kbps/s"
    print(Fore.CYAN + "========================================================================================")
    print(Cursor.UP(1)+Cursor.FORWARD(20)+Fore.YELLOW+str(msg))

best.download(quiet=True, callback=XD)