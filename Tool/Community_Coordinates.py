def CommunityCoordinates_Generator(Communities,w,h):
        
        Width  = w - 250
        Height = h - 150
        Half_Width  = Width/2 
        Half_Height = Height/2
        Community_Coordinate={}
    
        if Communities == 1:
            poly = [10,10,w-170,10,w-170,h-100,10,h-100]
            tempXlist = [poly[x] for x in range(len(poly)) if x%2 ==0]
            tempYlist = [poly[x+1] for x in range(len(poly)) if x%2 ==0]
            Community_Coordinate[Communities] = poly,tempXlist,tempYlist
            return Community_Coordinate
        
        if Communities == 2:
            
            poly = [10,10,Half_Width,10,Half_Width,h-100,10,h-100]
            tempXlist = [poly[x] for x in range(len(poly)) if x%2 ==0]
            tempYlist = [poly[x+1] for x in range(len(poly)) if x%2 ==0]
            Community_Coordinate[Communities-1] = poly,tempXlist,tempYlist

            #Poly2
            poly2=[]
            for i in range(0,len(poly),2):
                poly2.append(poly[i]+Half_Width+70)
                poly2.append(poly[i+1])
                
            tempXlist = [poly2[x] for x in range(len(poly2)) if x%2 ==0]
            tempYlist = [poly2[x+1] for x in range(len(poly2)) if x%2 ==0]
            Community_Coordinate[Communities] = poly2,tempXlist,tempYlist
            return Community_Coordinate
            
        if Communities ==3:
            poly = [10,10,Half_Width,10,Half_Width,Half_Height,10,Half_Height]
            tempXlist = [poly[x] for x in range(len(poly)) if x%2 ==0]
            tempYlist = [poly[x+1] for x in range(len(poly)) if x%2 ==0]
            Community_Coordinate[Communities-2] = poly,tempXlist,tempYlist
            
            #Poly2
            poly2=[]
            for i in range(0,len(poly),2):
                poly2.append(poly[i]+Half_Width+70)
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
                    poly3.append(Width+70)
                poly3.append(poly[i]+Half_Height+50)
            tempXlist = [poly3[x] for x in range(len(poly3)) if x%2 ==0]
            tempYlist = [poly3[x+1] for x in range(len(poly3)) if x%2 ==0]
            Community_Coordinate[Communities] = poly3,tempXlist,tempYlist
            return Community_Coordinate

        if Communities == 4:            
            poly = [10,10,Half_Width,10,Half_Width,Half_Height,10,Half_Height]
            tempXlist = [poly[x] for x in range(len(poly)) if x%2 ==0]
            tempYlist = [poly[x+1] for x in range(len(poly)) if x%2 ==0]
            Community_Coordinate[Communities-3] = poly,tempXlist,tempYlist
            
            #Poly2
            poly2=[]
            for i in range(0,len(poly),2):
                poly2.append(poly[i]+Half_Width+70)
                poly2.append(poly[i+1])
                
            tempXlist = [poly2[x] for x in range(len(poly2)) if x%2 ==0]
            tempYlist = [poly2[x+1] for x in range(len(poly2)) if x%2 ==0]
            Community_Coordinate[Communities-2] = poly2,tempXlist,tempYlist
            
            #Poly3
            poly3=[]
            for i in range(1,len(poly),2):
                poly3.append(poly[i-1])
                poly3.append(poly[i]+Half_Height+50)
            tempXlist = [poly3[x] for x in range(len(poly3)) if x%2 ==0]
            tempYlist = [poly3[x+1] for x in range(len(poly3)) if x%2 ==0]
            Community_Coordinate[Communities-1] = poly3,tempXlist,tempYlist
            
            #Poly4
            poly4=[]
            for i in range(0,len(poly3),2):
                poly4.append(poly3[i]+Half_Width+70)
                poly4.append(poly3[i+1])
                
            tempXlist = [poly4[x] for x in range(len(poly4)) if x%2 ==0]
            tempYlist = [poly4[x+1] for x in range(len(poly4)) if x%2 ==0]
            Community_Coordinate[Communities] = poly4,tempXlist,tempYlist
            return Community_Coordinate
