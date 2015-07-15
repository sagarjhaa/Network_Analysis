'''
Created on Feb 12, 2015

@author: swli
'''
from Simulator import Simulator

class SimulatorExperimence(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
     
    '''   
    def MutiTimes(self,nPoints,nLinks,nOrg,nT1,nT2,nTimes):
        nSteps=0;
        for i in range(10):
            s=Simulator(nPoints)
            s.genPoints()
            s.genRandomLinks(nLinks)
            s.setPointTyp(2,nT1,nT2,p1,p2)
            s.goSimulate("a")
            nSteps=nSteps+s.getStepNum()
            print nSteps
        return nSteps
    '''        
    def testLinks(self):
        tests=[]
        for i in range(2,30):        
            nSteps=self.MutiTimes(1000,i,1,10,20,100)
            print str(i) +":"+str(nSteps)
            tests.append(nSteps)
        print tests               
        return 
    
    
    def doTest(self):
       # self.doT1Number()
        #self.doT1P()
        #self.doT2Number()
        #self.doT2P()
        self.doT1nT2n()
        #self.doT1pT2p()

    def doT1pT2p(self):
        nPnt=1000
        nLink=40
        nT1=40
        nT2=20
        tests=""
        s=Simulator(nPnt)
        s.genPoints()
        s.genRandomLinks(nLink*nPnt) 
        
        f2 = open('doT1pT2p2.txt', 'w')               
        for i in range(0,101):     
            for j in range(0,i+1):   
                nSteps=self.MutiTimesNoGen(s,1,nT1,nT2,0.01*i,0.01*j)
                print str(i)+"\t"+ str(j) +"\t"+str(nSteps)
                f2.write(str(i)+"\t"+ str(j) +"\t"+str(nSteps)+"\n")
                tests=tests+str(nSteps)+"\t"
            for j in range(i,101):  
                tests=tests+"0\t"
            tests=tests+("\n")    
        f = open('doT1pT2p.txt', 'w')
        f.write(tests)
                  
        return       

    def doT1nT2n(self):
        nPnt=1000
        nLink=40
        
        tests=""
        s=Simulator(nPnt)
        s.genPoints()
        s.genRandomLinks(nLink*nPnt)    
        f2=    open('doT1nT2n2.txt', 'w')
        for i in range(0,100):     
            for j in range(0,i+1):   
                nSteps=self.MutiTimesNoGen(s,1,i,j,0.5,0.2)
                print str(i)+"\t"+ str(j) +"\t"+str(nSteps)
                f2.write(str(i)+"\t"+ str(j) +"\t"+str(nSteps)+"\n")
                tests=tests+str(nSteps)+"\t"
            for j in range(i,101):  
                tests=tests+"0\t"
            tests=tests+("\n")    
        f = open('doT1nT2n.txt', 'w')
        f.write(tests)
                  
        return    
        
    def doT2P(self):
        tests=[]
        s=Simulator(1000,40)
        s.genPoints()
        s.genLinks()
        for i in range(10,51):        
            nSteps=self.MutiTimesNoGen(s,1,20,0.5,0.01*i)
            print str(i*0.01) +"\t"+str(nSteps)
            tests.append(nSteps)
        print tests               
        return         
    def doT1P(self):
        tests=[]
        s=Simulator(1000)
        s.genPoints()
        #s.genLinks(10*1000)
        s.genRandomLinks(10*1000)
        #s.setPointType(nOrigins, nLink1, nLink2, p1, p2)
        for i in range(20,101):        
            nSteps=self.MutiTimesNoGen(s,1,30,10,0.01*i,0.2)
            print str(i*0.01) +"\t"+str(nSteps)
            tests.append(nSteps)
        print tests               
        return 
    def doT1Number(self):            
        tests=[]
        s=Simulator(1000,40,1)
        s.genPoints()
        #s.genLinks()
        s.genRandomLinks(5*1000)
        for i in range(20,41):        
            nSteps=self.MutiTimesNoGen(s,2,i,20,0.5,0.2)
            print str(i) +"\t"+str(nSteps)
            tests.append(nSteps)
        print tests               
        return 
    def doT2Number(self):            
        tests=[]
        s=Simulator(1000,40,1)
        s.genPoints()
        s.genRandomLinks(40)
        for i in range(10,31):        
            nSteps=self.MutiTimesNoGen(s,2,30,i,0.5,0.2)
            print str(i) +"\t"+str(nSteps)
            tests.append(nSteps)
        print tests               
        return 
    def MutiTimesNoGen(self,s,nOrgin,nLink1,nLink2,p1,p2):        
        nSteps=0;
        for i in range(2):   #Change this to 100 to take time
            s.setPointType(nOrgin,nLink1,nLink2,p1,p2)                    
            s.goSimulate("a")
            nSteps=nSteps+s.getStepNum()
        #  print nSteps
        return nSteps*1.0/100
        
if __name__ == "__main__":       
    SimulatorExperimence().doTest()
        
