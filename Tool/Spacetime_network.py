'''
Created on March 17, 2015

@author: sagar jha
'''

from Tkinter import *
import Tkinter as tk
import random as rd
import copy

from Community_Coordinates import CommunityCoordinates_Generator
from diffuse.Simulator import Simulator

import nodebox.graphics as nbg
import nodebox_graph

#Initilization
'''
    communities is the total number of communities displayed on the screen.
    n1,n2,n3,n4 are the nodes in the respective communities.
    l1,l2,l3,l4 are the links in the respective communities.
    p1,p2,p3,p4 are the initlial percentage for opnion leader of all communities.
'''
Communities = 4
n1 = 7    
n2 = 5
n3 = 5
n4 = 5

l1 = 7
l2 = 5
l3 = 5
l4 = 5

p1 = 40
p2 = 40
p3 = 40
p4 = 40

# Radius is the initial radius of the nodes.
Radius = 10

Widget_to_Node = {}

class Network:

    def __init__(self,master=None):

        self.master = master
        self.master.title("Network Simulator")
        self.master.grid()
        self.master.rowconfigure(0,weight=1)
        self.master.columnconfigure(0,weight=1)
        self.canvas = Canvas(self.master,width=w-250,height=h-150,bg="grey")
        self.canvas.grid(row=0,rowspan=1,column=0)

        #Community_Coordinate dictionary to store the coordinates of all communities.
        self.Community_Coordinate = {}
        #Communities is the variable to store the number of communities.
        self.Communities = Communities
        #Function CommmunityCoordinates_Generator generate the coordinate for the given number of communities.
        self.Community_Coordinate = CommunityCoordinates_Generator(self.Communities,w,h)

        #Radius and Half_Radius of the nodes.
        self.Radius = Radius
        self.Half_Radius = Radius/2

        '''

        Looping throught all the communities
        Drawing the communities(polygon)
        Generating the points
        Generating links for the random network
        Drawing elements (Nodes and Links)to the communities
        
        '''
        
        for i in range(1,self.Communities+1):
            _polygon = self.canvas.create_polygon(self.Community_Coordinate[i][0],outline='red',width=2)
            
            if i == 1:
                self.n1 = n1
                self.l1 = l1
                self.p1 = p1
                
                self.canvas.itemconfig(_polygon,fill="#fff")
                self.s1 = Simulator(self.n1)
                self.s1.genPoints(self.Community_Coordinate[1])           
                self.s1.genLinks(self.l1)
                
                for sag in range(len(self.s1.pAll)):
                    print self.s1.pAll[sag].id,self.s1.pAll[sag].follower
                    
                self.__drawElements(self.s1,self.n1,self.p1,i)
                                
            if i ==2:
                '''
                Generating same node as community 1
                Drawing a Star Network.
                '''
                self.s2 = Simulator(self.n1)
                self.s2.genPoints_GenStar(self.Community_Coordinate[i])
                
                self.n2 = copy.deepcopy(self.n1)
                self.l2 = copy.deepcopy(self.l1)
                self.p2 = copy.deepcopy(self.p1)

                self.canvas.itemconfig(_polygon,fill="#fff")
##                self.s2 = Simulator(self.n2)
##                self.s2.genPoints(self.Community_Coordinate[i])           
##                self.s2.genLinks(l2)
                self.__drawElements(self.s2,self.n2,self.p2,i)

            if i ==3:
                '''
                GenRndGnm Network
                '''
                self.s3 = Simulator(self.n1)
                self.s3.genPoints_GenRndGnm(self.Community_Coordinate[i])

                self.n3 = copy.deepcopy(self.n1)
                self.l3 = copy.deepcopy(self.l1)
                self.p3 = copy.deepcopy(self.p1)
                
                self.canvas.itemconfig(_polygon,fill="#fff")
##                self.s3 = Simulator(self.n3)
##                self.s3.genPoints(self.Community_Coordinate[i])           
##                self.s3.genLinks(l3)
                self.__drawElements(self.s3,self.n3,self.p3,i)

                    
            if i ==4:
                '''
                GenForestFire Network
                '''
                self.s4 = Simulator(self.n1)
                self.s4.genPoints_GenForestFire(self.Community_Coordinate[i])
                
                self.n4 = copy.deepcopy(self.n1)
                self.l4 = copy.deepcopy(self.l1)
                self.p4 = copy.deepcopy(self.p1)
                
                self.canvas.itemconfig(_polygon,fill="#fff")
##                self.s4 = Simulator(self.n4)
##                self.s4.genPoints(self.Community_Coordinate[i])           
##                self.s4.genLinks(l4)
                self.__drawElements(self.s4,self.n4,self.p4,i)

    def __drawElements(self,s,n,p,i):

        '''
        __drawElements is the function to draw the nodes and links on the canvas.
        It takes the Nodes,Links and the Porbablities.
        '''

        self.s = s
        self.n = n
        self.p = p

        self.width = w - 250
        self.hwidth = self.width/2

        self.height = h - 150
        self.hheight = self.height /2
        
        '''
        If block to change the coordinate of nodes in communities 2,3,and 4 according to 1
        '''
        
        if i == 2:
            for jNode in range(len(self.s.pAll)):
                self.s.pAll[jNode].color = self.s1.pAll[jNode].color
                self.s.pAll[jNode].x = self.s1.pAll[jNode].x +  self.hwidth + 10
                self.s.pAll[jNode].y = self.s1.pAll[jNode].y 

        if i == 3:
            for jNode in range(len(self.s.pAll)):
                self.s.pAll[jNode].color = self.s1.pAll[jNode].color
                self.s.pAll[jNode].x = self.s1.pAll[jNode].x
                self.s.pAll[jNode].y = self.s1.pAll[jNode].y +  self.hheight + 10

        if i == 4:
            for jNode in range(len(self.s.pAll)):
                self.s.pAll[jNode].color = self.s1.pAll[jNode].color
                self.s.pAll[jNode].x = self.s1.pAll[jNode].x +  self.hwidth + 10
                self.s.pAll[jNode].y = self.s1.pAll[jNode].y +  self.hheight + 10
            
        '''
        Loop for all the nodes in the communities.
        Draw the nodes.
        Draw the Links.
        '''        
        for jNode in range(len(self.s.pAll)):

            #Cross Checking
##            print "Node ID: ",jNode ,"::","Per.Follow: ",(100*len(self.s.pAll[jNode].links))/n1,"%","::","Per.Follower: ",(100*len(self.s.pAll[jNode].follower))/n1
##            print "Follow:  ",len(self.s.pAll[jNode].links),self.s.pAll[jNode].links
##            print "Follower:",len(self.s.pAll[jNode].follower),self.s.pAll[jNode].follower
##            print "-"* 50

            #lenFollower is the number of followers of that node, if No follower then assignning 1 for radius
            #The calculation of radius depends upon the number of follower.
            lenFollower = len(self.s.pAll[jNode].follower)
            if lenFollower == 0:
                lenFollower = 1

            '''
            Drawing Nodes
            '''
            #if (100*lenFollower)/self.n >= self.p:
            _oval = self.canvas.create_oval(self.s.pAll[jNode].x,
                                            self.s.pAll[jNode].y,
                                            self.s.pAll[jNode].x + (self.Radius + (50 * lenFollower)/self.n),
                                            self.s.pAll[jNode].y + (self.Radius + (50 * lenFollower)/self.n),
                                            outline=self.s.pAll[jNode].color,
                                            fill="",
                                            width=2,
                                            activefill="green")
            print _oval
            Widget_to_Node[_oval]= jNode
            self.canvas.tag_bind(_oval,'<ButtonPress-1>',self.__showLinkInfo)
                
##            else:
##                _oval = self.canvas.create_oval(self.s.pAll[jNode].x,
##                                                self.s.pAll[jNode].y,
##                                                self.s.pAll[jNode].x + (self.Radius),
##                                                self.s.pAll[jNode].y + (self.Radius),
##                                                outline="black",width=2,
##                                                activefill="green",
##                                                fill="")#Point_List[jNode].color
##                Widget_to_Node[_oval]= jNode
##                self.canvas.tag_bind(_oval,'<ButtonPress-1>',self.__showLinkInfo)

            '''
            Drawing Links
            '''
##            if (100*lenFollower)/n1 >= self.p1:
##                for iNode in range(len(self.s.pAll[jNode].follower)):
##                    
##                    ToNode= self.s.pAll[jNode].follower[iNode]
##                    self.canvas.create_line(self.s.pAll[jNode].x + self.Half_Radius,
##                                            self.s.pAll[jNode].y + self.Half_Radius,
##                                            self.s.pAll[ToNode].x + self.Half_Radius,
##                                            self.s.pAll[ToNode].y + self.Half_Radius,
##                                            fill="black",
##                                            dash=(4, 4),
##                                            arrow="first",
##                                            activewidth=3)
    
##    def nodeConverter(self,widget_id):
##
##        if widget_id-1 ==1:
##            return widget_id-1
##        else:
##            tempnode = (widget_id/2)
##            widget_id_1 = 2*tempnode - (tempnode -1)
##            return widget_id_1
                
##        if widget_id[0]  <> 1:
##            pNode = self.nodeConverter(widget_id[0])
##            print "Node is:",pNode
##
##            #self.canvas.itemconfig(widget_id[0],fill="red")   #important Line
##            Nodes_Id = self.Nodes.keys()
##            for i in range(len(Nodes_Id)):
##                self.canvas.itemconfig(Nodes_Id[i],fill="")
##                
##            try:
##                if len(self.Links[widget_id[0]]) > 0:
##                    for i in range(len(self.Links[widget_id[0]])):
##                        print self.nodeConverter(self.Links[widget_id[0]][i]),"--->",pNode
##                        self.canvas.itemconfig(self.Links[widget_id[0]][i],fill="red")
##            except:
##                pass
        
    def __showLinkInfo(self,event):

        widget_id = event.widget.find_closest(event.x,event.y)
        jNode = Widget_to_Node[widget_id[0]]
        
        
        nbg.canvas = nbg.Canvas(width=640, height=480, name="NodeBox for OpenGL", resizable=False)
        nodebox_graph.create_graph(jNode,self.s1)
        nbg.canvas.clear
        #nbg.canvas.size = 700,700
        nbg.canvas.fullscreen = True
        nbg.canvas.run(nodebox_graph.draw)
        del nbg.canvas
        


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
        self.No_Nodes_Scale.set(4)
        self.No_Nodes_Scale.bind("<ButtonRelease-1>",self.changeCommunities)#,self.update_beta_2
        self.No_Nodes_Scale.grid(row=1,column=1)

        ##############################################################################################################################
        #Node Control - 1
        self.spinbox_Label= tk.Label(top, text='Number of Nodes?')
        self.spinbox_Label.grid(row=2, column=0)
        self.spinbox_Label= tk.Label(top,text='Nodes 1:')
        self.spinbox_Label.grid(row=3, column=0)
        self.No_Nodes_Scale1 = tk.Scale(top,from_=2, to=200,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale1.set(n1)
        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.changeNodes_n1)#,self.update_beta_2
        self.No_Nodes_Scale1.grid(row=3,column=1)

        #Link Control - 1
        self.spinbox_Label= tk.Label(top, text='Number of Links?')
        self.spinbox_Label.grid(row=2, column=2)
        self.No_Nodes_Scale1 = tk.Scale(top,from_=n1, to=(n1*(n1-1)),orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale1.set(n1)
        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.changeLinks_l1)#,self.update_beta_2
        self.No_Nodes_Scale1.grid(row=3,column=2)

        #Opinion Leader Control - 1
        self.spinbox_Label= tk.Label(top, text='Opinion Leader Percentage')
        self.spinbox_Label.grid(row=2, column=4)
        self.No_Nodes_Scale1 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale1.set(p1)
        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.change_p1)#,self.update_beta_2
        self.No_Nodes_Scale1.grid(row=3,column=4)

##        ##############################################################################################################################
##        #Node Control - 2
##        self.spinbox_Label2= tk.Label(top, text='Number of Nodes?')
##        self.spinbox_Label2.grid(row=4, column=0)
##        self.spinbox_Label2= tk.Label(top,text='Nodes 2:')
##        self.spinbox_Label2.grid(row=5, column=0)
##        self.No_Nodes_Scale2 = tk.Scale(top,from_=2, to=200,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale2.set(5)
##        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeNodes_n2)#,self.update_beta_2
##        self.No_Nodes_Scale2.grid(row=5,column=1)
##
##        #Link Control - 2
##        self.spinbox_Label2= tk.Label(top, text='Number of Links?')
##        self.spinbox_Label2.grid(row=4, column=2)
##        self.No_Nodes_Scale2 = tk.Scale(top,from_=n2, to=(n2*(n2-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale2.set(n2)
##        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeLinks_l2)#,self.update_beta_2
##        self.No_Nodes_Scale2.grid(row=5,column=2)
##
##        #Opinion Leader Control - 2
##        self.spinbox_Label2= tk.Label(top, text='Opinion Leader Percentage')
##        self.spinbox_Label2.grid(row=4, column=4)
##        self.No_Nodes_Scale2 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale2.set(p2)
##        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.change_p2)#,self.update_beta_2
##        self.No_Nodes_Scale2.grid(row=5,column=4)
##
##        ##############################################################################################################################
##        #Node Control - 3
##        self.spinbox_Label3= tk.Label(top, text='Number of Nodes?')
##        self.spinbox_Label3.grid(row=6, column=0)
##        self.spinbox_Label3= tk.Label(top,text='Nodes 3:')
##        self.spinbox_Label3.grid(row=7, column=0)
##        self.No_Nodes_Scale3 = tk.Scale(top,from_=2, to=200,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale3.set(5)
##        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.changeNodes_n3)#,self.update_beta_2
##        self.No_Nodes_Scale3.grid(row=7,column=1)
##
##        #Link Control - 3
##        self.spinbox_Label3= tk.Label(top, text='Number of Links?')
##        self.spinbox_Label3.grid(row=6, column=2)
##        self.No_Nodes_Scale3 = tk.Scale(top,from_=n2, to=(n2*(n2-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale3.set(n3)
##        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.changeLinks_l3)
##        self.No_Nodes_Scale3.grid(row=7,column=2)
##
##        #Opinion Leader Control - 3
##        self.spinbox_Label3= tk.Label(top, text='Opinion Leader Percentage')
##        self.spinbox_Label3.grid(row=6, column=4)
##        self.No_Nodes_Scale3 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale3.set(p3)
##        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.change_p3)
##        self.No_Nodes_Scale3.grid(row=7,column=4)
##
##        ##############################################################################################################################
##        #Node Control - 4
##        self.spinbox_Label4= tk.Label(top, text='Number of Nodes?')
##        self.spinbox_Label4.grid(row=8, column=0)
##
##        self.spinbox_Label4= tk.Label(top,text='Nodes 4:')
##        self.spinbox_Label4.grid(row=9, column=0)
##
##        self.No_Nodes_Scale4 = tk.Scale(top,from_=2, to=200,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale4.set(5)
##        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.changeNodes_n4)#,self.update_beta_2
##        self.No_Nodes_Scale4.grid(row=9,column=1)
##
##        #Link Control - 4
##        self.spinbox_Label4= tk.Label(top, text='Number of Links?')
##        self.spinbox_Label4.grid(row=8, column=2)
##        self.No_Nodes_Scale4 = tk.Scale(top,from_=n4, to=(n4*(n4-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale4.set(n4)
##        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.changeLinks_l4)
##        self.No_Nodes_Scale4.grid(row=9,column=2)
##
##        #Opinion Leader Control - 4
##        self.spinbox_Label4= tk.Label(top, text='Opinion Leader Percentage')
##        self.spinbox_Label4.grid(row=8, column=4)
##        self.No_Nodes_Scale4 = tk.Scale(top,from_=1, to=100,orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale4.set(p4)
##        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.change_p4)
##        self.No_Nodes_Scale4.grid(row=9,column=4)

        ##############################################################################################################################
        #Radius Control
        self.spinbox_Label= tk.Label(top, text='Radius of Nodes?')
        self.spinbox_Label.grid(row=10, column=0)

        self.spinbox_Label= tk.Label(top,text='Radius:')
        self.spinbox_Label.grid(row=11, column=0)

        self.No_Nodes_Scale2 = tk.Scale(top,from_=2, to=20,orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale2.set(20)
        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeRadius)#,self.update_beta_2
        self.No_Nodes_Scale2.grid(row=11,column=1)


    def changeCommunities(self,event):
        global Communities
        Communities = event.widget.get()
        MG=Network(root) #This just generates a new Network with original coordinates
        
    ##############################################################################################################################
    def changeNodes_n1(self,event):
        global n1,l1
        n1 = event.widget.get()
        l1 = n1
        MG=Network(root) #This just generates a new Network with original coordinates

        #self.spinbox_Label= tk.Label(self.top, text='Number of Links?')
        #self.spinbox_Label.grid(row=2, column=2)

        self.No_Nodes_Scale1 = tk.Scale(self.top,from_=n1, to=(n1*(n1-1)),orient=HORIZONTAL,length=200)
        self.No_Nodes_Scale1.set(n1)
        self.No_Nodes_Scale1.bind("<ButtonRelease-1>",self.changeLinks_l1)
        self.No_Nodes_Scale1.grid(row=3,column=2)

    def changeLinks_l1(self,event):
        global l1
        l1 = event.widget.get()
        #print scale        
        MG=Network(root) 

    def change_p1(self,event):
        global p1
        p1 = event.widget.get()
        MG=Network(root) 

##    ##############################################################################################################################    
##    def changeNodes_n2(self,event):
##        global n2
##        n2 = event.widget.get()
##        MG=Network(root) #This just generates a new Network with original coordinates
##
##        self.No_Nodes_Scale2 = tk.Scale(self.top,from_=n2, to=(n2*(n2-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale2.set(n2)
##        self.No_Nodes_Scale2.bind("<ButtonRelease-1>",self.changeLinks_l2)
##        self.No_Nodes_Scale2.grid(row=5,column=2)
##
##
##    def changeLinks_l2(self,event):
##        global l2
##        l2 = event.widget.get()
##        MG=Network(root) 
##
##    def change_p2(self,event):
##        global p2
##        p2 = event.widget.get()
##        MG=Network(root) 
##
##    ##############################################################################################################################    
##    def changeNodes_n3(self,event):
##        global n3
##        n3 = event.widget.get()
##        MG=Network(root) 
##        
##        self.No_Nodes_Scale3 = tk.Scale(self.top,from_=n3, to=(n3*(n3-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale3.set(n3)
##        self.No_Nodes_Scale3.bind("<ButtonRelease-1>",self.changeLinks_l3)
##        self.No_Nodes_Scale3.grid(row=7,column=2)
##
##
##    def changeLinks_l3(self,event):
##        global l3
##        l3 = event.widget.get()
##        MG=Network(root) 
##
##    def change_p3(self,event):
##        global p3
##        p3 = event.widget.get()
##        MG=Network(root)
##
##    ##############################################################################################################################
##    def changeNodes_n4(self,event):
##        global n4
##        n4 = event.widget.get()
##        #print scale
##        MG=Network(root)
##
##        self.No_Nodes_Scale4 = tk.Scale(self.top,from_=n4, to=(n3*(n4-1)),orient=HORIZONTAL,length=200)
##        self.No_Nodes_Scale4.set(n4)
##        self.No_Nodes_Scale4.bind("<ButtonRelease-1>",self.changeLinks_l4)
##        self.No_Nodes_Scale4.grid(row=9,column=2)
##
##
##    def changeLinks_l4(self,event):
##        global l4
##        l4 = event.widget.get()
##        MG=Network(root) 
##
##    def change_p4(self,event):
##        global p4
##        p4 = event.widget.get()
##        MG=Network(root)

    ##############################################################################################################################
    def changeRadius(self,event):
        global Radius
        Radius = event.widget.get()
        MG = Network(root)
        
def onClick():
    inputDialog = Settings(root)
    root.wait_window(inputDialog.top)

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

 
root=Tk()
#root.minsize=(1000,900)
#root.attributes('-fullscreen',True)  #It will hide the title bar but open in maximized mode
w,h = root.winfo_screenwidth(),root.winfo_screenheight()  #It gives screen widht and height

root.state('zoomed')
root.geometry=("1000x900+0+0")

NG=Network(root)

mainButton = tk.Button(root, width=20, text='Settings',command=onClick)
mainButton.grid(row=1, column=1)
root.mainloop()
