"""
Displaying shapefiles (point, polyline and polygons) in a GUI, capable of rendering maps based on
attribute values, and showing basic attribute statistics including the mean, the standard deviation, 
the skewness, and the kurtosis
"""
from Tkinter import Tk,Menu
import Tkconstants
import tkFileDialog
import shp_reader
import dbfload as dbf
from main_canvas import MainCanvas
#from scipy import stats
import math

#Sagar's Edit
from diffusion.SimulatorExperimence import SimulatorExperimence
#Added the simulator class

class MainApp(object):
    """
    The MainApp based on TKinter

    Attributes
    ----------

    root             : Tk
                      The Tk object
    dbfdata          : dictionary
                      The current dbf data
    menubar          : Menu
                      The menu bar
    attibmenu        : Menu
                      The attribute menu
    """
    def __init__(self):
        self.root = Tk()
        self.root.geometry("300x250")
        self.root.title("Shape file Reader")
        self.createMenu()
        self.root.mainloop()

    def createMenu(self):       
        """
        Creates GUI components and register events
        """
        self.menubar = Menu(self.root)
        self.dbfdata = None
        
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.__openShpfile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        
        self.attibmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Attibutes", menu=self.attibmenu,state='disabled')

        #Sagar Jha
        self.menubar.add_cascade(label="Simulator",command=self.__simulate) 
        #Added Simulator 
        
        self.root.config(menu=self.menubar)

    def __simulate(self):
        """
        This function will create object of SimulatorExperimence 
        """
        self.Sim = SimulatorExperimence()
        ## Test to check object type       
        ## print(type(self.Sim))
        self.Sim.doTest()
        
        
    def __openShpfile(self):
        """
        Open a shapefile and read in the contents, pop up the attribute menu 
        with the attributes of the shapefile
        """   
        print "open shape file!"
        directory=tkFileDialog.askopenfilename(filetypes=[("SHAPE_FILE","*.shp")])
        print directory
        
        if directory == "":
            return
        
        self.shapes, self.shp_type, self.bbox = shp_reader.read_shp(directory)
        #read corresponding dbf data
        dbfFile = dbf.DbfLoader(directory[:-3] + "dbf")
        
        t = dbfFile.table2list()
        varNames = dbfFile.get_field_names()
        variables = {}
        for variable in varNames:
            variables[variable] = [record[varNames.index(variable)] for record in t]
            
        if self.dbfdata!=None:
            self.attibmenu.delete(0, len(self.dbfdata)-1)
            
        #add attributes into menu
        for key in variables.keys():  
            self.__addAttribute(key)
        
        self.dbfdata = variables
        self.menubar.entryconfig(2, state=Tkconstants.NORMAL)
    
    def __addAttribute(self,attributeName):
        """
        Add an attribute to the menu
        """
        self.attibmenu.add_command(label=attributeName, command=lambda i=attributeName:self.__updateCanvas(i))
        
    def __updateCanvas(self, attributeName):
        """
        Updates the canvas and showing statistical information
        """
        print "update Canvas "+attributeName
        data_list=self.dbfdata[attributeName]
        
        print "attribute values: ", data_list
        try:
            n, min_max, mean, var, skew, kurt = stats.describe(data_list)
            print "============================"
            print "attribute statistics\n"
            print("Number of units: {0:d}".format(n))
            print("Minimum: {0:8.6f} Maximum: {1:8.6f}".format(min_max[0], min_max[1]))
            print("Mean: {0:8.6f}".format(mean))
            print("Standard deviation: {0:8.6f}".format(math.sqrt(var)))
            print("Skew : {0:8.6f}".format(skew))
            print("Kurtosis: {0:8.6f}".format(kurt))
            print "\n============================"
            
            high=max(data_list)
            low=min(data_list)
            dif=float(high-low)
            
            for i in range(len(data_list)):
                #map colors to 0-200, 0-200, 0-200 (avoid pure white for display purpose)
                index=float(data_list[i]-low)/dif*200
                index=str(hex(200-int(index)).split('x')[1])
    
                color="#"+index+index+index    
                self.shapes[i].color=color
        except:
            print "non-numeric attribute"
            
        self.canvas=MainCanvas(self.shapes,self.bbox,self.shp_type,self.root,attributeName,data_list)
    
if __name__ == '__main__':
    MainApp()
