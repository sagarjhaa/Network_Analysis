'''
Created on Feb 9, 2015

@author: swli
'''

from Node import Node
from Link import Link  
import random 
import copy

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
