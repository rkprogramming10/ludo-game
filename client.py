from msilib.schema import File
import socket
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image

screen_width = None
screen_height = None
SERVER = None
PORT = None
IP_ADDRESS = None

canvas_1 = None
playerName = None
nameEntry = None
nameWindow = None


def playerName():
    global playerName, nameEntry, nameWindow, screen_height, screen_height, canvas_1
    nameWindow = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes("`-fullscreen", True)

    # for a screen Size
    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(File='assets/background.png')

    canvas_1 = Canvas(nameWindow, width=500, height=500)
    canvas_1.pack(fill="both", expand=True)
    canvas_1.create_image(0, 0, image=bg, anchor="nw")
    canvas_1.create_text(screen_width/2, screen_height/5,
                         text="Enter your name", font=("Chalkbord SE", 100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify=CENTER,
                      bd=5, font=("Chalkboard SE", 50), bg="white")
    nameEntry.place(x=screen_width / 2 - 220, y=screen_height/4 + 100)

    button = Button(nameWindow, text='Save', font=(
        "Chalkboard SE", 30), bg="green", width=15, height=2)
    button.place(x=screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.mainloop()


def setup():
    global SERVER, PORT, IP_ADDRESS
    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    playerName()


setup()
