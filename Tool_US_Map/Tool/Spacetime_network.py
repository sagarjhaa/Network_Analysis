'''
Created on March 17, 2015

@author: sagar jha
'''

#from Tkinter import Tk,Menu,Canvas,Scale

from   Tkinter import *
from   shp_reader import SHP_TYPE_POINT,SHP_TYPE_LINE,SHP_TYPE_POLYGON,Polygon
from   main_canvas import MainCanvas,GenerateNetwork
import Tkconstants
import tkFileDialog
import shp_reader
import random as rd
import dbfload as dbf
import Tkinter as tk  #For the setting


Communities = 1
n1,n2,n3,n4 = 1,1,1,1
p1,p2,p3,p4 = 0,0,0,0
l1,l2,l3,l4 = 0,0,0,0

class Network:

    def __init__(self):

        self.root = Tk()
        self.root.state("zoomed")
        self.root.title("Network Simulator")
        self.createMenu()
        self.root.mainloop()

    def createMenu(self):       
        """
        Creates GUI components and register events
        """
        self.menubar = Menu(self.root)
        self.dbfdata = None
        
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.__openShpfile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        
        self.attibmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Attibutes", menu=self.attibmenu,state='disabled')
        self.menubar.add_cascade(label="Settings", command = self.onClick)
        self.root.config(menu=self.menubar)

    def onClick(self):
        inputDialog = Settings(self.root)
        self.root.wait_window(inputDialog.top)    

    def __openShpfile(self):
        """
        Open a shapefile and read in the contents, pop up the attribute menu 
        with the attributes of the shapefile
        """   
        print "open shape file!"
        directory=tkFileDialog.askopenfilename(filetypes=[("SHAPE_FILE","*.shp")])
        print directory
        
        if directory == "":
            return
        
        self.shapes, self.shp_type, self.bbox = shp_reader.read_shp(directory)
        #read corresponding dbf data
        dbfFile = dbf.DbfLoader(directory[:-3] + "dbf")
        
        t = dbfFile.table2list()
        varNames = dbfFile.get_field_names()
        variables = {}
        for variable in varNames:
            variables[variable] = [record[varNames.index(variable)] for record in t]
            
        if self.dbfdata!=None:
            self.attibmenu.delete(0, len(self.dbfdata)-1)
            
        #add attributes into menu
        for key in variables.keys():  
            self.__addAttribute(key)
        
        self.dbfdata = variables
        self.menubar.entryconfig(2, state=Tkconstants.NORMAL)
        #self.__updateCanvas("STATE_NAME")
    
    def __addAttribute(self,attributeName):
        """
        Add an attribute to the menu
        """
        self.attibmenu.add_command(label=attributeName, command=lambda i=attributeName:self.__updateCanvas(i))

    def __updateCanvas(self, attributeName):
        """
        Updates the canvas and showing statistical information
        """
        print "update Canvas "+attributeName
        self.datalist=self.dbfdata[attributeName]

        self.root.grid()
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)
        self.canvas=MainCanvas(self.shapes,self.bbox,self.shp_type,self.root,attributeName,self.datalist)
        
    
class Settings:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.top.title('Settings')

        #Community Control
        self.spinbox_Label= tk.Label(top, text='Number of Community?')
        self.spinbox_Label.grid(row=0, column=0)

        self.spinbox_Label= tk.Label(top,text='Community:')
        self.spinbox_Label.grid(row=1, column=0)

        self.No_Nodes_Scale = tk.Scale(top,from_=1, to=4,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale.set(Communities)
        self.No_Nodes_Scale.bind("<ButtonRelease-1>",self.changeCommunities)
        self.No_Nodes_Scale.grid(row=1,column=1)

        ##############################################################################################################################
        #Network Control
        self.variable = StringVar(top)
        self.variable.set("GenStar")
        self.options = tk.OptionMenu(top,self.variable,"GenStar","GenRndGnm","GenForestFire")
        self.options.grid(row = 1,column=2)
        

        ##############################################################################################################################
        #Node Control - 1
        self.spinbox_Label= tk.Label(top, text='Number of Nodes?')
        self.spinbox_Label.grid(row=2, column=0)
        self.spinbox_Label= tk.Label(top,text='Nodes 1:')
        self.spinbox_Label.grid(row=3, column=0)
        self.No_Nodes_Scale1 = tk.Scale(top,from_=1, to=200,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale1.set(n1)
        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.changeNodes_n1)
        self.No_Nodes_Scale1.grid(row=3,column=1)

        #Link Control - 1
        self.spinbox_Label= tk.Label(top, text='Number of Links?')
        self.spinbox_Label.grid(row=2, column=2)
        self.No_Nodes_Scale1 = tk.Scale(top,from_=n1, to=(n1*(n1-1)),orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale1.set(l1)
        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.changeLinks_l1)
        self.No_Nodes_Scale1.grid(row=3,column=2)

        #Opinion Leader Control - 1
        self.spinbox_Label= tk.Label(top, text='Opinion Leader Percentage')
        self.spinbox_Label.grid(row=2, column=4)
        self.No_Nodes_Scale1 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale1.set(p1)
        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.change_p1)
        self.No_Nodes_Scale1.grid(row=3,column=4)

        ##############################################################################################################################
        #Node Control - 2
        self.spinbox_Label2= tk.Label(top, text='Number of Nodes?')
        self.spinbox_Label2.grid(row=4, column=0)
        self.spinbox_Label2= tk.Label(top,text='Nodes 2:')
        self.spinbox_Label2.grid(row=5, column=0)
        self.No_Nodes_Scale2 = tk.Scale(top,from_=1, to=200,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale2.set(n2)
        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeNodes_n2)
        self.No_Nodes_Scale2.grid(row=5,column=1)

        #Link Control - 2
        self.spinbox_Label2= tk.Label(top, text='Number of Links?')
        self.spinbox_Label2.grid(row=4, column=2)
        self.No_Nodes_Scale2 = tk.Scale(top,from_=n2, to=(n2*(n2-1)),orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale2.set(n2)
        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeLinks_l2)
        self.No_Nodes_Scale2.grid(row=5,column=2)

        #Opinion Leader Control - 2
        self.spinbox_Label2= tk.Label(top, text='Opinion Leader Percentage')
        self.spinbox_Label2.grid(row=4, column=4)
        self.No_Nodes_Scale2 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale2.set(p2)
        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.change_p2)
        self.No_Nodes_Scale2.grid(row=5,column=4)

        ##############################################################################################################################
        #Node Control - 3
        self.spinbox_Label3= tk.Label(top, text='Number of Nodes?')
        self.spinbox_Label3.grid(row=6, column=0)
        self.spinbox_Label3= tk.Label(top,text='Nodes 3:')
        self.spinbox_Label3.grid(row=7, column=0)
        self.No_Nodes_Scale3 = tk.Scale(top,from_=1, to=200,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale3.set(n3)
        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.changeNodes_n3)
        self.No_Nodes_Scale3.grid(row=7,column=1)

        #Link Control - 3
        self.spinbox_Label3= tk.Label(top, text='Number of Links?')
        self.spinbox_Label3.grid(row=6, column=2)
        self.No_Nodes_Scale3 = tk.Scale(top,from_=n2, to=(n2*(n2-1)),orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale3.set(n3)
        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.changeLinks_l3)
        self.No_Nodes_Scale3.grid(row=7,column=2)

        #Opinion Leader Control - 3
        self.spinbox_Label3= tk.Label(top, text='Opinion Leader Percentage')
        self.spinbox_Label3.grid(row=6, column=4)
        self.No_Nodes_Scale3 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale3.set(p3)
        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.change_p3)
        self.No_Nodes_Scale3.grid(row=7,column=4)

        ##############################################################################################################################
        #Node Control - 4
        self.spinbox_Label4= tk.Label(top, text='Number of Nodes?')
        self.spinbox_Label4.grid(row=8, column=0)

        self.spinbox_Label4= tk.Label(top,text='Nodes 4:')
        self.spinbox_Label4.grid(row=9, column=0)

        self.No_Nodes_Scale4 = tk.Scale(top,from_=1, to=200,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale4.set(n4)
        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.changeNodes_n4)
        self.No_Nodes_Scale4.grid(row=9,column=1)

        #Link Control - 4
        self.spinbox_Label4= tk.Label(top, text='Number of Links?')
        self.spinbox_Label4.grid(row=8, column=2)
        self.No_Nodes_Scale4 = tk.Scale(top,from_=n4, to=(n4*(n4-1)),orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale4.set(n4)
        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.changeLinks_l4)
        self.No_Nodes_Scale4.grid(row=9,column=2)

        #Opinion Leader Control - 4
        self.spinbox_Label4= tk.Label(top, text='Opinion Leader Percentage')
        self.spinbox_Label4.grid(row=8, column=4)
        self.No_Nodes_Scale4 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale4.set(p4)
        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.change_p4)
        self.No_Nodes_Scale4.grid(row=9,column=4)

        ##############################################################################################################################
        #Radius Control
        self.spinbox_Label= tk.Label(top, text='Radius of Nodes?')
        self.spinbox_Label.grid(row=10, column=0)

        self.spinbox_Label= tk.Label(top,text='Radius:')
        self.spinbox_Label.grid(row=11, column=0)

        self.No_Nodes_Scale2 = tk.Scale(top,from_=2, to=20,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale2.set(20)
        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeRadius)
        self.No_Nodes_Scale2.grid(row=11,column=1)

        ##############################################################################################################################
        #Update Button
        self.uButton = tk.Button(top,text="Update Map")
        self.uButton.bind("<ButtonRelease-1>",self.updateControl)
        self.uButton.grid(row=11,column=2)

    def updateControl(self,event):
        Network = self.variable.get()
        #print "Network: ",self.variable.get()
        self.nodes = [n1,n2,n3,n4]
        GenerateNetwork(Network,Communities,self.nodes)

    def changeCommunities(self,event):
        global Communities
        Communities = event.widget.get()
        
    ##############################################################################################################################
    def changeNodes_n1(self,event):
        global n1
        n1 = event.widget.get()

    def changeLinks_l1(self,event):
        global l1
        l1 = event.widget.get()

    def change_p1(self,event):
        global p1
        p1 = event.widget.get()

    ##############################################################################################################################    
    def changeNodes_n2(self,event):
        global n2
        n2 = event.widget.get()

    def changeLinks_l2(self,event):
        global l2
        l2 = event.widget.get()

    def change_p2(self,event):
        global p2
        p2 = event.widget.get()

    ##############################################################################################################################    
    def changeNodes_n3(self,event):
        global n3
        n3 = event.widget.get()

    def changeLinks_l3(self,event):
        global l3
        l3 = event.widget.get()

    def change_p3(self,event):
        global p3
        p3 = event.widget.get()


    ##############################################################################################################################
    def changeNodes_n4(self,event):
        global n4
        n4 = event.widget.get()

    def changeLinks_l4(self,event):
        global l4
        l4 = event.widget.get()

    def change_p4(self,event):
        global p4
        p4 = event.widget.get()

    ##############################################################################################################################
    def changeRadius(self,event):
        global Radius
        Radius = event.widget.get()


if __name__ == '__main__':
    Network()
