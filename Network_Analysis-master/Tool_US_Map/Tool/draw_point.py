##from Tkinter import *
##
##master = Tk()
##
##w = Canvas(master, width=500, height=500)
##w.pack()
##
####w.create_line(0, 0, 200, 100)
####w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
####
####w.create_rectangle(50, 25, 150, 75, fill="blue")
##
##_point = w.create_oval(50, 100, 150, 200)
##mainloop()


from Tkinter import *

master = Tk()

variable = StringVar(master)
variable.set("one") # default value

w = OptionMenu(master, variable, "one", "two", "three")
w.pack()

mainloop()
