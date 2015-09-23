__author__ = 'sjha1'
try:
    import tkinter as tk  # for python 3
except:
    #import Tkinter as tk  # for python 2
    from Tkinter import *
    import ttk as ttk
    import ctypes
    import tkMessageBox
    import tkFileDialog
    import Tkconstants
    import shp_reader
    import dbfload as dbf
    from   main_canvas import MainCanvas,GenerateNetwork

user32 = ctypes.windll.user32
WIDTH,HEIGHT = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
WIDTH -= 20
HEIGHT -= 75
BACKGROUND = "grey"

#CONSTANTS FOR GLOBAL USE
ROOT = None
NB = None

def writeCalculations(widget,text,error):
    global NB
    if error:
        widget.tag_configure('error',foreground='red')
        widget.insert(END,text,'error')
        NB.select(1)
    else:widget.insert(END,text)

    widget.insert(END,"\n")


class Application:
    def __init__(self):
        global ROOT

        self.root = Tk()
        ROOT = self.root

        self.root.title("Network Simulator")
        self.root.geometry('%dx%d+%d+%d' % (WIDTH,HEIGHT,0,0))
        self.createUI()
        self.root.mainloop()

    def createUI(self):
        global NB

        #Divide the screen in Frames
        # We have two main Frame fr_first and fr_second
        self.fr_first = LabelFrame(self.root,text = "Controls",background=BACKGROUND,highlightcolor="red",relief=RAISED)
        self.fr_first.grid(row=0,column=0,sticky="nsew")

        self.fr_second = LabelFrame(self.root,text="Window",background=BACKGROUND,highlightcolor="red",relief=RAISED)
        self.fr_second.grid(row=0,column=1,sticky="nsew")

        #defind the controls for the fr_first
        self.btn_Simulator = Button(self.fr_first,text="Simulator",command=self.__showControls,width=20)
        self.btn_Simulator.grid(row=0,column=0,pady=10,sticky=(W,E),padx=5)

        self.btn_Analysis = Button(self.fr_first,text="Analysis",width=20)
        self.btn_Analysis.grid(row=0,column=1,pady=10,sticky=(W,E),padx=5)

        self.fr_first.grid_columnconfigure(0,weight=2)
        self.fr_first.grid_columnconfigure(1,weight=2)

        style = ttk.Style()

        style.theme_create( "mystyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [50, 1], "background": "#468499" },
            "map":       {"background": [("selected", "#cc0000")] } } } )

        style.theme_use("mystyle")

        self.nb_main = ttk.Notebook(self.fr_second)
        NB = self.nb_main
        self.nb_main.pack(expand=1,fill=BOTH)

        f1 = Frame(self.nb_main)
        self.f2 = Frame(self.nb_main)

        self.nb_main.add(self.f2,text="Canvas")
        self.nb_main.add(f1,text="Calculation")

        self.text = Text(f1)
        self.canvas = Canvas(self.f2)
        self.canvas.configure(background="black")

        

        self.text.pack(expand=1,fill=BOTH,)
        self.canvas.pack(expand=1,fill=BOTH)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=3)

    def __showControls(self):

        writeCalculations(self.text,"Showing the Simulator controls",False)
        self.obj_Sim = Simulator(self.root,self.fr_first,self.canvas,self.text)
        self.btn_Simulator.configure(state="disabled")


class Simulator(Application):

    def __init__(self,root,first_frame,canvas,text):
        self.root = root
        self.fr_first = first_frame
        self.canvas = canvas
        self.text = text

        self.fr_Simulator = Frame(self.fr_first,background=BACKGROUND)
        self.fr_Simulator.grid(row=1,column=0,columnspan=2,sticky=(W),padx=5,pady=20)

        self.btn_File = Button(self.fr_Simulator,text="File",command = self.__openShpfile)
        self.btn_File.grid(row=0,column=0,sticky=(W),ipadx=20)

        lb_Attribute = Label(self.fr_Simulator,text="Attributes",background=BACKGROUND)
        lb_Attribute.grid(row=1,column = 0,sticky=(W),pady=20)

        self.var = IntVar()
        self.c = Checkbutton(self.fr_Simulator, text="Add Layer", variable=self.var,background=BACKGROUND)
        self.c.grid(row=3,column=0,sticky=(W),pady = 20)

        self.lb_FileName = Label(self.fr_Simulator,text="No input file!!",anchor=W,background=BACKGROUND)
        self.lb_FileName.grid(row=0,column = 1,sticky=(E),padx=20,ipadx=40)

        self.btn_Draw = Button(self.fr_Simulator,text="Visulize",command = self.__UpdateCanvas)
        self.btn_Draw.grid(row=3,column=1,sticky=(E,W),pady = 20,padx = 20,ipadx=40)
        self.btn_Draw.configure(width=7)
        # writeCalculations(self.text,self.__openShpfile.__doc__,True)



    def __openShpfile(self):
        """Open a shapefile and read in the contents, pop up the attribute menu with the attributes of the shapefile"""
        print "open shape file!"
        directory=tkFileDialog.askopenfilename(filetypes=[("SHAPE_FILE","*.shp")])
        #print directory

        self.lb_FileName.config(text= directory.split("/")[-1])
        writeCalculations(self.text,"Completed reading file: " + directory.split("/")[-1],False)

        if directory == "":
            return

        self.shapes, self.shp_type, self.bbox = shp_reader.read_shp(directory)

        #read corresponding dbf data
        dbfFile = dbf.DbfLoader(directory[:-3] + "dbf")

        t = dbfFile.table2list()
        varNames = dbfFile.get_field_names()
        variables = {}
        for variable in varNames:
            #print variable, len(variable)
            variables[variable] = [record[varNames.index(variable)] for record in t]

        self.variable = StringVar(self.root)
        self.variable.set(varNames[0])
        self.lst_Attributes = apply(OptionMenu,(self.fr_Simulator,self.variable)+tuple(varNames))
        self.lst_Attributes.grid(row=1,column=1,sticky=(E,W),pady = 20,padx = 20,ipadx=40)
        self.lst_Attributes.configure(width=7)
        self.dbfdata = variables


    def __UpdateCanvas(self):
        '''This function draw the data on the canvas '''

        self.attributeSelected =  self.variable.get()
        self.datalist = self.dbfdata[self.attributeSelected]

        if self.var.get():
            self.Pre_canvas.addLayer(self.shapes, self.shp_type, self.attributeSelected,self.datalist)
        else:
            self.canvas.delete(ALL)
            self.Pre_canvas=MainCanvas(self.shapes,self.bbox,self.shp_type,self.root,self.attributeSelected,self.datalist,self.canvas)





if __name__ == '__main__':
    Application()

