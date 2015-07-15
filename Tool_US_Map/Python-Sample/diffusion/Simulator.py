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
        
   
    def checkParamters(self):  
        """  chek paramters
        """     
#         if self.nPoints/2>self.nLinks: 
#             print "Error: links need larger than nPoints" 
#             return False
        if self.nT1+self.nT2>self.nPoints: 
            print "Error: nT1+nT2 need less than nPoints" 
            return False 
        if self.nLinks> self.nPoints*self.nPoints: 
            print "Error:Too much links"
            return False         
        
        
        
    def genPoints(self):
        """
        gen n Points
        """
             
        #generator Points        
        for i in range(self.nPoints):
            node=Node()
            node.id=i
            node.x=random.random()
            node.y=random.random()            
            self.pAll.append(node)
        '''self.genPointType(0.5,0.2,5,2)'''
            
    def setPointType(self,nOrigins,nLink1,nLink2,p1,p2):
            
        self.pT1=[]
        self.pT2=[]
        
        self.nOrigins=nOrigins  
        self.pOrgins=[]
         #Set T2 Flag        
#         pid=0
#         while pid<self.nT2:
#             rid=random.randint(0, self.nPoints-1)
#             if(isExist(self.pT2,rid)>-1):
#                 continue
#             if(isExist(self.pT1,rid)>-1):
#                 continue
#             self.pT2.append(rid)
#             self.pAll[rid].p=p2
#             pid=pid+1
#                 
#         #Set T1 Flag     
#         pid=0
#         while pid<self.nT1:
#             rid=random.randint(0, self.nPoints-1)
#             if(isExist(self.pT1,rid)>-1):
#                 continue
#             self.pT1.append(rid)
#             self.pAll[rid].p=p1
#             pid=pid+1               
#        
#             
        #Set Orginal Flag      
        for i in range(self.nPoints):
            point=self.pAll[i]
            point.status=0
            point.p=0
            if(len(point.toIds)>nLink1):
                self.pT1.append(i)
                self.pAll[i].p=p1
            else:
                if len(point.toIds)>nLink2:
                    self.pT2.append(i)
                    point.p=p2
                                  
        pid=0
        while pid<self.nOrigins:
            rid=random.randint(0, self.nPoints-1)
            if(isExist(self.pOrgins,rid)>-1):
                continue
            self.pOrgins.append(rid)
            self.pAll[rid].p=1
            pid=pid+1
        self.nT1=len(self.pT1)
        self.nT2=len(self.pT2)
        self.nOrigins=len(self.pOrgins)  
    def description(self):    
        print "The number of T1 "+str(self.nT1)          
        print "The number of T2 "+str(self.nT1)
         
        
        
          
    def genLinks(self,nLinks):  
        '''
        generate links 
        '''
        self.nLinks=nLinks
        linkid=0   
        for fromId in range(self.nPoints):
            n=random.randint(1,self.nLinks)
            i=0            
            while  i <n:
                toId=random.randint(0,self.nPoints-1)                        
                if self.addLlink(fromId,toId,linkid)==False  : continue
                linkid=linkid+1
                i=i+1
        return linkid+1       
    
    def genRandomLinks(self,nLinks):
        '''
        Generate Random Links 
        '''
        self.nLinks=nLinks
        self.genBasicRandomLinks()
        self.genMoreLinks(self.nPoints-1,nLinks)
   
    def genBasicRandomLinks(self):
        '''
        generate basic Links
        '''
        self.addLlink(0,1,1)
               
        for i in range(2,self.nPoints):
            point=self.pAll[i]
            fromId=random.randint(0,i-1)
            self.addLlink(fromId,1,i-1)  
        
        
    def genMoreLinks(self,linkid,nMoreLinks): 
        '''
        generate links between Points
        '''  
        # Random.seed(0.2)          
        # to generate Links
        # linkid=0    
        while linkid<nMoreLinks:
         
            fromId=random.randint(0,self.nPoints-1)
            toId=random.randint(0,self.nPoints-1)
                        
            if self.addLlink(fromId,toId,linkid)==False  : continue
            linkid=linkid+1
            
    def addLlink(self,fromId,toId,linkId):
        """
        add Link between two Points
        """
        if fromId==toId:                 
            print "error: fromNode is same with toNode"
            return False
        if isExist(self.pAll[fromId].toIds,toId)>-1:
            print self.pAll[fromId].toIds
            print "error: exist links from "+str(fromId)+" to "+str(toId)
            return False
#       if isExist(self.pAll[toId].toIds,fromId)>-1:
#                 continue                     
        
        link=Link()
        link.id=linkId
        link.fromNode=fromId
        link.toNode=toId
        self.pAll[fromId].links.append(Link)
        self.pAll[fromId].toIds.append(toId)  
            
        self.pAll[toId].links.append(Link) #//No direction
        self.pAll[toId].toIds.append(fromId)
        return True     
            
            
    
    def startSimulate(self):
        ''''
        start to simulate
        '''
        if self.checkParamters()==False:
            return 0
        
        self.nCount=0
        self.pUpdated=[]
        toUpdated=[]
        for pid in self.pOrgins:
            #pid=self.pOrgins[i]
            self.pAll[pid].status=100
            toUpdated.append(pid)
        self.pUpdated.append(toUpdated);
        return 1
  
    def hasNextStep(self):
        """   is finished?
        """    
        if self.nCount==0:
            return True            
        l=len(self.getLastUpdated())
        return l>0
    
    
    def nextStep(self):   
        """
        to simulate one step
        """    
        toUpdated=[]         
        for pid in self.pUpdated[self.nCount]:
            point=self.pAll[pid]
            toIds=point.toIds
            #less than the probably, don't spread
            if random.random()>point.p:
                continue
            for toId in toIds:                
                if self.pAll[toId].status==100:
                    continue
                self.pAll[toId].status=100
                toUpdated.append(toId)                    
        self.pUpdated.append(toUpdated);
        self.nCount=self.nCount+1;
        
        return self.nCount+1
    
     
    def getLastUpdated(self):
        '''
        get the Last updated Points
        ''' 
       # print self.nCount
        return self.pUpdated[self.nCount]      
    
    
    def printSummary(self):
        '''
        print run steps
        '''
        print "Simulation in "+str(self.nCount)+" steps"
        
        nSum=0
        for i in range(self.nCount):
            print str(i)+": "+str(len(self.pUpdated[i]))+" points updated!"
            nSum=nSum+len(self.pUpdated[i])
        print str(nSum)+" Points were update, left "+str(self.nPoints-nSum)+"Points."
        return nSum            
    
        
  
    def goSimulate(self,Param):
        '''
        keep simulate until finished
        '''    
        self.startSimulate()
        while( self.nCount==0 or self.hasNextStep()):
            self.nextStep()
        return self.nCount;
    
    
    def getUpdatedNodeByStep(self,nStep):
        '''
        Get the points'id in the nStep step 
        '''
        if(nStep>self.nCount-1):
            return []        
        return self.pUpdated[nStep]
        
    def getStepNum(self):
        """ Get the number of steps before stop
        """
        return self.nCount    
    
    def getX0(self,scale):
        ret=[]
        for i in range(self.nPoints):
            if(isExist(self.pT1, i)):
                continue   
            if(isExist(self.pT2, i)):
                continue
            p=self.pAll[i]         
            ret.append(int(p.x*scale))
        return ret
    
    def getY0(self,scale):
        ret=[]
        for i in range(self.nPoints):
            if(isExist(self.pT1, i)):
                continue   
            if(isExist(self.pT2, i)):
                continue
            p=self.pAll[i]
            ret.append(int(p.y*scale))
        return ret
    def getX1(self,scale):
        ret=[]
        for i in self.pT1:            
            p=self.pAll[i]
            ret.append(int(p.x*scale))
        return ret
    
    def getY1(self,scale):
        ret=[]
        for i in self.pT1:            
            p=self.pAll[i]
            ret.append(int(p.y*scale))
        return ret
    
    def getX2(self,scale):
        ret=[]
        for i in self.pT2:            
            p=self.pAll[i]
            ret.append(int(p.x*scale))
        return ret
    
    def getY2(self,scale):
        ret=[]
        for i in self.pT2:            
            p=self.pAll[i]
            ret.append(int(p.y*scale))
        return ret
    
