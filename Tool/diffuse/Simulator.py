'''
Created on March 17, 2015

@author: sagar jha
'''

from Node import Node
from Link import Link  
import random 
import copy

import snap

def isExist(l,key):
    for k in l:
        if(k==key):
            return 1
    return -1

NodeID = 0


class Simulator:
    '''
    Simulator for Difussion
    '''       
     
    def __init__(self,nPoints):
        '''
        Constructor
        '''  
        
        #Number of ...
        self.nPoints=nPoints
         
        #Array of ...
        self.pAll=[]
        
        #Step state 
        self.nCount=0
        self.pUpdated=[]
                
        '''self.checkParamters()
        '''
    def genPoints_GenStar(self,Community_Coordinate):
        """
        gen n Points
        """
        global NodeID
        
        print "-" * 50
        print "GenStar"
        print "-" * 50

        Graph = snap.GenStar(snap.PNGraph, self.nPoints, True)

        temp = {}
        for i in Graph.Nodes():
            #print i.GetId()
            temp[i.GetId()] = NodeID
            NodeID = NodeID + 1
        
        for i in Graph.Nodes():

            XmaxNo = max(Community_Coordinate[1])
            XminNo = min(Community_Coordinate[1])
            YmaxNo = max(Community_Coordinate[2])
            YminNo = min(Community_Coordinate[2])

            node=Node()
            node.id=temp[i.GetId()]#i.GetId()
            
            r = lambda: random.randint(0,255)
            rColor = '#%02X%02X%02X' % (r(),r(),r())
            node.color = rColor
            
            node.x=random.randrange(XminNo+1,XmaxNo-20)
            node.y=random.randrange(YminNo+1,YmaxNo-20)
            
            #self.pAll.append(node)
            
            for EI in Graph.Edges():
                if EI.GetSrcNId() == i.GetId():
                        #print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())

                        if EI.GetSrcNId() <> EI.GetDstNId() :
                            node.follower.append(temp[EI.GetDstNId()])
                            #node.follower.append(EI.GetDstNId())
                        
            print node.id, node.follower
            self.pAll.append(node)

    def genPoints_GenRndGnm(self,Community_Coordinate):
        """
        gen n Points
        """
        print "-" * 50
        print "GenRndGnm"
        print "-" * 50

        global NodeID
        
        Graph = snap.GenRndGnm(snap.PNGraph,self.nPoints, self.nPoints)

        temp = {}
        for i in Graph.Nodes():
            #print i.GetId()
            temp[i.GetId()] = NodeID
            NodeID = NodeID + 1
        
        for i in Graph.Nodes():

            XmaxNo = max(Community_Coordinate[1])
            XminNo = min(Community_Coordinate[1])
            YmaxNo = max(Community_Coordinate[2])
            YminNo = min(Community_Coordinate[2])

            node=Node()
            node.id=temp[i.GetId()]#i.GetId()
            
            r = lambda: random.randint(0,255)
            rColor = '#%02X%02X%02X' % (r(),r(),r())
            node.color = rColor
            
            node.x=random.randrange(XminNo+1,XmaxNo-20)
            node.y=random.randrange(YminNo+1,YmaxNo-20)
            
            #self.pAll.append(node)
            
            for EI in Graph.Edges():
                if EI.GetSrcNId() == i.GetId():
                        #print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())

                        if EI.GetSrcNId() <> EI.GetDstNId() :
                            node.follower.append(temp[EI.GetDstNId()])
                            #node.follower.append(EI.GetDstNId())
                        
            print node.id, node.follower
            self.pAll.append(node)
            
    def genPoints_GenForestFire(self,Community_Coordinate):
        """
        gen n Points
        """

        print "-" * 50
        print "GenForestFire"
        print "-" * 50

        global NodeID
        
        Graph = snap.GenForestFire(self.nPoints, 0.5,0.5)

        temp = {}
        for i in Graph.Nodes():
            #print i.GetId()
            temp[i.GetId()] = NodeID
            NodeID = NodeID + 1
        
        
        for i in Graph.Nodes():

            XmaxNo = max(Community_Coordinate[1])
            XminNo = min(Community_Coordinate[1])
            YmaxNo = max(Community_Coordinate[2])
            YminNo = min(Community_Coordinate[2])

            node=Node()
            node.id=temp[i.GetId()]#i.GetId()
            
            r = lambda: random.randint(0,255)
            rColor = '#%02X%02X%02X' % (r(),r(),r())
            node.color = rColor
            
            node.x=random.randrange(XminNo+1,XmaxNo-20)
            node.y=random.randrange(YminNo+1,YmaxNo-20)
            
            #self.pAll.append(node)
            
            for EI in Graph.Edges():
                if EI.GetSrcNId() == i.GetId():
                        #print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())

                        if EI.GetSrcNId() <> EI.GetDstNId() :
                            node.follower.append(temp[EI.GetDstNId()])
                            #node.follower.append(EI.GetDstNId())
                        
            print node.id, node.follower
            self.pAll.append(node)
        
    def genPoints(self,Community_Coordinate):
        """
        gen n Points
        """
        global NodeID
        print "Random Network"
        print "-" * 50
        
        for i in range(self.nPoints):

            
            XmaxNo = max(Community_Coordinate[1])
            XminNo = min(Community_Coordinate[1])
            YmaxNo = max(Community_Coordinate[2])
            YminNo = min(Community_Coordinate[2])

            node=Node()
            node.id=NodeID
            #print "NodeID ",node.id
            NodeID = NodeID + 1
            
            
            r = lambda: random.randint(0,255)
            rColor = '#%02X%02X%02X' % (r(),r(),r())
            node.color = "#CC0000" #rColor
            
            roleList = ['T1','T2','T3']
            node.role = random.choice(roleList)

            if node.role == "T1":
                node.probability = random.uniform(0,0.5)
            if node.role == "T2":
                node.probability = random.uniform(0,0.2)
            if node.role == "T3":
                node.probability = random.uniform(0,0.05)
            
            node.x=random.randrange(XminNo+1,XmaxNo-20)
            node.y=random.randrange(YminNo+1,YmaxNo-20)
            
            self.pAll.append(node)

    def genLinks(self,nLinks):
        '''
        generate links
        '''
        self.nLinks = nLinks
        tempLinks = 1
        
        for fromId in range(self.nPoints):
            n = random.randrange(self.nPoints)
            
            while self.pAll[fromId].id == self.pAll[n].id or self.pAll[n].id in self.pAll[fromId].links:
                n = random.randrange(self.nPoints)
                
            tempLinks = tempLinks + 1
            #print "fromId ",fromId,"appending: ",self.pAll[n].id
            self.pAll[fromId].links.append(self.pAll[n].id)
            self.pAll[n].follower.append(self.pAll[fromId].id)

##        if tempLinks < self.nLinks:
##            self.genRandomLinks(tempLinks)

    def genRandomLinks(self,tempLinks):
        '''
        generate random links
        '''
        while tempLinks < self.nLinks:
            fromId =random.randrange(0,self.nPoints)
            n = random.randrange(self.nPoints)
            while fromId == n and n in self.pAll[fromId].links and len(self.pAll[fromId].links) == self.nPoints-1:
                fromId =random.randrange(0,self.nPoints)
                n = random.randrange(self.nPoints)
                
            if fromId <> n and n not in self.pAll[fromId].links:
                self.pAll[fromId].links.append(n)
                self.pAll[n].follower.append(fromId)
                #ilinks = ilinks + 1
                tempLinks = tempLinks + 1
