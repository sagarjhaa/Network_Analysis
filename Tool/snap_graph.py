import snap

Graph = snap.GenFull(snap.PNGraph, 5)

for EI in Graph.Nodes():
        #print EI.GetId(),EI.GetOutDeg()
  
        for j in Graph.Edges():
             
                if j.GetSrcNId() == EI.GetId():
                        print "edge: (%d, %d)" % (j.GetSrcNId(), j.GetDstNId())
  
        
print  "*" * 50
##for EI in Graph.Edges():
##        print i
##        print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
##        i = i + 1

UGraph = snap.GenFull(snap.PUNGraph, 5)
for EI in UGraph.Edges():
    print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())

print  "*" * 50
Network = snap.GenFull(snap.PNEANet, 5)
for EI in Network.Edges():
    print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
