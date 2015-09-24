__author__ = 'sjha1'

import ctypes
user32 = ctypes.windll.user32
WIDTH,HEIGHT = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
WIDTH -= 20
HEIGHT -= 75
canvasWidth,canvasHeight,margin_x, margin_y = WIDTH, HEIGHT,0,0
BACKGROUND = "Grey"


