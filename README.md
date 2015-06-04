# Network_Analysis
Python based tool to visualize diffusion of message in different social media networks.
Executive Summary
The network analysis tool is one of its kind where different network can be used to simulate the diffusion of message in social media.
The tool is currently tested on windows system.

















How to configure the machine?
1)	Download the Network_Analysis tool from the follow link:
https://github.com/sagarjhaa/Network_Analysis

2)	Unzip the downloaded folder. The folder structure is as shown below.
a.	Requirement
i.	Nodebox (folder)
ii.	pyglet (folder)
iii.	_snap.pyd
iv.	Python-2.7.10.amd64
v.	snap.py
vi.	vcredist_x64
b.	Tool
i.	Diffuse (folder)
ii.	Community_Coordinates.py
iii.	nodebox_graph.py
iv.	Spacetime_network.py

The requirement folder is containing the files and modules needed by the tool to execute the functionality. Whereas the Tool folder contain the actual program files to visualize the network.


How to install
Installation of python 2.7 – 64 bit version
	In the Requirement folder, double click the “Python-2.7.10.amd64” and follow the steps prompt on the screen to successfully install python.
	After successfully installation check the system path variable for path to python scripts and other libraries.
How to check path variable?
	Select Computer from the Start menu
	Choose System Properties from the context menu
	Click Advanced system settings > Advanced tab
	Click on Environment Variables, under System Variables, find PATH, and click on it.
	The PATH should contain the path to python folder in your system.
•	For example I have installed it in “C:\Python27” then the PATH should contain.
	C:\Python27\Scripts
	C:\Python27
	C:\Python27\Lib\site-packages
•	If the path to python folders is not there then manually add the path to the PATH variable.

Installation of SNAP and Nodebox module for python
	Firstly install the Visual C++ Redistributable for Visual Studio 2012 to use the SNAP module in python programming. 
	To install it, double click the “vcredist_x64” from the requirement folder and follow the steps.
	Once it is done, open the folder where python is installed in your system. It will somewhat look like this.
	Go to the path: *\Python27\Lib\site-packages\
	Copy the following files/folder from the Requirement folder to the site-packages folder.
•	nodebox  (folder)
•	pyglet (folder)
•	_snap.pyd (file)
•	Snap.py (file)

The machine is now configure to run the tool without error. Now we can import modules like SNAP and Nodebox into the python script and use the additional functionality in our analysis.
How to run the tool?
The files to run the tools are available into the “Tool” folder.
1)	Double click the spacetime_network.py file and it will show up the following GUI with similar figure.

2)	Click on the “Settings” button and it will open the setting’s menu as shown below.


3)	Slide the Node 1 Slider and increase it to the 10 and Number of links to 40.It will show something like this where some circle are colored and some are not to show the number of follower. The more the number of follower, the bigger is the circle.



4)	Click on the colored circle to see the network. Press escape to exit the visualization.




Queries
If you face any issue during executing the tool. Follow the step.
1)	Check the path to python folder is there in the PATH variable in the system.
2)	Write your queries to me at sjha1@kent.edu with the exact error or warning message. If possible attach screenshot for better understanding. 
