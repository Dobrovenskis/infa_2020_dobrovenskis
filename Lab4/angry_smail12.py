import pygame
from pygame.draw import *
import numpy as np


def brow(screen, x_b, y_b, ling, wight, angle):
    polygon(screen, (0, 0, 0), [(x_b, y_b), (int(x_b - ling*np.cos(angle)), int(y_b - ling*np.sin(angle))), \
                           (x_b - int(ling*np.cos(angle) - wight*np.sin(angle)),int(y_b - ling*np.sin(angle) - wight*np.cos(angle))), \
                           (x_b + int(wight*np.sin(angle)), y_b - int(wight*np.cos(angle))), (x_b, y_b)])
    
def angry_smail(screen, x, y, z):
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    YEL = (255, 255, 0)



    circle(screen, YEL, (x, y), 100//z)

    circle(screen, RED, (x - 50//z, y - 25//z), 30//z)
    circle(screen, BLACK, (x - 50//z, y - 25//z), 30//z, 1)
    circle(screen, BLACK, (x - 50//z, y - 25//z), 10//z)

    circle(screen, RED, (x + 50//z, y - 25//z), 20//z)
    circle(screen, BLACK, (x + 50//z, y - 25//z), 20//z, 1)
    circle(screen, BLACK, (x + 50//z, y- 25//z), 10//z)

    rect(screen, BLACK, (x - 50//z, y + 50//z, 100//z, 20//z))
    brow(screen, x - 20//z,y - 30//z, 100//z, 10//z, 0.7)
    brow(screen, x + 20//z, y - 30//z, 100//z, 10//z, 2)
