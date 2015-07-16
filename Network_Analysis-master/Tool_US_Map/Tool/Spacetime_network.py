'''
Created on March 17, 2015

@author: sagar jha
'''

#from Tkinter import Tk,Menu,Canvas,Scale

from   Tkinter import *
from   shp_reader import SHP_TYPE_POINT,SHP_TYPE_LINE,SHP_TYPE_POLYGON,Polygon
import Tkconstants
import tkFileDialog
import shp_reader
import random as rd
import dbfload as dbf

#import main_canvas as MainCanvas
from main_canvas import MainCanvas,drawNodes

import Tkinter as tk  #For the setting 

##from Community_Coordinates import CommunityCoordinates_Generator
##from diffuse.Simulator import Simulator
##import nodebox.graphics as nbg
##import nodebox_graph

##canvasWidth, canvasHeight,margin_x, margin_y  = 1800, 950, 100, 200
dict1={}

Communities = 0
n1,n2,n3,n4 = 0,0,0,0
p1,p2,p3,p4 = 0,0,0,0
l1,l2,l3,l4 = 0,0,0,0

class Network:

    def __init__(self):

        self.root = Tk()
        self.root.state("zoomed")
        self.root.title("Network Simulator")
        self.createMenu()
        self.root.mainloop()
        
        #self.root.grid()
        #self.master.rowconfigure(0,weight=1)
        #self.master.columnconfigure(0,weight=1)
        #self.canvas = Canvas(self.master,width=w-250,height=h-150,bg="grey")
        #self.canvas.grid(row=0,rowspan=1,column=0)

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
##        self.canvas = Canvas(self.root,width=canvasWidth+margin_x,height=canvasHeight+margin_y,bg="grey", scrollregion=('-50c','-50c',"50c","50c"))
##        self.canvas.grid(row=0,rowspan=1,column=0)
        self.canvas=MainCanvas(self.shapes,self.bbox,self.shp_type,self.root,attributeName,self.datalist)
##        self.__drawShape()
##
##    def __drawShape(self):
##
##        minX, minY, maxX, maxY = self.bbox[0],self.bbox[1],self.bbox[2],self.bbox[3]
##        # calculate ratios of visualization
##        ratiox = canvasWidth/(maxX-minX)
##        ratioy = canvasHeight/(maxY-minY)
##        # take the smaller ratio of window size to geographic distance
##        ratio = ratiox
##        if ratio>ratioy:
##            ratio = ratioy
##
##        if self.shp_type == SHP_TYPE_POINT:
##            self.__drawPoints(minX, minY, maxX, maxY, ratio)
##        elif self.shp_type == SHP_TYPE_LINE:
##            self.__drawPolylines(minX, minY, maxX, maxY, ratio)
##        elif self.shp_type == SHP_TYPE_POLYGON:
##            self.__drawPolygons(minX, minY, maxX, maxY, ratio)
##    
##    def __drawPoints(self,minX, minY, maxX, maxY,ratio):
##        """
##        Draw points on the canvas
##        """  
##        tag_count = 0
##        # loop through each point
##        for point in self.shapes:
##            #define an empty xylist for holding converted coordinates
##            x = int((point.x-minX)*ratio)+margin_x/2
##            y = int((maxY-point.y)*ratio)+margin_y/2
##            _point = self.canvas.create_oval(x-2, y-2, x+2, y+2,outline=point.color,  
##                               fill=point.color, width=2, tags = self.datalist[tag_count])
##            self.canvas.tag_bind( _point, '<ButtonPress-1>', self.__showAttriInfo)
##            tag_count += 1
##        
##    def __drawPolylines(self,minX, minY, maxX, maxY,ratio):
##        """
##        Draw polylines on the canvas
##        """     
##        tag_count = 0
##        # loop through each polyline
##        for polyline in self.shapes:
##            #define an empty xylist for holding converted coordinates
##            xylist = []
##            # loops through each point and calculate the window coordinates, put in xylist
##            for j in range(len(polyline.x)):
##                pointx = int((polyline.x[j]-minX)*ratio)+margin_x/2
##                pointy = int((maxY-polyline.y[j])*ratio)+margin_y/2
##                xylist.append(pointx)
##                xylist.append(pointy)
##            # loop through each part of the polyline
##            for k in range(polyline.partsNum):
##                #get the end sequence number of points in the part
##                if (k==polyline.partsNum-1):
##                    endPointIndex = len(polyline.x)
##                else:
##                    endPointIndex = polyline.partsIndex[k+1]
##                # define a temporary list for holding the part coordinates
##                tempXYlist = []
##                #take out points' coordinates for the part and add to the temporary list
##                for m in range(polyline.partsIndex[k], endPointIndex):
##                    tempXYlist.append(xylist[m*2])
##                    tempXYlist.append(xylist[m*2+1])
##                # create the line
##                _line = self.canvas.create_line(tempXYlist,fill=polyline.color, tags = self.datalist[tag_count])
##                self.canvas.tag_bind( _line, '<ButtonPress-1>', self.__showAttriInfo)            
##            tag_count += 1
##  
##    def __drawPolygons(self,minX, minY, maxX, maxY,ratio):
##        """
##        Draw polygons on the canvas
##        """      
##        tag_count = 0
##        for polygon in self.shapes:
##            #define an empty xylist for holding converted coordinates
##            xylist = []
##            
##            # loops through each point and calculate the window coordinates, put in xylist
##            for point in polygon.points:
##                pointx = int((point.x -minX)*ratio) + +margin_x/0.5
##                pointy = int((maxY- point.y)*ratio) + +margin_y/5
##                xylist.append(pointx)
##                xylist.append(pointy)
##            #print xylist
##            """
##            polyline.partsIndex is a tuple data type holding the starting points for each
##            part. For example, if the polyline.partsIndex of a polyline equals to (0, 4, 9),
##            and the total points, which is calcuate by len(polyline.points) equals to 13.
##            This means that the polyline has three parts, and the each part would have the points
##            as follows.
##            
##            part 1: p0,p1,p2,p3
##            part 2: p4,p5,p6,p7,p8
##            part 3: p9,p10,p11,p12
##            
##            The xylist would be:
##            xylist = [x0, y0, x1, y1, x2, y2, x3, y3, x4, y4....x12, y12]
##            where 
##            xylist[0] = x0
##            xylist[1] = y0
##            xylist[2] = x1
##            xylist[3] = y1
##            .....
##            
##            To draw the first part of polyline, we want to get tempXYlist as
##        
##            tempXYlist = [x0, y0, x1, y1, x2, y2, x3, y3]
##            
##            At this time, m is in range(0,4)
##            
##            xylist[m*2] would be is x0(when m=0), x1(when m=1), x2(when m=2), x3(when m=3)
##        
##            xylist[m*2+1] would be is y0(when m=0), y1(when m=1), y2(when m=2), y3(when m=3)
##            """
##            
##            for k in range(polygon.partsNum):
##                #get the end sequence number of points in the part
##                if (k==polygon.partsNum-1):
##                    endPointIndex = len(polygon.points)
##                else:
##                    endPointIndex = polygon.partsIndex[k+1]
##         
##                #Define a temporary list for holding the part coordinates
##                tempXYlist = []
##                tempXlist = []
##                tempYlist = []
##                #take out points' coordinates for the part and add to the temporary list
##                for m in range(polygon.partsIndex[k], endPointIndex):            
##                    tempXYlist.append(xylist[m*2])
##                    tempXYlist.append(xylist[m*2+1])
##                    tempXlist.append(xylist[m*2])
##                    tempYlist.append(xylist[m*2+1])
##
##                xMax = max(tempXlist)
##                xMin = min(tempXlist)
##
##                yMax = max(tempYlist)
##                yMin = min(tempYlist)
##
##                if xMax == xMin:
##                    xMin = xMax - 1
##
##                if yMax == yMin:
##                    yMin = yMax - 1
##
##                tempVar = False
##                #while not tempVar:
##                xPoint = rd.randrange(xMin,xMax)
##                yPoint = rd.randrange(yMin,yMax)
##                tempVar =  point_inside_polygon(xPoint,yPoint,tempXYlist)
##                
##                
##                startIndex = polygon.partsIndex[k] #start index for our positive polygon.                
##                tempPoints = polygon.points[startIndex: endPointIndex]#we get our temppoints to help use create our polygon using positive data
##                newPolygon = Polygon(tempPoints) #here we create our polygons using positve data
##                area = newPolygon.getArea() # Calculate the area
##                
##                #Sagar Jha center added to calculate centroid of polygon
##                center = newPolygon.getCentroid()
##                xCenter = int((center.x -minX)*ratio) + +margin_x/0.5
##                yCenter = int((maxY- center.y)*ratio) + +margin_y/5
##                
##                if area > 0:
##                    _polygon = self.canvas.create_polygon(tempXYlist,activefill="blue",fill=polygon.color,outline="blue",tags = self.datalist[tag_count])#creating our polygon outline
##                    #print k,_polygon                   
##                    
##                    if k==0:
##                        pass
##                        #_oval    = self.canvas.create_oval(xCenter, yCenter,xCenter +5,yCenter+ 5, outline="red",fill="green", width=2,tags = center)
##                        #dict1[_oval]=[center.x,center.y]
##                        #_oval1   = self.mainCanvas.create_oval(xPoint, yPoint,xPoint +5,yPoint+ 5, outline="red",fill="green", width=2)
##                else:
##                    # If it is a hole, fill with the same color as the canvas background color 
##                    _polygon = self.canvas.create_polygon(tempXYlist,fill="black",outline="black", tags = self.datalist[tag_count])
##                self.canvas.tag_bind( _polygon, '<ButtonPress-1>', self.__showAttriInfo)
##                #self.canvas.tag_bind( _oval, '<ButtonPress-1>', self.__showAttriInfo)
##            tag_count += 1   
##
##    def __showAttriInfo(self,event):
##        """
##        Show attribute information of clicked unit
##        """        
##        widget_id=event.widget.find_closest(event.x, event.y)
##        
##        if widget_id[0] in dict1.keys():
##            print widget_id[0], dict1[widget_id[0]][0],dict1[widget_id[0]][1]
##        else:
##            print "click!!!!", widget_id
##            print self.attributeName+" is: "+self.mainCanvas.gettags(widget_id)[0] 
        
        
    
class Settings:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.top.title('Settings')

        #Community Control
        self.spinbox_Label= tk.Label(top, text='Number of Community?')
        self.spinbox_Label.grid(row=0, column=0)

        self.spinbox_Label= tk.Label(top,text='Community:')
        self.spinbox_Label.grid(row=1, column=0)

        self.No_Nodes_Scale = tk.Scale(top,from_=0, to=4,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale.set(Communities)
        self.No_Nodes_Scale.bind("<ButtonRelease-1>",self.changeCommunities)
        self.No_Nodes_Scale.grid(row=1,column=1)

        ##############################################################################################################################
        #Network Control
        self.variable = StringVar(top)
        self.variable.set("A")
        self.options = tk.OptionMenu(top,self.variable,"A","B","C")
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
        print "Communities: ",Communities
        print "n1: ",n1
        print "n2: ",n2
        print "n3: ",n3
        print "n4: ",n4
        print "Network: ",self.variable.get()
        a = drawNodes()

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

def point_inside_polygon(x,y,poly):
    n = len(poly)/2
    inside =False

    p1x = poly[0]
    p1y = poly[1]
    
    for i in range(0,n+1,1):
        p2x = poly [(i%n)*2]
        p2y = poly [(i%n)*2 +1]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

 
##root=Tk()
###root.minsize=(1000,900)
###root.attributes('-fullscreen',True)  #It will hide the title bar but open in maximized mode
##w,h = root.winfo_screenwidth(),root.winfo_screenheight()  #It gives screen widht and height
##
##root.state('zoomed')
##root.geometry=("1000x900+0+0")
##
##NG=Network(root)
##root.mainloop()


if __name__ == '__main__':
    Network()
