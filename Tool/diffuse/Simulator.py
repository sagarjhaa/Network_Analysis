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
    def genPoints_Snap(self,Community_Coordinate):
        """
        gen n Points
        """

        #GenFull
        #GenCircle
        #GenGrid
        #GenStar
        #GenTree
        #GenRndGnm
        #GenPrefAttach
        #GenGeoPrefAttach
        #GenForestFire
        #GenSmallWorld
        #GenBaraHierar
        #GenConfModel
        #GenConfModel
        #GenCopyModel
        #GenDegSeq
        #GenRewire
        #GenRndDegK
        #GenRndPowerLaw
        #GenRMat
        #GenRMatEpinions
        
        
        #Graph = snap.GenFull(snap.PNGraph, self.nPoints)
        #Graph = snap.GenFull(snap.PUNGraph, 5)
        #Graph = snap.GenFull(snap.PNEANet, 5)

        #Graph = snap.GenCircle(snap.PNGraph, 5, 5)
        #Graph = snap.GenCircle(snap.PUNGraph, 5, 5)
        #Graph = snap.GenCircle(snap.PNEANet, 5, 5)

        #Graph = snap.GenGrid(snap.PNGraph, 5, 5, False)

        Graph = snap.GenStar(snap.PNGraph, self.nPoints, True)
        #Graph = snap.GenStar(snap.PUNGraph, self.nPoints, True)
        #Graph = snap.GenStar(snap.PNEANet, self.nPoints, True)

        #Graph = snap.GenTree(snap.PNGraph, self.nPoints, self.nPoints)
        #Graph = snap.GenTree(snap.PUNGraph, self.nPoints, self.nPoints)
        #Graph = snap.GenTree(snap.PNEANet, self.nPoints, self.nPoints)

        #Graph = snap.GenRndGnm(snap.PNGraph, self.nPoints, self.nPoints)
        #Graph = snap.GenRndGnm(snap.PUNGraph, self.nPoints, self.nPoints)
        
        for i in Graph.Nodes():

            XmaxNo = max(Community_Coordinate[1])
            XminNo = min(Community_Coordinate[1])
            YmaxNo = max(Community_Coordinate[2])
            YminNo = min(Community_Coordinate[2])

            node=Node()
            node.id=i.GetId()
            
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
                            node.follower.append(EI.GetDstNId())
                        

            self.pAll.append(node)

    def genPoints_GenRndGnm(self,Community_Coordinate):
        """
        gen n Points
        """

        Graph = snap.GenRndGnm(snap.PNGraph,self.nPoints, self.nPoints)

        
        for i in Graph.Nodes():

            XmaxNo = max(Community_Coordinate[1])
            XminNo = min(Community_Coordinate[1])
            YmaxNo = max(Community_Coordinate[2])
            YminNo = min(Community_Coordinate[2])

            node=Node()
            node.id=i.GetId()
            
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
                            node.follower.append(EI.GetDstNId())
                        

            self.pAll.append(node)
            
    def genPoints_GenForestFire(self,Community_Coordinate):
        """
        gen n Points
        """

        Graph = snap.GenForestFire(self.nPoints, 0.5,0.5)

        
        for i in Graph.Nodes():

            XmaxNo = max(Community_Coordinate[1])
            XminNo = min(Community_Coordinate[1])
            YmaxNo = max(Community_Coordinate[2])
            YminNo = min(Community_Coordinate[2])

            node=Node()
            node.id=i.GetId()
            
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
                            node.follower.append(EI.GetDstNId())
                        

            self.pAll.append(node)
        
    def genPoints(self,Community_Coordinate):
        """
        gen n Points
        """
        for i in range(self.nPoints):

            
            XmaxNo = max(Community_Coordinate[1])
            XminNo = min(Community_Coordinate[1])
            YmaxNo = max(Community_Coordinate[2])
            YminNo = min(Community_Coordinate[2])

            node=Node()
            node.id=i
            
            r = lambda: random.randint(0,255)
            rColor = '#%02X%02X%02X' % (r(),r(),r())
            node.color = rColor
            
            node.x=random.randrange(XminNo+1,XmaxNo-20)
            node.y=random.randrange(YminNo+1,YmaxNo-20)
            
            self.pAll.append(node)

    def genLinks(self,nLinks):
        '''
        generate links
        '''
        self.nLinks = nLinks
        tempLinks = 0
        
        for fromId in range(self.nPoints):            
            n = random.randrange(self.nPoints)
            
            while fromId == n or n in self.pAll[fromId].links:
                n = random.randrange(self.nPoints)
                
            tempLinks = tempLinks + 1
            self.pAll[fromId].links.append(n)
            self.pAll[n].follower.append(fromId)

        if tempLinks < self.nLinks:
            self.genRandomLinks(tempLinks)

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
