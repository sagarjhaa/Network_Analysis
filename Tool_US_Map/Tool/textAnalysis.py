'''
Created on May 15,2015
@author: Sagar Jha
'''

import nltk as nltk
from Tkinter import *

class analysisWidget(object):
    def __init__(self,master,text):
        top=self.top=Toplevel(master)

        self.text = text
        self.top.title("Text Analysis")

        self.inputbox = Entry(top,font = "Helvetica 16")
        self.inputbox.pack(fill=BOTH,expand=1)
         
        self.searchText = Button(top,text="SearchText",command=self.__searchText)
        self.searchText.pack(fill=BOTH,expand=1)

        self.searchSText = Button(top,text="Search Similar Text",command=self.__searchSimilarText)
        self.searchSText.pack(fill=BOTH,expand=1)

        self.searchCText = Button(top,text="Search Common Context Text",command=self.__seachCommonConText)
        self.searchCText.pack(fill=BOTH,expand=1)

        self.dPlot = Button(top,text="Dispersion Plot",command=self.__dispersionPlot)
        self.dPlot.pack(fill=BOTH,expand=1)
        
        self.fDist = Button(top,text="Frequency Distribution",command=self.__frequencyDistribution)
        self.fDist.pack(fill=BOTH,expand=1)

##        self.b=Button(top,text='Ok',command=self.cleanup)
##        self.b.pack(fill=BOTH,expand=1)
##        self.top.grab_set_global()

    def findValue(self):
        return self.Choice.get()
        
    def cleanup(self):
        self.top.destroy()

    def readTextbox(self):
       inputtext = self.inputbox.get()
       self.inputlist = []
       
       if inputtext <> "":
          self.inputlist = inputtext.split(",")
       else:
          print "Please enter words into the textbox!!!"
    

    def __searchText(self):
      print "Search Text"
      print "-" * 50
      self.readTextbox()
      for i in range(len(self.inputlist)):
         self.text.concordance(self.inputlist[i])
         print "-" * 50
      
    def __searchSimilarText(self):

      print "Search Similar Text"
      print "-" * 50
      self.readTextbox()
      for i in range(len(self.inputlist)):
         self.text.similar(self.inputlist[i])
         print "-" * 50

    def __seachCommonConText(self):

       print "Search common context"
       print "-" * 50
       self.readTextbox()
       self.text.common_contexts(self.inputlist)
       print "-" * 50
       
    def __dispersionPlot(self):

       print "Dispersion Plot"
       self.readTextbox()
       self.text.dispersion_plot(self.inputlist)
       print "-" * 50

    def __frequencyDistribution(self):

      print "Frequency Distribution"
      fdist1 = nltk.FreqDist(self.text)
      vocab1 = fdist1.keys()
      print "-" * 50

      iNum = 50
      if len(vocab1) < iNum:
         iNum = len(vocab1)
      
      fdist1.plot(iNum,cumulative=True)
      print "-" * 50




      
      
