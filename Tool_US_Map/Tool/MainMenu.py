'''
Created on March 17, 2015
@author: sagar jha
'''


from   Tkinter import *
from   shp_reader import SHP_TYPE_POINT,SHP_TYPE_LINE,SHP_TYPE_POLYGON,Polygon
from   main_canvas import MainCanvas,GenerateNetwork
import Tkconstants
import tkFileDialog
import shp_reader
import random as rd
import dbfload as dbf
import Tkinter as tk  #For the setting

import nltk as nltk
from  textAnalysis import analysisWidget

Communities = 1
n1,n2,n3,n4 = 1,1,1,1
p1,p2,p3,p4 = 0,0,0,0
l1,l2,l3,l4 = 0,0,0,0

class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.top.title("Please Enter Your Choice")
        self.l=Label(top,text="What would you like to do today?")
        self.l.pack()
        self.l=Label(top,text="For Simulation choose Yes and to import twitter data choose No")
        self.l.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()

        self.top.grab_set_global()

    def findValue(self):
        return self.Choice.get()
        
    def cleanup(self):
        self.top.destroy()    

class Network:

    def __init__(self):

        self.root = Tk()
        self.root.state("zoomed")
        self.root.title("Network Simulator")
        self.simulatorChoice()
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

        if self.pop.options:
            self.menubar.add_cascade(label="Settings", state='disable',command = self.onClick)
        else:
            self.menubar.add_cascade(label="Analysis", state='disable',command = self.textAnalysis)
            
        self.root.config(menu=self.menubar)


    def simulatorChoice(self):
        '''
        Create popup for choice to go to Simulation or Real Twitter Data
        '''
        self.pop = popupWindow(self.root)
        self.root.wait_window(self.pop.top)

        if self.pop.findValue() == "Yes":
            self.pop.options = True
        else:
            self.pop.options = False
        

    def onClick(self):
        self.inputDialog = Settings(self.root)
        self.root.wait_window(self.inputDialog.top)

    def textAnalysis(self):
        '''
        Process the text from the twitter file and analysed using NLTK
        '''

        '''
        Preparing data from sting to text format to used it with functions from NLTK
        '''
        try:
            
            self.datalist=self.dbfdata["text"]
            self.data_list = []
            temp = []
            for i in range(len(self.datalist)):
                temp.append(self.datalist[i])
                self.data_list.append(temp)
                temp = []

            
            tw=[]
            itemp  = len(self.data_list)
            for i in range(itemp):
                temp_list = ",".join(self.data_list[i])
                tw.append(temp_list)

            wlist = []
            for item in tw:
                words = item.split(" ")
                for word in words:
                    wlist.append(word)

            text = nltk.Text(wlist)
            a = analysisWidget(self.root,text)

        except:
            print "Select file with text column for tweets..."
            


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
        self.menubar.entryconfig(3, state=Tkconstants.NORMAL)
    
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

        if self.pop.options:
            self.canvas=MainCanvas(self.shapes,self.bbox,self.shp_type,self.root,attributeName,self.datalist)

        else:            
            if (not hasattr(self, 'canvas')) or self.canvas == None:
                self.canvas=MainCanvas(self.shapes,self.bbox,self.shp_type,self.root,attributeName,self.datalist) 
            else:
                self.canvas.addLayer(self.shapes, self.shp_type, attributeName,self.datalist)
                self.canvas = None
     
    
class Settings:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.resizable(0,0)
        self.row = 0
        self.column = 0
        self.top.title('Settings')

        #Community Control
        self.spinbox_Label= tk.Label(top, text='Communities: ')
        self.spinbox_Label.grid(row=self.row, column=self.column,sticky=W+S)

        self.column = self.column + 1
        self.No_Nodes_Scale = tk.Scale(top,from_=1, to=4,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale.set(Communities)
        self.No_Nodes_Scale.bind("<ButtonRelease-1>",self.changeCommunities)
        self.No_Nodes_Scale.grid(row=self.row,column=self.column)


        ##############################################################################################################################
        #Node Control - 1
        self.row = self.row + 1
        self.column = self.column - 1
        self.spinbox_Label= tk.Label(top,text='Nodes 1: ')
        self.spinbox_Label.grid(row=self.row, column=self.column,sticky=W+S)
        self.No_Nodes_Scale1 = tk.Scale(top,from_=1, to=400,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale1.set(n1)

        self.column = self.column + 1
        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.changeNodes_n1)
        self.No_Nodes_Scale1.grid(row=self.row,column=self.column)

##        #Link Control - 1
##        self.column = self.column + 1
##        self.spinbox_Label= tk.Label(top, text='Number of Links? ')
##        self.spinbox_Label.grid(row=self.row, column=self.column,sticky=W)
##
##        self.column = self.column + 1
##        self.No_Nodes_Scale1 = tk.Scale(top,from_=n1, to=(n1*(n1-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale1.set(l1)
##        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.changeLinks_l1)
##        self.No_Nodes_Scale1.grid(row=self.row,column=self.column)
##
##        #Opinion Leader Control - 1
##        self.column = self.column + 1
##        self.spinbox_Label= tk.Label(top, text='Opinion Leader Percentage ')
##        self.spinbox_Label.grid(row=self.row, column=self.column)
##
##        self.column = self.column + 1
##        self.No_Nodes_Scale1 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale1.set(p1)
##        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.change_p1)
##        self.No_Nodes_Scale1.grid(row=self.row,column=self.column)

        ##############################################################################################################################
        #Node Control - 2
        self.row = self.row + 1
        self.column = 0
        
        self.spinbox_Label2= tk.Label(top,text='Nodes 2: ')
        self.spinbox_Label2.grid(row=self.row, column=self.column,sticky=W+S)

        self.column = self.column + 1
        self.No_Nodes_Scale2 = tk.Scale(top,from_=1, to=400,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale2.set(n2)
        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeNodes_n2)
        self.No_Nodes_Scale2.grid(row=self.row,column=self.column)

##        #Link Control - 2
##        self.column = self.column + 1
##        self.spinbox_Label2= tk.Label(top, text='Number of Links? ')
##        self.spinbox_Label2.grid(row=self.row, column=self.column)
##
##        self.column = self.column + 1
##        self.No_Nodes_Scale2 = tk.Scale(top,from_=n2, to=(n2*(n2-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale2.set(n2)
##        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeLinks_l2)
##        self.No_Nodes_Scale2.grid(row=self.row,column=self.column)
##
##        #Opinion Leader Control - 2
##        self.column = self.column + 1
##        self.spinbox_Label2= tk.Label(top, text='Opinion Leader Percentage ')
##        self.spinbox_Label2.grid(row=self.row, column=self.column)
##
##        self.column = self.column + 1
##        self.No_Nodes_Scale2 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale2.set(p2)
##        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.change_p2)
##        self.No_Nodes_Scale2.grid(row=self.row,column=self.column)
##
        ##############################################################################################################################
        #Node Control - 3
        
        self.row = self.row + 1
        self.column = 0
        self.spinbox_Label3= tk.Label(top,text='Nodes 3: ')
        self.spinbox_Label3.grid(row=self.row, column=self.column,sticky=W+S)

        self.column = self.column + 1
        self.No_Nodes_Scale3 = tk.Scale(top,from_=1, to=400,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale3.set(n3)
        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.changeNodes_n3)
        self.No_Nodes_Scale3.grid(row=self.row,column=self.column)

##        #Link Control - 3
##        self.column = self.column + 1
##        self.spinbox_Label3= tk.Label(top, text='Number of Links? ')
##        self.spinbox_Label3.grid(row=self.row, column=self.column)
##
##        self.column = self.column + 1
##        self.No_Nodes_Scale3 = tk.Scale(top,from_=n2, to=(n2*(n2-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale3.set(n3)
##        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.changeLinks_l3)
##        self.No_Nodes_Scale3.grid(row=self.row,column=self.column)
##
##        #Opinion Leader Control - 3
##        self.column = self.column + 1
##        self.spinbox_Label3= tk.Label(top, text='Opinion Leader Percentage ')
##        self.spinbox_Label3.grid(row=self.row, column=self.column)
##
##        self.column = self.column + 1
##        self.No_Nodes_Scale3 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale3.set(p3)
##        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.change_p3)
##        self.No_Nodes_Scale3.grid(row=self.row,column=self.column)

        ##############################################################################################################################
        #Node Control - 4

        self.row = self.row + 1
        self.column = 0
        self.spinbox_Label4= tk.Label(top,text='Nodes 4: ')
        self.spinbox_Label4.grid(row=self.row, column=self.column,sticky=W+S)

        self.column = self.column + 1
        self.No_Nodes_Scale4 = tk.Scale(top,from_=1, to=400,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale4.set(n4)
        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.changeNodes_n4)
        self.No_Nodes_Scale4.grid(row=self.row,column=self.column)

##        #Link Control - 4
##        self.column = self.column + 1
##        self.spinbox_Label4= tk.Label(top, text='Number of Links? ')
##        self.spinbox_Label4.grid(row=self.row, column=self.column)
##
##        self.column = self.column + 1
##        self.No_Nodes_Scale4 = tk.Scale(top,from_=n4, to=(n4*(n4-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale4.set(n4)
##        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.changeLinks_l4)
##        self.No_Nodes_Scale4.grid(row=self.row,column=self.column)
##
##        #Opinion Leader Control - 4
##
##        self.column = self.column + 1
##        self.spinbox_Label4= tk.Label(top, text='Opinion Leader Percentage ')
##        self.spinbox_Label4.grid(row=self.row, column=self.column)
##
##        self.column = self.column + 1
##        self.No_Nodes_Scale4 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale4.set(p4)
##        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.change_p4)
##        self.No_Nodes_Scale4.grid(row=self.row,column=self.column)
##
        ##############################################################################################################################
##        #Radius Control
##        self.spinbox_Label= tk.Label(top, text='Radius of Nodes? ')
##        self.spinbox_Label.grid(row=self.row, column=self.column)
##
##        self.spinbox_Label= tk.Label(top,text='Radius: ')
##        self.spinbox_Label.grid(row=self.row, column=self.column)
##
##        self.No_Nodes_Scale2 = tk.Scale(top,from_=2, to=20,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale2.set(20)
##        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeRadius)
##        self.No_Nodes_Scale2.grid(row=self.row,column=self.column)

        ##############################################################################################################################
        #Network Control
        self.row = self.row + 1
        self.column = 0
        self.spinbox_Label4= tk.Label(top,text='Network: ')
        self.spinbox_Label4.grid(row=self.row, column=self.column,sticky=W+S,pady=10)

        self.column = self.column + 1
        self.variable = StringVar(top)
        self.variable.set("GenStar")
        self.options = tk.OptionMenu(top,self.variable,"GenStar","GenRndGnm","GenForestFire","GenFull","GenCircle")
        self.options.grid(row = self.row,column=self.column,sticky=W+S,pady=10)

        ##############################################################################################################################
        #Diffusion Button
        self.row = self.row + 1
        self.column = 1
        self.ExportButton = tk.Button(top,text="Diffusion")
        self.ExportButton.bind("<ButtonRelease-1>",self.diffuse)
        self.ExportButton.grid(row=self.row,column=self.column,padx=5,rowspan=2)

        ##############################################################################################################################
        #Export Button
        self.row = self.row + 1
        self.column = 2
        self.ExportButton = tk.Button(top,text="Export")
        self.ExportButton.bind("<ButtonRelease-1>",self.exportControls)
        self.ExportButton.grid(row=self.row,column=self.column,padx=5,rowspan=2)

        #Import Button
        self.column = 3
        self.ImportButton = tk.Button(top,text="Import")
        self.ImportButton.bind("<ButtonRelease-1>",self.importControls)
        self.ImportButton.grid(row=self.row,column=self.column,padx=5,rowspan=2)

        #Update Button
        self.column = 4
        self.UpdateButton = tk.Button(top,text="Update Map")
        self.UpdateButton.bind("<ButtonRelease-1>",self.updateControls)
        self.UpdateButton.grid(row=self.row,column=self.column,padx=5,rowspan=2)

    def exportControls(self,event):
        filename = raw_input("Enter file name to save settings: ")
        if filename <> "":
            filename = filename +".txt"
            file = open(filename,"w")
            file.write("Communities:" + str(Communities)+"\n\n")
            file.write("Node 1 :" + str(n1)+"\n\n")
            file.write("Node 2 :" + str(n2)+"\n\n")
            file.write("Node 3 :" + str(n3)+"\n\n")
            file.write("Node 4 :" + str(n4)+"\n\n")
            file.write("Network:" + self.variable.get()+"\n\n")
            file.close()

        print "Settings saved in file " + filename + ".txt"

    def importControls(self,event):
        self.list = [self.No_Nodes_Scale,self.No_Nodes_Scale1,self.No_Nodes_Scale2,self.No_Nodes_Scale3,self.No_Nodes_Scale4,self.variable]
        i =0
        self.No_Nodes_Scale3.set(n3)
        directory=tkFileDialog.askopenfilename(filetypes=[("TEXT FILE","*.txt")])

        if directory <> "":                
            file = open(directory,'r')
            for line in file:
                if line <> "" and line <> "\n":
                    index = line.index(":")
                    self.list[i].set(line[index+1:].strip())
                    i = i + 1
            file.close()
        else:
            print "Please select file!!!"
        
    def updateControls(self,event):
        Network = self.variable.get().strip()
        Communities = self.No_Nodes_Scale.get()
        n1= self.No_Nodes_Scale1.get()
        n2= self.No_Nodes_Scale2.get()
        n3= self.No_Nodes_Scale3.get()
        n4= self.No_Nodes_Scale4.get()

        self.nodes = [n1,n2,n3,n4]
        self.genNetwork = GenerateNetwork(Network,Communities,self.nodes)

    def diffuse(self,event):
        self.genNetwork.diffusion()

    def changeCommunities(self,event):
        global Communities
        Communities = event.widget.get()
        
    ##############################################################################################################################
    def changeNodes_n1(self,event):
        global n1
        n1 = event.widget.get()

##    def changeLinks_l1(self,event):
##        global l1
##        l1 = event.widget.get()
##
##    def change_p1(self,event):
##        global p1
##        p1 = event.widget.get()

    ##############################################################################################################################    
    def changeNodes_n2(self,event):
        global n2
        n2 = event.widget.get()

##    def changeLinks_l2(self,event):
##        global l2
##        l2 = event.widget.get()
##
##    def change_p2(self,event):
##        global p2
##        p2 = event.widget.get()

    ##############################################################################################################################    
    def changeNodes_n3(self,event):
        global n3
        n3 = event.widget.get()

##    def changeLinks_l3(self,event):
##        global l3
##        l3 = event.widget.get()
##
##    def change_p3(self,event):
##        global p3
##        p3 = event.widget.get()


    ##############################################################################################################################
    def changeNodes_n4(self,event):
        global n4
        n4 = event.widget.get()

##    def changeLinks_l4(self,event):
##        global l4
##        l4 = event.widget.get()
##
##    def change_p4(self,event):
##        global p4
##        p4 = event.widget.get()

    ##############################################################################################################################
    def changeRadius(self,event):
        global Radius
        Radius = event.widget.get()


if __name__ == '__main__':
    Network()
