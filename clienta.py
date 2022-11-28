import random
import socket
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image

screen_width = None
screen_height = None
SERVER = None
PORT = None
IP_ADDRESS = None

player_1name = 'joining'
player_2name = 'joining'
player_1label = None
player_2label = None
player1_score = 0
player2_score = 0
player1_scorelable = None
player2_scorelable = None
winingmsg = None
winningfunction_call = 0

canvas_1 = None
playerName = None
nameEntry = None
nameWindow = None
canvas_2 = None
dice = None
gameWindow = None
left_boxes = []
right_boxes = []
finishingBox = None
playerType = None
rollButton = None
playerTurn = None
resetButton = None


def checkColorPosition(boxes, color):
    for box in boxes:
        boxColor = box.cget('bg')
        if (boxColor == color):
            return boxes.index(box)
    return False


def movePlayer1(steps):
    global left_boxes
    boxPosition = checkColorPosition(left_boxes[1:], 'red')
    if (boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        toltalSteps = 10
        remaininigStep = toltalSteps-coloredBoxIndex
        if (steps == remaininigStep):
            for box in left_boxes[1:]:
                box.config(bg='white')
            global finishingBox
            finishingBox.config(bg='red')
            global SERVER, playerName
            greetMessage = f'red Wins the Game'
            SERVER.send(greetMessage.encode())
        elif (steps < remaininigStep):
            for box in left_boxes[1:]:
                box.config(bg='white')
            nextstep = (coloredBoxIndex + 1) + diceValue
            left_boxes[nextstep].config(bg='red')
        else:
            print("Move False")
    else:
        left_boxes[steps].config(bg='red')


def movePlayer2(steps):
    global right_boxes
    tempbox = right_boxes[-2::-1]
    boxPosition = checkColorPosition(tempbox, 'yellow')
    if (boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        toltalSteps = 10
        remaininigStep = toltalSteps-coloredBoxIndex
        if (diceValue == remaininigStep):
            for box in right_boxes[-2::-1]:
                box.config(bg='white')
            global finishingBox
            finishingBox.config(bg='yellow')
            global SERVER, playerName
            greetMessage = f'yellow Wins the Game'
            SERVER.send(greetMessage.encode())
        elif (diceValue < remaininigStep):
            for box in right_boxes[-2::-1]:
                box.config(bg='white')
            nextstep = (coloredBoxIndex + 1) + diceValue
            right_boxes[::-1][nextstep].config(bg='yellow')
        else:
            print("Move False")
    else:
        right_boxes[len(right_boxes) - (steps + 1)].config(bg='yellow')


def rollDice():
    global SERVER
    diceChoices = ['\u2680', '\u2681', '\u2682',
                   '\u2683', '\u2684', '\u2685']  # dice number
    value = random.choice(diceChoices)
    global rollButton, playerTurn, playerType
    rollButton.destroy()
    playerTurn = False
    if (playerType == 'player1'):
        SERVER.send(f'{value}player2Turn'.encode())
    if (playerType == 'player2'):
        SERVER.send(f'{value}player1Turn'.encode())


def finishingBox():
    global gameWindow, finishingBox, screen_height, screen_width
    finishingBox = Label(gameWindow, text='Home', font=(
        'Helvetica', 18), width=8, height=5, borderwidth=0, bg='green', fg='white')
    finishingBox.place(x=screen_width/2-55, y=screen_height/2-70)


def leftBoard():
    global gameWindow, left_boxes, screen_height
    xpos = 10
    for box in range(0, 11):
        if (box == 0):
            boxLable = Label(gameWindow, font=(
                "Helvetica", 30), width=2, height=1, relief='ridge', borderwidth=0, bg='red')
            boxLable.place(x=xpos, y=screen_height/2-88)
            left_boxes.append(boxLable)
            xpos += 50
        else:
            boxLable = Label(gameWindow, font=(
                "Helvetica", 40), width=2, height=1, relief='ridge', borderwidth=0, bg='white')
            boxLable.place(x=xpos, y=screen_height/2-100)
            left_boxes.append(boxLable)
            xpos += 65


def rightBoard():
    global gameWindow, screen_height, right_boxes
    xpos = 820
    for box in range(0, 11):
        if (box == 10):
            boxLable = Label(gameWindow, font=(
                "Helvetica", 30), width=2, height=1, relief='ridge', borderwidth=0, bg='yellow')
            boxLable.place(x=xpos, y=screen_height/2-88)
            right_boxes.append(boxLable)
            xpos += 50
        else:
            boxLable = Label(gameWindow, font=(
                "Helvetica", 40), width=2, height=1, relief='ridge', borderwidth=0, bg='white')
            boxLable.place(x=xpos, y=screen_height/2-100)
            right_boxes.append(boxLable)
            xpos += 65


def gameWindow():
    global gameWindow, canvas_2, screen_height, screen_width, dice, winingmsg, resetButton
    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes("-fullscreen", True)
    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    canvas_2 = Canvas(gameWindow, width=500, height=500)
    canvas_2.pack(fill="both", expand=True)
    bg = ImageTk.PhotoImage(file='./assets/background.png')

    canvas_2.create_image(0, 0, image=bg, anchor="nw")

    canvas_2.create_text(screen_width/2, screen_height/5,
                         text="Ludo Ladder", font=("Chalkboard SE", 100), fill='white')

    winingmsg = canvas_2.create_text(
        screen_width/2+10, screen_height/250+100, text='', font=('Chalkboard SE', 100), fill='green')

    resetButton = Button(gameWindow, text='Roll',font=(
        'Chalkboard SE ', 15), bg='grey', width=20, height=5)

    leftBoard()
    
    rightBoard()
    finishingBox()
    global rollButton
    rollButton = Button(gameWindow, text='Roll', command=rollDice, font=(
        'Chalkboard SE ', 15), bg='grey', width=20, height=5)
    global playerTurn, playerType, playerName, player_1name, player_2name, player1_score, player2_score, player_1label, player_2label, player2_scorelable, player1_scorelable
    if (playerType == 'player1' and playerTurn):
        rollButton.place(x=screen_width/2-80, y=screen_height/2+150)
    else:
        rollButton.pack_forget()

    dice = canvas_2.create_text(screen_width/2+10, screen_height /
                                2+100, text='\u2680', font=('Chalkboard SE', 250), fill='white')
    gameWindow.resizable(True, True)
    gameWindow.mainloop()


def save_name():
    global SERVER, nameEntry, nameWindow, playerName
    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()
    SERVER.send(playerName.encode())
    gameWindow()


def askPlayerName():
    global playerName, nameEntry, nameWindow, canvas_1
    nameWindow = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes("-fullscreen", True)

    # for a screen Size
    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file='./assets/background.png')

    canvas_1 = Canvas(nameWindow, width=500, height=500)
    canvas_1.pack(fill="both", expand=True)
    canvas_1.create_image(0, 0, image=bg, anchor="nw")
    canvas_1.create_text(screen_width/2, screen_height/5,
                         text="Enter your name", font=("Chalkbord SE", 100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify=CENTER,
                      bd=5, font=("Chalkboard SE", 50), bg="white")
    nameEntry.place(x=screen_width / 2 - 220, y=screen_height/4 + 100)

    button = Button(nameWindow, text='Save', command=save_name, font=(
        "Chalkboard SE", 30), bg="green", width=15, height=2)
    button.place(x=screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()


def handleWin(message):
    global playerType, rollButton, winingmsg, canvas_2, screen_width, screen_height, resetButton
    if 'red' in message:
        if playerType == 'player2':
            rollButton.destroy()
    if 'yellow' in message:
        if playerType == 'player1':
            rollButton.destroy()
    message = message.split('.')[0] + '.'
    canvas_2.itemconfigure(winingmsg, text=message)
    resetButton.place(x=screen_width/2-80, y=screen_height-220)


def receivedmsg():
    global SERVER, playerType, playerTurn, rollButton, screen_height, screen_width, dice, canvas_2, gameWindow, player_1name, player_2name, player_2label, player_1label, winningfunction_call
    while True:
        message = SERVER.recv(2048).decode()
        if 'player_type' in message:
            recvmsg = eval(message)
            playerType = recvmsg['player_type']
            playerTurn = recvmsg['turn']
        elif 'player_names' in message:
            players = players['player_names']
            for p in players:
                if p['type'] == 'player1':
                    player_1name = p['name']
                if p['type'] == 'player2':
                    player_2name = p['name']
        elif '⚀' in message:
            canvas_2.itemconfigure(dice, text='\u2680')
        elif '⚁' in message:
            canvas_2.itemconfigure(dice, text='\u2681')
        elif '⚂' in message:
            canvas_2.itemconfigure(dice, text='\u2682')
        elif '⚃' in message:
            canvas_2.itemconfigure(dice, text='\u2683')
        elif '⚄' in message:
            canvas_2.itemconfigure(dice, text='\u2684')
        elif '⚅' in message:
            canvas_2.itemconfigure(dice, text='\u2685')
        elif 'wins the game' in message and winningfunction_call == 0:
            winningfunction_call += 1
            handleWin(message)
        if 'player1_turn' in message and playerType == 'player1':
            playerTurn = True
            rollButton = Button(gameWindow, text='RollDice', command=rollDice, font=(
                'Chalkboard SE', 15), bg='grey', width=20, height=5)
            rollButton.place(x=screen_width/2-80, y=screen_height/2+250)

        elif 'player2_turn' in message and playerType == 'player2':
            playerTurn = True
            rollButton = Button(gameWindow, text='RollDice', command=rollDice, font=(
                'Chalkboard SE', 15), bg='grey', width=20, height=5)
            rollButton.place(x=screen_width/2-80, y=screen_height/2+250)

        if 'player1_turn' in message or 'player2_turn' in message:
            diceChoices = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
            diceValue = diceChoices.index(message[0]) + 1
            if 'player2_turn' in message:
                movePlayer1(diceValue)
            if 'player1_turn' in message:
                movePlayer2(diceValue)


def setup():
    global SERVER, PORT, IP_ADDRESS
    IP_ADDRESS = '127.0.0.1'
    PORT = 8000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    thread = Thread(target=receivedmsg)
    thread.start()
    askPlayerName()


setup()
