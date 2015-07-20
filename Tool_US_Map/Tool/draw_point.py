##from Tkinter import *
##
##master = Tk()
##
##w = Canvas(master, width=500, height=500)
##w.pack()
##
##Shape E
##points = [70, 110, 90, 150, 130, 170, 90, 190, 70, 230, 50, 190, 10, 170, 50, 150]
##w.create_polygon(points, width=2, fill='green', outline='blue')
##
##points = [100, 140, 110, 110, 140, 100, 110, 90, 100, 60, 90, 90, 60, 100, 90, 110]
##
##w.create_polygon(points, outline="#476042", 
##            fill='yellow', width=3)
##
##mainloop()

#ScrollBar Program
from Tkinter import *

master = Tk()

scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(master, yscrollcommand=scrollbar.set)
for i in range(1000):
    listbox.insert(END, str(i))
listbox.pack(side=LEFT, fill=BOTH)

scrollbar.config(command=listbox.yview)

mainloop()

#Bitmap Program

##from Tkinter import *
##
##canvas_width = 300
##canvas_height =80
##
##master = Tk()
##canvas = Canvas(master, 
##           width=canvas_width, 
##           height=canvas_height)
##canvas.pack()
##
##bitmaps = ["error", "gray75", "gray50", "gray25", "gray12", "hourglass", "info", "questhead", "question", "warning"]
##nsteps = len(bitmaps)
##step_x = int(canvas_width / nsteps)
##
##for i in range(0, nsteps):
##   canvas.create_bitmap((i+1)*step_x - step_x/2,50, bitmap=bitmaps[i])
##
##mainloop()
