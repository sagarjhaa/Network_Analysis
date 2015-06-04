import snap

##Graph = snap.GenRndGnm(snap.PNGraph, 30,300)
##i=1
##for EI in Graph.Nodes():
##        #print EI.GetId(),EI.GetOutDeg()
##  
##        for j in Graph.Edges():
##             
##                if j.GetSrcNId() == EI.GetId():
##                        print i,"edge: (%d, %d)" % (j.GetSrcNId(), j.GetDstNId())
##                        i = i + 1
##  
##        
##print  "*" * 30
####for EI in Graph.Edges():
####        print i
####        print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
####        i = i + 1
##
##UGraph = snap.GenRndGnm(snap.PUNGraph, 3,3)
##i =1
##for EI in UGraph.Edges():
##    print i,"edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
##    i = i + 1
##
##print  "*" * 30
##Network = snap.GenRndGnm(snap.PNEANet, 3,3)
##i=1
##for EI in Network.Edges():
##    print i,"edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
##    i = i + 1
Graph = snap.GenForestFire(10, 0.5, 0.5)
for EI in Graph.Edges():
    print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
