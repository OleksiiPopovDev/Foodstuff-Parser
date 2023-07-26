import pyautogui
from time import sleep
from random import randint


pyautogui.PAUSE = 1.5
pyautogui.FAILSAGE = True
screen_width , screen_height = pyautogui.size()

def getNextPos():
    x = randint(0, screen_width - 1)
    y = randint(0, screen_height -1)
    return x , y

def move():
    x,y = getNextPos()
    print("Moving to ({},{})".format(x,y))
    pyautogui.moveTo(x,y, duration=0.25)
    sleep(1)

print("Press CTRL-C to Stop")
while True:
    move()