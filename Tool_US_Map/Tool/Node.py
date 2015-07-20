'''
Created on March 17, 2015

@author: sagar jha
'''

class Node:
    '''
    classdocs
    '''
  
    def __init__(self):
        '''
        Constructor
        '''
        self.x=0
        self.y=0
        self.id=0
        self.links=[]
        self.toIds=[]
        self.shape = ""
        
        self.status=0
        
        self.role = ""
        self.probability = ""
        self.color = ""
        self.follower=[]
        self.cover = False
    
