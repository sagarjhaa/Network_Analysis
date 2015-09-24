# # __author__ = 'sjha1'

WIDTH = 1

#from constants import WIDTH,HEIGHT

# #
# # import Tkinter as tk
# # import tkFont
# #
# # class SampleApp(tk.Tk):
# #     def __init__(self, *args, **kwargs):
# #         tk.Tk.__init__(self, *args, **kwargs)
# #         self._textFont = tkFont.Font(name="TextFont")
# #         self._textFont.configure(**tkFont.nametofont("TkDefaultFont").configure())
# #
# #         toolbar = tk.Frame(self, borderwidth=0)
# #         container = tk.Frame(self, borderwidth=1, relief="sunken",
# #                              width=600, height=600)
# #         container.grid_propagate(False)
# #         toolbar.pack(side="top", fill="x")
# #         container.pack(side="bottom", fill="both", expand=True)
# #
# #         container.grid_rowconfigure(0, weight=1)
# #         container.grid_columnconfigure(0, weight=1)
# #         text = tk.Text(container, font="TextFont")
# #         text.grid(row=0, column=0, sticky="nsew")
# #
# #         zoomin = tk.Button(toolbar, text="+", command=self.zoom_in)
# #         zoomout = tk.Button(toolbar, text="-", command=self.zoom_out)
# #         zoomin.pack(side="left")
# #         zoomout.pack(side="left")
# #
# #         text.insert("end", '''Press te + and - buttons to increase or decrease the font size''')
# #
# #     def zoom_in(self):
# #         font = tkFont.nametofont("TextFont")
# #         size = font.actual()["size"]+2
# #         font.configure(size=size)
# #
# #     def zoom_out(self):
# #         font = tkFont.nametofont("TextFont")
# #         size = font.actual()["size"]-2
# #         font.configure(size=max(size, 8))
# #
# # if __name__ == "__main__":
# #     app = SampleApp()
# #     app.mainloop()
#
#
# # from Tkinter import *
# # import tkFont
# # root=Tk()
# # dFont=tkFont.Font(family="Arial", size=30)
# # def killme():
# #     root.quit()
# #     root.destroy()
# # LB=Text(root, width=16, height=5, font=dFont)
# # LB.grid(row=0, column=0, sticky=W+N+S)
# # yscrollbar=Scrollbar(root, orient=VERTICAL, command=LB.yview)
# # yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)
# # LB["yscrollcommand"]=yscrollbar.set
# # LB.update()
# # h=int(round(LB.winfo_height()/LB["height"])), int(round(LB.winfo_width()/LB["width"]))
# # def resize(event):
# #
# #     pixelX=root.winfo_width()-yscrollbar.winfo_width()
# #     pixelY=root.winfo_height()
# #     LB["width"]=int(round(pixelX/h[1]))
# #     LB["height"]=int(round(pixelY/h[0]))
# # root.bind("<Configure>", resize)
# # root.mainloop()
#
# # from Tkinter import *
# #
# # master = Tk()
# #
# # scrollbar = Scrollbar(master)
# # scrollbar.pack(side=RIGHT, fill=Y)
# #
# # listbox = Listbox(master, yscrollcommand=scrollbar.set)
# # for i in range(15):
# #     listbox.insert(END, str(i))
# # listbox.pack(side=LEFT, fill=BOTH)
# #
# # scrollbar.config(command=listbox.yview)
# #
# # mainloop()
#
# import Tkinter as tk
#
# class Example(tk.Frame):
#     def __init__(self, root):
#
#         tk.Frame.__init__(self, root)
#         self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
#         self.frame = tk.Frame(self.canvas, background="#ffffff")
#         self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.vsb.set)
#
#         self.vsb.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.create_window((4,4), window=self.frame, anchor="nw",
#                                   tags="self.frame")
#
#         self.frame.bind("<Configure>", self.onFrameConfigure)
#
#         self.populate()
#
#     def populate(self):
#         '''Put in some fake data'''
#         for row in range(100):
#             tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
#                      relief="solid").grid(row=row, column=0)
#             t="this is the second column for row %s" %row
#             tk.Label(self.frame, text=t).grid(row=row, column=1)
#
#     def onFrameConfigure(self, event):
#         '''Reset the scroll region to encompass the inner frame'''
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
# if __name__ == "__main__":
#     root=tk.Tk()
#     Example(root).pack(side="top", fill="both", expand=True)
#     root.mainloop()