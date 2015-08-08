"""
the canvas to draw the shapefile and interaction with mouse clicks
"""
from Tkinter import *
from shp_reader import SHP_TYPE_POINT,SHP_TYPE_LINE,SHP_TYPE_POLYGON,Polygon

import random as rd
import snap
from PolygonParts import PolygonPart
from Node import Node
import time

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

    def addLayer(self,shapes,shp_type,attributeName,datalist):
        self.shapes = shapes
        self.shp_type = shp_type
        self.attributeName = attributeName
        self.datalist = datalist
        
        self.__drawShape(shapes,datalist, self.bbox,shp_type)

        
    def __createCanvas(self):
        """
        Create the canvas and draw all the spatial objects
        """
        
        global Gcanvas,GCoordinate
        self.canvasRoot =self.root# Toplevel()#
        self.canvasRoot.title(self.attributeName)
        self.canvasRoot.lower(belowThis = self.root)
        
        if Gcanvas == "":
            self.mainCanvas = Canvas(self.canvasRoot, bg = '#eff7ef', width = int(canvasWidth+margin_x), height = int(canvasHeight+margin_y), scrollregion=('0c','0c',"150c","150c"))
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
        
        self.__drawShape(self.shapes,self.datalist,self.bbox,self.shp_type)
        GCoordinate = self.CoordinateCollect
        self.mainCanvas.pack()
        
    def __drawShape(self,shapes,datalist,bbox,shp_type):
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
        
        if shp_type == SHP_TYPE_POINT:
            self.__drawPoints(minX, minY, maxX, maxY, ratio)
        elif shp_type == SHP_TYPE_LINE:
            self.__drawPolylines(minX, minY, maxX, maxY, ratio)
        elif shp_type == SHP_TYPE_POLYGON:
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
            _point = self.mainCanvas.create_oval(x-5, y-5, x+5, y+5,outline=point.outline,  
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
                pointx = int((point.x -minX)*ratio) + +margin_x/2
                pointy = int((maxY- point.y)*ratio) + +margin_y/2
                
                xylist.append(pointx)
                xylist.append(pointy)
    
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
                
                
                startIndex = polygon.partsIndex[k] #start index for our positive polygon.                
                tempPoints = polygon.points[startIndex: endPointIndex]#we get our temppoints to help use create our polygon using positive data
                newPolygon = Polygon(tempPoints) #here we create our polygons using positve data
                area = newPolygon.getArea() # Calculate the area
                
                
                if area > 0:
                    #color = rd.choice(["#e2baba","#be6565","#deb2b2"])#(["#acdcd1","#86aba3","#607a74"])
                    color = "#66b266"
                    _polygon = self.mainCanvas.create_polygon(tempXYlist,activefill="#9999ff",fill=color,outline="white",tags = self.datalist[tag_count])#creating our polygon outline
                    
                else:
                    # If it is a hole, fill with the same color as the canvas background color 
                    _polygon = self.mainCanvas.create_polygon(tempXYlist,fill="white",outline="white", tags = self.datalist[tag_count])
                self.mainCanvas.tag_bind( _polygon, '<ButtonPress-1>', self.__showAttriInfo)
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
        self.Hidden = False
        self.nPoints = 0
        self.OvalNo ={}
        self.LineNo = []
        self.itemNo = []
        self.pAll = []
        
        for i in range(self.Communities):
            self.nPoints = self.nPoints + self.nodes[i]

        if len(GNodesItemNo) <> 0 :
            for iCount in GNodesItemNo:
                Gcanvas.delete(iCount)

        #Check 1 if no shape file is selected
        if Gcanvas == "":
            print "Please select a shape file!!!"
        else:
            self.drawNode()
            #self.diffusion()

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
                self.node.shape = "triangle"
            if shape ==2:
                self.node.shape = "rectangle"
            if shape ==3:
                self.node.shape = "circle"

            nodeCounter = nodeCounter - 1
            if nodeCounter <=0:
                if len(self.dnodes)<> 0:
                    nodeCounter = self.dnodes.pop()
                    print "Completed Community: ",shape
                shape = shape + 1
            
            self.CoordinateSelection()
            self.Radius = 5
##            if len(self.node.follower) <> 0:
##                self.Radius = len(self.node.follower)
                
            if self.node.shape == "oval":
                _Oval = Gcanvas.create_oval(self.node.x,self.node.y,self.node.x+self.Radius,
                                            self.node.y+self.Radius,outline="#ff00ff",fill="white", width=2)

            if self.node.shape == "triangle":
                traingle = [self.node.x,self.node.y,self.node.x+self.Radius,self.node.y+self.Radius]
                _Oval = Gcanvas.create_oval(traingle,outline="#252568",fill="white", width=2)

            if self.node.shape == "rectangle":
                _Oval = Gcanvas.create_oval(self.node.x,self.node.y,self.node.x+self.Radius,
                                            self.node.y+self.Radius,outline="#474bcc",fill="white", width=2)

            if self.node.shape == "circle":
                _Oval = Gcanvas.create_oval(self.node.x,self.node.y,self.node.x+self.Radius,
                                            self.node.y+self.Radius,outline="#364949",fill="white", width=2)

            self.OvalNo[_Oval]=self.node.id#[self.node.x,self.node.y]
            Gcanvas.tag_bind( _Oval, '<ButtonPress-1>', self.__showAttriInfo)
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
            tempVar =  self.point_inside_polygon(xPoint,yPoint,tempXYlist)
            i = i+1
            if i >25:
##                print xMin,xMax,yMin,yMax
                break
            
        self.node.x = xPoint
        self.node.y = yPoint

    def point_inside_polygon(self,x,y,poly):
        
        n = len(poly)/2
        inside =False

        p1x = poly[0]
        p1y = poly[1]
        #print p1x,p1y
        for i in range(0,n+1,1):
            p2x = poly [(i%n)*2]
            p2y = poly [(i%n)*2 +1]
    ##        p2x,p2y = poly[i % n]
    ##        print i,i%n,p2x,p2y
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def diffusion(self):

##        Print all the nodes with the followers
##        for i in range(len(self.pAll)):
##            print self.pAll[i].id,self.pAll[i].x,self.pAll[i].y #" Follower ",self.pAll[i].follower

        completed_nodes = []
        uncomplete_nodes = []
        widgetList = []

        maxFollowers = [len(i.follower) for i in self.pAll]
##        print maxFollowers
        
        initialNode  = self.pAll[maxFollowers.index(max(maxFollowers))]#rd.choice(self.pAll)
        completed_nodes.append(initialNode.id)
        
        widgetId = self.OvalNo.keys()[self.OvalNo.values().index(initialNode.id)]
        newwidth = 10
        Gcanvas.itemconfig(widgetId,outline="orange",width = newwidth)
        
        for i in range(len(initialNode.follower)):
            destNode = self.pAll[initialNode.follower[i]]

            widgetId = self.OvalNo.keys()[self.OvalNo.values().index(destNode.id)]
            Gcanvas.itemconfig(widgetId,width = newwidth,outline = "red")
            
            #_line=Gcanvas.create_line(initialNode.x,initialNode.y,destNode.x,destNode.y,arrow="last",fill="black",width=3)

            uncomplete_nodes.append(initialNode.follower[i])
            #self.itemNo.append(_line)
            
            
        #colors = ["black","grey","yellow","#f6c99a","#efc818","#c3fd53","#66cccc","#883eba","#aed3e1","#dbcbdb"]
        while len(uncomplete_nodes) <> 0:

            initialNode = self.pAll[uncomplete_nodes[0]]
            color = "black"
            #print uncomplete_nodes[0] , " Follower ",self.pAll[uncomplete_nodes[0]].follower
            uncompleted_follower = self.pAll[uncomplete_nodes[0]].follower
            for itemp in uncompleted_follower:
                if itemp not in completed_nodes:

                    destNode = self.pAll[itemp]
                    
                    widgetId = self.OvalNo.keys()[self.OvalNo.values().index(itemp)]
                    newwidth = newwidth -0.5
                    Gcanvas.itemconfig(widgetId,width = newwidth,outline = color)
                    uncomplete_nodes.append(itemp)

                   # _line=Gcanvas.create_line(initialNode.x,initialNode.y,destNode.x,destNode.y,arrow="last",fill="black",width=1)
                   # self.itemNo.append(_line)
                    
            
            completed_nodes.append(uncomplete_nodes[0])
            del uncomplete_nodes[0]

    def __showAttriInfo(self,event):
        """
        Show attribute information of clicked unit
        """        
        widget_id=event.widget.find_closest(event.x, event.y)

        try:
            NodeId = self.OvalNo[widget_id[0]]

            if len(self.LineNo) <> 0:
                for i in self.LineNo:
                    Gcanvas.delete(i)

            if self.Hidden:
                for i in range(len(self.pAll)):
                    widgetId = self.OvalNo.keys()[self.OvalNo.values().index(self.pAll[i].id)]
                    Gcanvas.itemconfig(widgetId,state="normal")
                    self.Hidden = False
            else:
                for i in range(len(self.pAll)):
                    widgetId = self.OvalNo.keys()[self.OvalNo.values().index(self.pAll[i].id)]
                    Gcanvas.itemconfig(widgetId,state="hidden")
                self.Hidden = True
                
            for i in range(len(self.pAll)):
                
                if self.pAll[i].id == NodeId:
                    #print "NodeId: ",NodeId," ---->",self.pAll[i].follower
                    Node1 = self.pAll[i]

                    widgetId = self.OvalNo.keys()[self.OvalNo.values().index(self.pAll[i].id)]
                    Gcanvas.itemconfig(widgetId,state="normal")
                    
                    for j in self.pAll[i].follower:
                        Node2 = self.pAll[j]
                        
                        widgetId = self.OvalNo.keys()[self.OvalNo.values().index(self.pAll[j].id)]
                        Gcanvas.itemconfig(widgetId,state="normal")
                        
                        _line=Gcanvas.create_line(Node1.x+5,Node1.y+5,Node2.x+5,Node2.y+5,arrow="last",fill="black",width=3)
                        self.itemNo.append(_line)
                        self.LineNo.append(_line)
                    GNodesItemNo = self.itemNo
                    break
        except:
            print "Please click again on the oval"

