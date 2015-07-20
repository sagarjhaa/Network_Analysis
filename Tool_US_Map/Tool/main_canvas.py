"""
the canvas to draw the shapefile and interaction with mouse clicks
"""
from Tkinter import *
#from Tkinter import Toplevel, Canvas
from shp_reader import SHP_TYPE_POINT,SHP_TYPE_LINE,SHP_TYPE_POLYGON,Polygon

import random as rd
import snap
from sag1 import point_inside_polygon
from PolygonParts import PolygonPart
from Node import Node

# display parameters
canvasWidth, canvasHeight,margin_x, margin_y  = 1800, 950, 100, 100

Gcanvas = ""
GCoordinate = ""
GNodesItemNo = []

class MainCanvas(object):
    """
    The shapefile displaying device based on TKinter Canvas

    Attributes
    ----------

    shapes           : array
                      The spatial units
    bbox             : array
                      The bounding box: minX, minY, maxX, maxY
    shp_type         : integer
                      The shape types: SHP_TYPE_POINT,SHP_TYPE_LINE,SHP_TYPE_POLYGON
    root             : Tk
                      The Tk Object
    attributeName    : string
                      The attribute name
    datalist         : array
                      The attribute data
                      
    """
    def __init__(self,shapes,bbox,shp_type,root,attributeName,datalist):
        self.shapes = shapes
        self.bbox = bbox
        self.shp_type = shp_type
        self.root = root
        self.attributeName = attributeName
        self.datalist = datalist
        self.OvalNo={}
        self.CoordinateCollect=[]

        self.__createCanvas()
        

##        for i in range(len(self.CoordinateCollect)):
##            for j in range(len(self.CoordinateCollect[i].parts)):
##                print self.CoordinateCollect[i].id,len(self.CoordinateCollect[i].parts),j#self.CoordinateCollect[i].parts[j]
         
    def __createCanvas(self):
        """
        Create the canvas and draw all the spatial objects
        """
        
        global Gcanvas,GCoordinate
        self.canvasRoot = self.root#Toplevel()#
        self.canvasRoot.title(self.attributeName)
        self.canvasRoot.lower(belowThis = self.root)


        
        if Gcanvas == "":
            self.mainCanvas = Canvas(self.canvasRoot, bg = 'black', width = canvasWidth+margin_x, height = canvasHeight+margin_y, scrollregion=('0c','0c',"150c","150c"))
            Gcanvas = self.mainCanvas

            #Scrollbar
            hbar=Scrollbar(self.mainCanvas,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command=self.mainCanvas.xview)
            vbar=Scrollbar(self.mainCanvas,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command=self.mainCanvas.yview)

            self.mainCanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.mainCanvas.pack(side=LEFT,expand=True,fill=BOTH)

        else:
            self.mainCanvas = Gcanvas
            self.mainCanvas.delete(ALL)
        
        self.__drawShape()
        GCoordinate = self.CoordinateCollect
        self.mainCanvas.pack()
        
    def __drawShape(self):
        """ 
        Draw all the spatial objects on the canvas
        """
        minX, minY, maxX, maxY = self.bbox[0],self.bbox[1],self.bbox[2],self.bbox[3]
        # calculate ratios of visualization
        ratiox = canvasWidth/(maxX-minX)
        ratioy = canvasHeight/(maxY-minY)
        # take the smaller ratio of window size to geographic distance
        ratio = ratiox
        if ratio>ratioy:
            ratio = ratioy
        
        if self.shp_type == SHP_TYPE_POINT:
            self.__drawPoints(minX, minY, maxX, maxY, ratio)
        elif self.shp_type == SHP_TYPE_LINE:
            self.__drawPolylines(minX, minY, maxX, maxY, ratio)
        elif self.shp_type == SHP_TYPE_POLYGON:
            self.__drawPolygons(minX, minY, maxX, maxY, ratio)
      
    def __drawPoints(self,minX, minY, maxX, maxY,ratio):
        """
        Draw points on the canvas
        """  
        tag_count = 0
        # loop through each point
        for point in self.shapes:
            #define an empty xylist for holding converted coordinates
            x = int((point.x-minX)*ratio)+margin_x/2
            y = int((maxY-point.y)*ratio)+margin_y/2
            _point = self.mainCanvas.create_oval(x-2, y-2, x+2, y+2,outline=point.color,  
                               fill=point.color, width=2, tags = self.datalist[tag_count])
            self.mainCanvas.tag_bind( _point, '<ButtonPress-1>', self.__showAttriInfo)
            tag_count += 1
        
    def __drawPolylines(self,minX, minY, maxX, maxY,ratio):
        """
        Draw polylines on the canvas
        """     
        tag_count = 0
        # loop through each polyline
        for polyline in self.shapes:
            #define an empty xylist for holding converted coordinates
            xylist = []
            # loops through each point and calculate the window coordinates, put in xylist
            for j in range(len(polyline.x)):
                pointx = int((polyline.x[j]-minX)*ratio)+margin_x/2
                pointy = int((maxY-polyline.y[j])*ratio)+margin_y/2
                xylist.append(pointx)
                xylist.append(pointy)
            # loop through each part of the polyline
            for k in range(polyline.partsNum):
                #get the end sequence number of points in the part
                if (k==polyline.partsNum-1):
                    endPointIndex = len(polyline.x)
                else:
                    endPointIndex = polyline.partsIndex[k+1]
                # define a temporary list for holding the part coordinates
                tempXYlist = []
                #take out points' coordinates for the part and add to the temporary list
                for m in range(polyline.partsIndex[k], endPointIndex):
                    tempXYlist.append(xylist[m*2])
                    tempXYlist.append(xylist[m*2+1])
                # create the line
                _line = self.mainCanvas.create_line(tempXYlist,fill=polyline.color, tags = self.datalist[tag_count])
                self.mainCanvas.tag_bind( _line, '<ButtonPress-1>', self.__showAttriInfo)            
            tag_count += 1
  
    def __drawPolygons(self,minX, minY, maxX, maxY,ratio):
        """
        Draw polygons on the canvas
        """
        itemId = 1
        tag_count = 0
        for polygon in self.shapes:
            #define an empty xylist for holding converted coordinates
            xylist = []

            self.PolyInfo = PolygonPart(itemId)
            itemId = itemId + 1
            
            # loops through each point and calculate the window coordinates, put in xylist
            for point in polygon.points:
                
                pointx = int((point.x -minX)*ratio) + +margin_x/0.5
                pointy = int((maxY- point.y)*ratio) + +margin_y/5
                xylist.append(pointx)
                xylist.append(pointy)
            #print xylist
            """
            polyline.partsIndex is a tuple data type holding the starting points for each
            part. For example, if the polyline.partsIndex of a polyline equals to (0, 4, 9),
            and the total points, which is calcuate by len(polyline.points) equals to 13.
            This means that the polyline has three parts, and the each part would have the points
            as follows.
            
            part 1: p0,p1,p2,p3
            part 2: p4,p5,p6,p7,p8
            part 3: p9,p10,p11,p12
            
            The xylist would be:
            xylist = [x0, y0, x1, y1, x2, y2, x3, y3, x4, y4....x12, y12]
            where 
            xylist[0] = x0
            xylist[1] = y0
            xylist[2] = x1
            xylist[3] = y1
            .....
            
            To draw the first part of polyline, we want to get tempXYlist as
        
            tempXYlist = [x0, y0, x1, y1, x2, y2, x3, y3]
            
            At this time, m is in range(0,4)
            
            xylist[m*2] would be is x0(when m=0), x1(when m=1), x2(when m=2), x3(when m=3)
        
            xylist[m*2+1] would be is y0(when m=0), y1(when m=1), y2(when m=2), y3(when m=3)
            """
            
            for k in range(polygon.partsNum):
                
                #get the end sequence number of points in the part
                if (k==polygon.partsNum-1):
                    endPointIndex = len(polygon.points)
                else:
                    endPointIndex = polygon.partsIndex[k+1]
         
                #Define a temporary list for holding the part coordinates
                tempXYlist = []
                tempXlist  = []
                tempYlist  = []
                #take out points' coordinates for the part and add to the temporary list
                for m in range(polygon.partsIndex[k], endPointIndex):            
                    tempXYlist.append(xylist[m*2])
                    tempXYlist.append(xylist[m*2+1])
                    tempXlist.append(xylist[m*2])
                    tempYlist.append(xylist[m*2+1])

                self.PolyInfo.parts[k]=tempXYlist
                
                xMax = max(tempXlist)
                xMin = min(tempXlist)

                yMax = max(tempYlist)
                yMin = min(tempYlist)

                if xMax == xMin:
                    xMin = xMax - 1

                if yMax == yMin:
                    yMin = yMax - 1

                tempVar = False
                #while not tempVar:
                xPoint = rd.randrange(xMin,xMax)
                yPoint = rd.randrange(yMin,yMax)
                tempVar =  point_inside_polygon(xPoint,yPoint,tempXYlist)
                
                
                startIndex = polygon.partsIndex[k] #start index for our positive polygon.                
                tempPoints = polygon.points[startIndex: endPointIndex]#we get our temppoints to help use create our polygon using positive data
                newPolygon = Polygon(tempPoints) #here we create our polygons using positve data
                area = newPolygon.getArea() # Calculate the area
                
                #Sagar Jha center added to calculate centroid of polygon
                center = newPolygon.getCentroid()
                xCenter = int((center.x -minX)*ratio) + +margin_x/0.5
                yCenter = int((maxY- center.y)*ratio) + +margin_y/5
                
                if area > 0:
                    _polygon = self.mainCanvas.create_polygon(tempXYlist,activefill="blue",fill=polygon.color,outline="blue",tags = self.datalist[tag_count])#creating our polygon outline
                    
##                    if k==0:
##                        _oval    = self.mainCanvas.create_oval(xCenter, yCenter,xCenter +5,yCenter+ 5, outline="red",fill="green", width=2,tags = center)
##                        self.OvalNo[_oval]=[center.x,center.y]

                else:
                    # If it is a hole, fill with the same color as the canvas background color 
                    _polygon = self.mainCanvas.create_polygon(tempXYlist,fill="black",outline="black", tags = self.datalist[tag_count])
                self.mainCanvas.tag_bind( _polygon, '<ButtonPress-1>', self.__showAttriInfo)
##                self.mainCanvas.tag_bind( _oval, '<ButtonPress-1>', self.__showAttriInfo)
            self.CoordinateCollect.append(self.PolyInfo)
            tag_count += 1
            
    def __showAttriInfo(self,event):
        """
        Show attribute information of clicked unit
        """        
        widget_id=event.widget.find_closest(event.x, event.y)
        
        if widget_id[0] in self.OvalNo.keys():
            print widget_id[0], self.OvalNo[widget_id[0]][0],self.OvalNo[widget_id[0]][1]
        else:
            print "click!!!!", widget_id
            print self.attributeName+" is: "+self.mainCanvas.gettags(widget_id)[0]

class GenerateNetwork(object):

    def __init__(self,Network,Communities,nodes):

        global Gcanvas,GCoordinate,GNodesItemNo
        self.Communities = Communities
        self.canvas = Gcanvas
        self.Network = Network
        self.nodes = nodes
        self.dnodes = nodes
        self.nPoints = 0
        
        for i in range(self.Communities):
            self.nPoints = self.nPoints + self.nodes[i]

##        self.n1,self.n2,self.n3,self.n4 = self.nodes[0],self.nodes[1],self.nodes[2],self.nodes[3]
        

        if len(GNodesItemNo) <> 0 :
            for iCount in GNodesItemNo:
                Gcanvas.delete(iCount)

        self.itemNo = []
        self.pAll = []
        self.drawNode()

    def drawNode(self):

        global GNodesItemNo

        if self.Network == "GenStar":
            print "GenStar is the network with points ",self.nPoints
            Graph = snap.GenStar(snap.PNGraph, self.nPoints, True)

        if self.Network == "GenRndGnm":
            print "GenRndGnm is the netowork with points ",self.nPoints
            Graph = snap.GenRndGnm(snap.PNGraph,self.nPoints, self.nPoints)

        if self.Network == "GenForestFire":
            print "GenForestFire is the netowork with points ",self.nPoints
            Graph = snap.GenForestFire(self.nPoints, 0.5,0.5)

        shape = 0
        self.dnodes.reverse()
        nodeCounter = self.dnodes.pop()
        
        for i in Graph.Nodes():
            self.node = Node()
            self.node.id = i.GetId()
            
            for EI in Graph.Edges():
                if EI.GetSrcNId() == i.GetId():
                        if EI.GetSrcNId() <> EI.GetDstNId() :
                            self.node.follower.append(EI.GetDstNId())
            if shape ==0:
                self.node.shape = "oval"
            if shape ==1:
                self.node.shape = "square"
            if shape ==2:
                self.node.shape = "rectangle"
            if shape ==3:
                self.node.shape = "circle"

            nodeCounter = nodeCounter - 1
            if nodeCounter <=0:
                if len(self.dnodes)<> 0:
                    nodeCounter = self.dnodes.pop()
                shape = shape + 1
            
            self.CoordinateSelection()

            if self.node.shape == "oval":
                _Oval = Gcanvas.create_oval(self.node.x,self.node.y,self.node.x+5,self.node.y+5,outline="green",fill="green", width=2)

            if self.node.shape == "square":
                _Oval = Gcanvas.create_oval(self.node.x,self.node.y,self.node.x+5,self.node.y+5,outline="red",fill="red", width=2)

            if self.node.shape == "rectangle":
                _Oval = Gcanvas.create_oval(self.node.x,self.node.y,self.node.x+5,self.node.y+5,outline="yellow",fill="yellow", width=2)

            if self.node.shape == "circle":
                _Oval = Gcanvas.create_oval(self.node.x,self.node.y,self.node.x+5,self.node.y+5,outline="white",fill="white", width=2)

            self.itemNo.append(_Oval)
            self.pAll.append(self.node)

            
        GNodesItemNo = self.itemNo
            
    def CoordinateSelection(self):
        PolyPart = rd.randrange(len(GCoordinate))
        #print len(GCoordinate[PolyPart].parts)
        SubPolyPart = rd.randrange(len(GCoordinate[PolyPart].parts))
        #print "PolyPart: ",PolyPart," SubPolyPart ",SubPolyPart
        #print "Coordinate: ",GCoordinate[PolyPart].parts[SubPolyPart]
        tempXYlist = GCoordinate[PolyPart].parts[SubPolyPart]

        tempXlist = []
        tempYlist = []

                        
        for i in range(0,len(tempXYlist),2):
            tempXlist.append(tempXYlist[i])
            tempYlist.append(tempXYlist[i+1])
        
        xMax = max(tempXlist)
        xMin = min(tempXlist)

        yMax = max(tempYlist)
        yMin = min(tempYlist)

        if xMax == xMin:
            xMin = xMax - 1

        if yMax == yMin:
            yMin = yMax - 1

        tempVar = False
        i = 0
        while not tempVar:
            xPoint = rd.randrange(xMin,xMax)
            yPoint = rd.randrange(yMin,yMax)
            tempVar =  point_inside_polygon(xPoint,yPoint,tempXYlist)
            i = i+1
            if i >25:
##                print xMin,xMax,yMin,yMax
                break
            
        self.node.x = xPoint
        self.node.y = yPoint
        








        
        
    
        
        