'''
Created on Feb 10, 2015

@author: swli
'''
import unittest
from Simulator import Simulator
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
 
    def testSimulator(self):
        s=Simulator(10000,5,2,1000,2000)
        s.genPoints()
        s.genLinks()

        #plt.subplot(121)
        fig, axes = plt.subplots(1, 2, figsize=(12,3))
        axes[0].scatter(s.getX1(1200),s.getY1(1200),s = 10, color='red',alpha=0.5)
        axes[0].set_title("scatter")

        
#         plt.plot(s.getX1(1200),s.getY1(1200),color='red', marker='o', markersize=20)
#         plt.plot(s.getX2(1200),s.getY2(1200),'-',color='blue')
#         plt.title('plot of y=x^2')
        
#         for p in s.pAll:
#             p       
        s.goSimulate("a")
     
        s.printSummary()
        
        x2s=s.getX2(1200)
        y2s=s.getY2(1200)
        
        print(len(x2s))
        print(len(y2s))
        
        axes[1].scatter(x2s,y2s)
        
        axes[1].set_title("simulated")

        
#         plt.subplot(122)
#         plt.plot(s.getX1(1200),s.getY1(1200),'-',color='red')
#         plt.plot(s.getX2(1200),s.getY2(1200),'-',color='blue')
#         plt.title('plot of y=x^2')
        plt.savefig("beauty.png")      
        plt.show()  

        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
