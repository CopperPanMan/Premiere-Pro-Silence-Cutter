import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, SPACE
import time
import math
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller, Button as MouseController
import pyautogui
import matplotlib.pyplot as plt

########################################################
################ FUNCTION DEFINITIONS ##################
########################################################

def press(button):
    keyboard.press(button)
    time.sleep(waitTime)
    keyboard.release(button)
    time.sleep(waitTime)

def cutAndMove():
    #press z at X1
    click(X1+game_coords[0]+playheadOffset,playheadY)
    press('z')
    time.sleep(clickTime)
    #increment by X1 to the right
    press('h')
    pyautogui.moveTo((game_coords[0]+game_coords[2])/2,playheadY+15, duration = clickTime)
    pyautogui.drag(-X1, 0, 0.25, pyautogui.easeOutQuad)
    print("I moved this many pixels: ", X1)
    print("X1: ",X1)
    print("X2: ",X2)
    print("Cut location: ", X2-X1+game_coords[0]+playheadOffset)
    time.sleep(clickTime)
    #press q at X2-X1
    click(X2-X1+game_coords[0]+playheadOffset,playheadY) #click playhead at X2
    press('q')
    time.sleep(clickTime)

def zoomOut():
    averageC = (game_coords[2]+game_coords[0])//2
    click(averageC,971) #click middle of timeline to select
    time.sleep(.1)
    press("n") #press home to go to beginning of timeline
    for x in range(2): #zoom out 11 times
        press('-')
    click(averageC,971) #click middle of timeline to select

def prepareWindow():
    #eventually should click to select specific tracks (currently wouldnt work if they aren't selected) will always be a certain distance away from blue pixel box around timeline workspace
    averageC = (game_coords[2]+game_coords[0])//2
    click(averageC,971) #click middle of timeline to select
    time.sleep(.1)
    press("n") #press home to go to beginning of timeline
    for x in range(11): #zoom in 11 times
        press('=')
        time.sleep(waitTime)
    for y in range(3): #zoom out 5 times
        press('-')
        time.sleep(waitTime)
    click(averageC,971) #click middle of timeline to select

def takeScreenshot():
    press('v')
    click(1300,973)
    #time.sleep(.1)
    screen = np.array(ImageGrab.grab(bbox=game_coords)) #takes screenshot of bounding box. screen is an image
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) #cv2.COLOR_BGR2GRAY translates rgb image to grayscale. converts the screen image array to grayscale
    return screen

def resetWorkspace():
    press('h')
    pyautogui.moveTo(game_coords[2],playheadY+15, duration = clickTime)
    pyautogui.drag((game_coords[0]-game_coords[2]), 0, 0.5, pyautogui.easeOutQuad)
    #mouse.click(Button.left)
    #mouse.moveTo(game_coords[0],1000)
    #mouse.release(Button.left)

def resetVariables():
    global coordinate
    coordinate = 1
    global X2
    X2 = 0
    global X1
    X1 = 0

###########################################
######## INITIALIZING VARIABLES ###########
###########################################

#inputLeftX = 0
#inputRightX = 3440
#inputTopY = 0
#inputBottomY = 1439

inputLeftX = int(input('Enter leftmost X value of screen that Premiere is on: '))
inputRightX = int(input('Enter rightmost X value of screen that Premiere is on: '))
inputTopY = int(input('Enter top Y value of screen that Premiere is on: '))
inputBottomY = int(input('Enter bottom Y value of screen that Premiere is on: '))
NewArray = [inputLeftX, inputTopY, inputRightX, inputBottomY]

global x, y, X1, X2, coordinate, sleepVAR1, gap, acceptableGap, audioLevel, sleepVAR1, playheadOffset, iterationCount, rightX, leftX, rightY, leftY, playheadY, boolval
boolval, x, y, X1, X2, coordinate = 1, 0, inputBottomY, 0, 0, 1

Yellow = [240, 240, 0]
DGray = [32, 32, 32]
DSilence = [41, 92, 44]
GreenAudio = [81, 184, 88]
Gray = [38, 38, 38]

prescreen = np.array(ImageGrab.grab(bbox=NewArray))
#prescreen = cv2.cvtColor(prescreen, cv2.COLOR_BGR2GRAY)

#plt.imshow(prescreen)
#plt.show()

#while True:
#    mouse_pos = queryMousePosition() #sets mouse_pos to the current position of the mouse
#    print("color value at (",mouse_pos.x, ",", mouse_pos.y,")",prescreen[mouse_pos.y][mouse_pos.x])

###################################################
########### FINDING THE TIMELINE ##################
###################################################

while boolval: #find bottom left corner
    while x < inputRightX-1:
        if (prescreen[y-1][x] == GreenAudio).all() or (prescreen[y-1][x] == DSilence).all():
            if x < inputRightX - 30:
                if (prescreen[y][x+30] == GreenAudio).all or (prescreen[y-1][x] == DSilence).all():
                    leftX = x
                    bottomY = y
                    boolval = 0
                    break
        x = x + 10
    x = 0
    y = y - 1

x = leftX + 1
while True: #find bottom right corner
    if (prescreen[y][x] != GreenAudio).all() and (prescreen[y][x] != DSilence).all():
        x = x - 5
        rightX = x
        break
    x = x + 1

x = rightX
while True: #find top right corner. Increment down y until you find gray
    y = y - 1
    if (prescreen[y][x] == Gray).all():
        topY = y + 1
        break

while True: #find playhead Y value
    y = y - 1
    if (prescreen[y][x] == Yellow).all():
        playheadY = y - 6
        break

game_coords = [leftX+10, int((bottomY+topY)/2), rightX, bottomY]
keyboard = KeyboardController() 
previous_clicks = []

gap, acceptableGap, playheadOffset = 12, 40, 2
acceptableGap = int(input('Enter minSilence: '))
gap = int(input('Enter gap: '))
userAudioLevel = input('Enter Audio Level (1-20): ')
audioLevel = int((float(game_coords[3])-((float(game_coords[3]-game_coords[1]))*.05*float(userAudioLevel))))
lowerLevel = int(0.1*(bottomY+topY)/2)
waitTime = .01
clickTime = .1
sleepVAR1 = .1
iterationCount = 0

prepareWindow()
screen = np.array(ImageGrab.grab(bbox=game_coords)) # I believe takes screenshot of bounding box. screen is an image
screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) #cv2.COLOR_BGR2GRAY translates rgb image to grayscale. I believe this converts the screen image array to grayscale
pyautogui.moveTo(game_coords[0], audioLevel, duration = .5)
pyautogui.moveTo(game_coords[2], audioLevel, duration = 2)


###########################################
############### MAIN LOGIC ################
###########################################


while True:

    while True: #FIND LIGHT PIXEL by incrementing across

        # If AT END OF WORKSPACE
        if coordinate > (game_coords[2]-game_coords[0]-2):
            X2 = coordinate - 1 - gap #the location right before light pixel
            if (X2 - X1) > (acceptableGap): #if gap is big enough #ISSUE WITH THIS LOGIC RIGHT HERE
                cutAndMove()
                resetVariables()
                screen = takeScreenshot()
                break
            resetWorkspace()
            resetVariables()
            screen = takeScreenshot()

        #IF LIGHT PIXEL IS REACHED
        if screen[audioLevel-game_coords[1],coordinate] > 130:
            #SEARCH FOR LIGHT PIXELS TO THE BOTTOM LEFT
            X2 = coordinate - 1 - gap
            #print("FOUND A LIGHT PIXEL AT ", coordinate)
            X2 = coordinate - 1 - gap #the location right before light pixel
            if (X2 - X1) > (acceptableGap): #ISSUE WITH THIS LOGIC, NOT CUTTING IN CORRECT LOCATIONS. CHECK X1 AND X2?
                print("X2-X1: ", (X2-X1))
                print("CUTTING BECAUSE LIGHT PIXEL WAS FOUND AT [",coordinate,"]")
                cutAndMove()
                #if iterationCount == 1:
                 #   print("Iteration 3: ", iterationCount)
                  #  for i in range(len(screen[0])):
                   #     print("this is the value of screen at ", i, ": ", screen[audioLevel-game_coords[1],i])
                   # print("i")
                resetVariables()
                screen = takeScreenshot()
                iterationCount = iterationCount + 1
                break
            break

        #IF AT END OF PROJECT
        if screen[audioLevel-game_coords[1], coordinate] < 35:  #checks if pixel is really dark at coordinate (end of workspace)
            X2 = coordinate - 1 - gap
            cutAndMove()
            zoomOut()            
            exit()
        coordinate = coordinate + 1
        #print("Screenshot[",coordinate, "] = Dark Pixel")

    while True: #FIND DARK PIXEL by incrementing across

        #IF AT END OF WORKSPACE
        if coordinate > (game_coords[2]-game_coords[0]-2):
            resetWorkspace()
            resetVariables()
            screen = takeScreenshot()

        #IF DARK PIXEL IS REACHED
        if screen[audioLevel-game_coords[1], coordinate] < 130 and screen[audioLevel-game_coords[1], coordinate] > 35:
            while True:
                #IF AT END OF WORKSPACE
                if coordinate > (game_coords[2]-game_coords[0]-2):
                    resetWorkspace()
                    resetVariables()
                    screen = takeScreenshot()
                if screen[game_coords[3]-game_coords[1]-lowerLevel, coordinate+1] > 130:
                    coordinate = coordinate + 1
                else:
                    break
            X1 = coordinate + gap
            #print("X1 incremented in loop. Now = ", X1)
            coordinate = coordinate + 1 #optional but saves computions
            break
        coordinate = coordinate + 1
        #print("Screenshot[",coordinate, "] = Light Pixel")
