# __author__ = 'sjha1'
#
# __doc__ = info = '''
# This script was written by Sunjay Varma - www.sunjay-varma.com
#
# This script has two main classes:
# Tab - Basic tab used by TabBar for main functionality
# TabBar - The tab bar that is placed above tab bodies (Tabs)
#
# It uses a pretty basic structure:
# root
# -->TabBar(root, init_name) (For switching tabs)
# -->Tab    (Place holder for content)
# 	\t-->content (content of the tab; parent=Tab)
# -->Tab    (Place holder for content)
# 	\t-->content (content of the tab; parent=Tab)
# -->Tab    (Place holder for content)
# 	\t-->content (content of the tab; parent=Tab)
# etc.
# '''
#
# from Tkinter import *
#
# BASE = RAISED
# SELECTED = FLAT
#
# # a base tab class
# class Tab(Frame):
# 	def __init__(self, master, name):
# 		Frame.__init__(self, master)
# 		self.tab_name = name
#
#
#
# # the bulk of the logic is in the actual tab bar
# class TabBar(Frame):
# 	def __init__(self, master=None, init_name=None):
# 		Frame.__init__(self, master)
# 		self.tabs = {}
# 		self.buttons = {}
# 		self.current_tab = None
# 		self.init_name = init_name
#
# 	def show(self):
# 		self.pack(side=TOP, expand=YES, fill=X)
# 		self.switch_tab(self.init_name or self.tabs.keys()[-1])# switch the tab to the first tab
#
# 	def add(self, tab):
# 		#tab.pack_forget()							# hide the tab on init
#
# 		self.tabs[tab.tab_name] = tab						# add it to the list of tabs
# 		b = Button(self, text=tab.tab_name, relief=BASE,	# basic button stuff
# 			command=(lambda name=tab.tab_name: self.switch_tab(name)))	# set the command to switch tabs
# 		b.pack(side=LEFT)												# pack the buttont to the left mose of self
# 		self.buttons[tab.tab_name] = b											# add it to the list of buttons
#
# 	def delete(self, tabname):
#
# 		if tabname == self.current_tab:
# 			self.current_tab = None
# 			self.tabs[tabname].pack_forget()
# 			del self.tabs[tabname]
# 			self.switch_tab(self.tabs.keys()[0])
#
# 		else: del self.tabs[tabname]
#
# 		self.buttons[tabname].pack_forget()
# 		del self.buttons[tabname]
#
#
# 	def switch_tab(self, name):
# 		if self.current_tab:
# 			self.buttons[self.current_tab].config(relief=BASE)
# 			self.tabs[self.current_tab].pack_forget()			# hide the current tab
# 		self.tabs[name].pack(side=BOTTOM)					# add the new tab to the display
# 		self.current_tab = name							# set the current tab to itself
#
# 		self.buttons[name].config(relief=SELECTED)				# set it to the selected style
#
# if __name__ == '__main__':
# 	def write(x): print x
#
# 	root = Tk()
# 	root.title("Tabs")
#
# 	bar = TabBar(root, "Info")
#
#
# 	tab1 = Tab(root, "Wow...")				# notice how this one's master is the root instead of the bar
# 	Label(tab1, text="Sunjay Varma is an extra ordinary little boy.\n\n\n\n\nCheck out his website:\nwww.sunjay-varma.com", bg="white", fg="red").pack(side=TOP, expand=YES, fill=BOTH)
# 	Button(tab1, text="PRESS ME!", command=(lambda: write("YOU PRESSED ME!"))).pack(side=BOTTOM, fill=BOTH, expand=YES)
# 	Button(tab1, text="KILL THIS TAB", command=(lambda: bar.delete("Wow..."))).pack(side=BOTTOM, fill=BOTH, expand=YES)
#
# 	tab2 = Tab(root, "Hi there!")
# 	Label(tab2, text="How are you??", bg='black', fg='#3366ff').pack(side=TOP, fill=BOTH, expand=YES)
# 	txt = Text(tab2, width=50, height=20)
# 	txt.focus()
# 	txt.pack(side=LEFT, fill=X, expand=YES)
# 	Button(tab2, text="Get", command=(lambda: write(txt.get('1.0', END).strip()))).pack(side=BOTTOM, expand=YES, fill=BOTH)
#
# 	tab3 = Tab(root, "Info")
# 	Label(tab3, bg='white', text="This tab was given as an argument to the TabBar constructor.\n\nINFO:\n"+info).pack(side=LEFT, expand=YES, fill=BOTH)
#
# 	bar.add(tab1)                   # add the tabs to the tab bar
# 	bar.add(tab2)
# 	bar.add(tab3)
#
# 	bar.config(bd=2, relief=RIDGE)			# add some border
#
# 	bar.show()
#
# 	print bar.tabs
#
# 	root.mainloop()
#

# from Tkinter import *
# tk = Tk()
# paned = PanedWindow(tk, orient=HORIZONTAL, showhandle=0, handlepad=0,
#         handlesize=0, sashwidth=2, opaqueresize=1)
# paned.pack(side=LEFT, expand=YES, fill=BOTH)
# for l,w in [("One",30),("Two",70)]:#,("Three",15), ("Four",30)]
#     frame = Frame(paned, border=0)
#     paned.add(frame,minsize=16)
#     lbl = Label(frame, text=l, borderwidth=1, relief=RAISED)
#     lbl.pack(fill=X)
#     lst =  Listbox(frame, width=w, background="White")
#     lst.pack(expand=YES, fill=BOTH)
#     for i in range(100): lst.insert(END,"#%d"%(i))
# tk.mainloop()

from Tkinter import *
import ttk

root = Tk()

content = ttk.Frame(root, padding=(3,3,12,12))
frame = ttk.Frame(content,borderwidth=5, relief="sunken", width=200, height=100)
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()

onevar.set(True)
twovar.set(False)
threevar.set(True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))
frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=3, row=1, columnspan=2, sticky=(N, E, W), pady=5, padx=5)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

root.mainloop()

