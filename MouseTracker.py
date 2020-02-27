import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, SPACE
import time
import math
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller, Button as MouseController
import pyautogui
 
while True:
    mouse_pos = queryMousePosition() #sets mouse_pos to the current position of the mouse
    print(mouse_pos.x, mouse_pos.y)
    time.sleep(.01)
    
