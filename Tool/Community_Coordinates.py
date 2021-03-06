'''
Created on March 17, 2015

@author: sagar jha
'''

def CommunityCoordinates_Generator(Communities,w,h):
        
        Width  = w-250 
        Height = h-150
        Half_Width  = Width/2 
        Half_Height = Height/2
        Community_Coordinate={}

        gap = 10
        
        if Communities == 1:
            poly = [10,10,Width-gap,10,Width-gap,Height-gap,10,Height-gap]
            tempXlist = [poly[x] for x in range(len(poly)) if x%2 ==0]
            tempYlist = [poly[x+1] for x in range(len(poly)) if x%2 ==0]
            Community_Coordinate[Communities] = poly,tempXlist,tempYlist
            return Community_Coordinate
        
        if Communities == 2:
            poly = [10,10,Half_Width-gap,10,Half_Width-gap,Height-gap,10,Height-gap]
            tempXlist = [poly[x] for x in range(len(poly)) if x%2 ==0]
            tempYlist = [poly[x+1] for x in range(len(poly)) if x%2 ==0]
            Community_Coordinate[Communities-1] = poly,tempXlist,tempYlist

            #Poly2
            poly2=[]
            for i in range(0,len(poly),2):
                poly2.append(poly[i]+Half_Width+gap)
                poly2.append(poly[i+1])
                
            tempXlist = [poly2[x] for x in range(len(poly2)) if x%2 ==0]
            tempYlist = [poly2[x+1] for x in range(len(poly2)) if x%2 ==0]
            Community_Coordinate[Communities] = poly2,tempXlist,tempYlist
            return Community_Coordinate
            
        if Communities ==3:
            poly = [10,10,Half_Width-gap,10,Half_Width-gap,Half_Height-gap,10,Half_Height-gap]
            tempXlist = [poly[x] for x in range(len(poly)) if x%2 ==0]
            tempYlist = [poly[x+1] for x in range(len(poly)) if x%2 ==0]
            Community_Coordinate[Communities-2] = poly,tempXlist,tempYlist
            
            #Poly2
            poly2=[]
            for i in range(0,len(poly),2):
                poly2.append(poly[i]+Half_Width+gap)
                poly2.append(poly[i+1])
                
            tempXlist = [poly2[x] for x in range(len(poly2)) if x%2 ==0]
            tempYlist = [poly2[x+1] for x in range(len(poly2)) if x%2 ==0]
            Community_Coordinate[Communities-1] = poly2,tempXlist,tempYlist
            
            #Poly3
            poly3=[]
            for i in range(1,len(poly),2):
                if i-1 == 0 or i-1 == 6:
                    poly3.append(poly[i-1])
                else:
                    poly3.append(poly[i-1])
                    #poly3.append(Width)
                poly3.append(poly[i]+Half_Height+gap)
            tempXlist = [poly3[x] for x in range(len(poly3)) if x%2 ==0]
            tempYlist = [poly3[x+1] for x in range(len(poly3)) if x%2 ==0]
            Community_Coordinate[Communities] = poly3,tempXlist,tempYlist
            return Community_Coordinate

        if Communities == 4:
            #gap = 10
            poly = [10,10,Half_Width-gap,10,Half_Width-gap,Half_Height-gap,10,Half_Height-gap]
            tempXlist = [poly[x] for x in range(len(poly)) if x%2 ==0]
            tempYlist = [poly[x+1] for x in range(len(poly)) if x%2 ==0]
            Community_Coordinate[Communities-3] = poly,tempXlist,tempYlist
            
            #Poly2
            poly2=[]
            for i in range(0,len(poly),2):
                poly2.append(poly[i]+Half_Width +gap)   #70
                poly2.append(poly[i+1])   
            tempXlist = [poly2[x] for x in range(len(poly2)) if x%2 ==0]
            tempYlist = [poly2[x+1] for x in range(len(poly2)) if x%2 ==0]
            Community_Coordinate[Communities-2] = poly2,tempXlist,tempYlist
            
            #Poly3
            poly3=[]
            for i in range(1,len(poly),2):
                poly3.append(poly[i-1])
                poly3.append(poly[i]+Half_Height+gap)  #50

            tempXlist = [poly3[x] for x in range(len(poly3)) if x%2 ==0]
            tempYlist = [poly3[x+1] for x in range(len(poly3)) if x%2 ==0]
            Community_Coordinate[Communities-1] = poly3,tempXlist,tempYlist
            
            #Poly4
            poly4=[]
            for i in range(0,len(poly3),2):
                poly4.append(poly3[i]+Half_Width +gap)   #70
                poly4.append(poly3[i+1])
                
            tempXlist = [poly4[x] for x in range(len(poly4)) if x%2 ==0]
            tempYlist = [poly4[x+1] for x in range(len(poly4)) if x%2 ==0]
            Community_Coordinate[Communities] = poly4,tempXlist,tempYlist
            return Community_Coordinate
