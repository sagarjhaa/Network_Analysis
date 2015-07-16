"""
the canvas to draw the shapefile and interaction with mouse clicks
"""
from Tkinter import *
#from Tkinter import Toplevel, Canvas
from shp_reader import SHP_TYPE_POINT,SHP_TYPE_LINE,SHP_TYPE_POLYGON,Polygon

import random as rd
from sag1 import point_inside_polygon

# display parameters
canvasWidth, canvasHeight,margin_x, margin_y  = 1800, 950, 100, 200
dict1 = {}

Gcanvas = ""

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

        self.__createCanvas()
         
    def __createCanvas(self):
        """
        Create the canvas and draw all the spatial objects
        """
        global Gcanvas
        
        self.canvasRoot = self.root#Toplevel()#
        self.canvasRoot.title(self.attributeName)
        self.canvasRoot.lower(belowThis = self.root)
        if Gcanvas == "":
            self.mainCanvas = Canvas(self.canvasRoot, bg = 'black', width = canvasWidth+margin_x, height = canvasHeight+margin_y, scrollregion=('-50c','-50c',"50c","50c"))
            Gcanvas = self.mainCanvas
        else:
            self.mainCanvas = Gcanvas
            self.mainCanvas.delete(ALL)
        
        self.__drawShape()
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
        tag_count = 0
        for polygon in self.shapes:
            #define an empty xylist for holding converted coordinates
            xylist = []
            
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
                tempXlist = []
                tempYlist = []
                #take out points' coordinates for the part and add to the temporary list
                for m in range(polygon.partsIndex[k], endPointIndex):            
                    tempXYlist.append(xylist[m*2])
                    tempXYlist.append(xylist[m*2+1])
                    tempXlist.append(xylist[m*2])
                    tempYlist.append(xylist[m*2+1])

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
                    
                    if k==0:
                        _oval    = self.mainCanvas.create_oval(xCenter, yCenter,xCenter +5,yCenter+ 5, outline="red",fill="green", width=2,tags = center)
                        dict1[_oval]=[center.x,center.y]
                        #_oval1   = self.mainCanvas.create_oval(xPoint, yPoint,xPoint +5,yPoint+ 5, outline="red",fill="green", width=2)
                else:
                    # If it is a hole, fill with the same color as the canvas background color 
                    _polygon = self.mainCanvas.create_polygon(tempXYlist,fill="black",outline="black", tags = self.datalist[tag_count])
                self.mainCanvas.tag_bind( _polygon, '<ButtonPress-1>', self.__showAttriInfo)
                self.mainCanvas.tag_bind( _oval, '<ButtonPress-1>', self.__showAttriInfo)
            tag_count += 1
            
    def __showAttriInfo(self,event):
        """
        Show attribute information of clicked unit
        """        
        widget_id=event.widget.find_closest(event.x, event.y)
        
        if widget_id[0] in dict1.keys():
            print widget_id[0], dict1[widget_id[0]][0],dict1[widget_id[0]][1]
        else:
            print "click!!!!", widget_id
            print self.attributeName+" is: "+self.mainCanvas.gettags(widget_id)[0]

class drawNodes(object):

    def __init__(self):

        global Gcanvas
        self.canvas = Gcanvas
        self.drawNode1()

    def drawNode1(self):
        #_point = self.canvas.create_oval(370,113,400,143,outline="red",fill="green", width=4)
        _point = self.canvas.create_oval(100,200,400,600,outline="red",fill="green", width=4)
        #self.canvas.pack()
        
    
        
        
