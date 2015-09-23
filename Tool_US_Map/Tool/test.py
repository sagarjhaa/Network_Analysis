# __author__ = 'sjha1'
#
# import Tkinter as tk
# import tkFont
#
# class SampleApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         self._textFont = tkFont.Font(name="TextFont")
#         self._textFont.configure(**tkFont.nametofont("TkDefaultFont").configure())
#
#         toolbar = tk.Frame(self, borderwidth=0)
#         container = tk.Frame(self, borderwidth=1, relief="sunken",
#                              width=600, height=600)
#         container.grid_propagate(False)
#         toolbar.pack(side="top", fill="x")
#         container.pack(side="bottom", fill="both", expand=True)
#
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#         text = tk.Text(container, font="TextFont")
#         text.grid(row=0, column=0, sticky="nsew")
#
#         zoomin = tk.Button(toolbar, text="+", command=self.zoom_in)
#         zoomout = tk.Button(toolbar, text="-", command=self.zoom_out)
#         zoomin.pack(side="left")
#         zoomout.pack(side="left")
#
#         text.insert("end", '''Press te + and - buttons to increase or decrease the font size''')
#
#     def zoom_in(self):
#         font = tkFont.nametofont("TextFont")
#         size = font.actual()["size"]+2
#         font.configure(size=size)
#
#     def zoom_out(self):
#         font = tkFont.nametofont("TextFont")
#         size = font.actual()["size"]-2
#         font.configure(size=max(size, 8))
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()


# from Tkinter import *
# import tkFont
# root=Tk()
# dFont=tkFont.Font(family="Arial", size=30)
# def killme():
#     root.quit()
#     root.destroy()
# LB=Text(root, width=16, height=5, font=dFont)
# LB.grid(row=0, column=0, sticky=W+N+S)
# yscrollbar=Scrollbar(root, orient=VERTICAL, command=LB.yview)
# yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)
# LB["yscrollcommand"]=yscrollbar.set
# LB.update()
# h=int(round(LB.winfo_height()/LB["height"])), int(round(LB.winfo_width()/LB["width"]))
# def resize(event):
#
#     pixelX=root.winfo_width()-yscrollbar.winfo_width()
#     pixelY=root.winfo_height()
#     LB["width"]=int(round(pixelX/h[1]))
#     LB["height"]=int(round(pixelY/h[0]))
# root.bind("<Configure>", resize)
# root.mainloop()