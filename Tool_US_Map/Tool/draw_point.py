from Tkinter import *

master = Tk()

w = Canvas(master, width=500, height=500)
w.pack()

##w.create_line(0, 0, 200, 100)
##w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
##
##w.create_rectangle(50, 25, 150, 75, fill="blue")

a= [327.0, 65, 330.0, 62, 331.0, 62, 332.0, 65, 332.0, 67, 330.0, 66, 327.0, 67, 329.0, 69, 329.0, 74, 330.0, 74, 332.0, 77, 332.0, 79, 331.0, 81, 330.0, 80, 330.0, 78, 328.0, 78, 327.0, 75, 327.0, 69, 326.0, 67, 327.0, 65]
_point = w.create_polygon(a)


##from Tkinter import *
##
##master = Tk()
##
##variable = StringVar(master)
##variable.set("one") # default value
##
##w = OptionMenu(master, variable, "one", "two", "three")
##w.pack()
##

mainloop()
