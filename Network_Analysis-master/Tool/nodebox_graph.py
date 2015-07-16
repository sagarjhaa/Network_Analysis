'''
Created on March 17, 2015

@author: sagar jha
'''

from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph

import random as rd

# Create a graph with randomly connected nodes.
# Nodes and edges can be styled with fill, stroke, strokewidth parameters.
# Each node displays its id as a text label, stored as a Text object in Node.text.
# To hide the node label, set the text parameter to None.

g = Graph()

# Random nodes.

def create_graph(p_node,s):

    completed_nodes = []
    uncomplete_nodes = []

    global g

    g = Graph()
    p = p_node
    
    parent_follower  = s.pAll[p_node].follower
    parent_node_name = s.pAll[p_node].id
    
    g.add_node(id=str(parent_node_name),radius = 5,stroke = color(1, 0, 0.25, 1),text = color(1))

    print parent_node_name,"--->",parent_follower
    
    for i in range(len(parent_follower)):
        g.add_node(id=str(parent_follower[i]), 
            radius = 5,
            stroke = color(1), 
              text = color(1))

    completed_nodes.append(parent_node_name)
    
    # Random edges.
    for i in range(len(parent_follower)):
        node1 = str(parent_node_name)
        node2 = str(parent_follower[i])
        uncomplete_nodes.append(parent_follower[i])
        g.add_edge(node1, node2,
                   length = 500.0,
                   weight = random(),
                   stroke = color(1, 0, 0.25, 1))

    print "-"*50
    print "Completed_Nodes  ",completed_nodes
    print "Uncomplete_Nodes ",uncomplete_nodes


##New Round
    while len(uncomplete_nodes) <> 0:
        
        node1 = uncomplete_nodes[0]
        changed_node = node_convert(node1,s)
        follower_list = s.pAll[changed_node].follower

        for i in follower_list:
            if i not in completed_nodes:

                node_1 = str(node1)
                node2 = str(i)
                print node_1,"--->",i
                uncomplete_nodes.append(i)
                g.add_node(id=str(i),radius = 5,stroke = color(1, 0, 0.25, 1),text = color(1))
                g.add_edge(node_1,node2,
                           length = 50.0,
                           stroke = color(1),
                           weight = random())

        completed_nodes.append(node1)                
        del uncomplete_nodes[0]

##  New Round
##    for I in range(len(parent_follower)):
##        
##        p_node = s.pAll[p].follower[I]
##        parent_name = p_node
##        
##        p_node = node_convert(p_node,s)
##        p_links = s.pAll[p_node].follower
##
##        p_node = parent_name #change
##        
##        print parent_name,"-->",p_links
##
##        r     = rd.choice([x * 0.01 for x in range(0,100)]) #rd.choice([0,51,255])    #rd.randint(10,200)
##        green = rd.choice([x * 0.01 for x in range(0,100)]) #rd.choice([255,128,255]) #rd.randint(0,100)
##        b     = rd.choice([x * 0.01 for x in range(0,100)]) #rd.choice([128,0,255])   #rd.randint(0,200)
##
##        if len(p_links) <> 0:
##                
##            for i in range(len(p_links)):
##                node1 = str(parent_name)
##
##                bul = True
##                if p_links[i] not in s.pAll[p].follower:  #Not a parent follower
##                    
##                    for j in range (I):                   #Loop to check another sibling's follower
##                        
##                        sibling = s.pAll[p].follower[j]
##                        sibling = node_convert(sibling,s)
##                        
##                        if p_links[i] in s.pAll[sibling].follower:
##
##                            bul = True #Controlling Parameter
##
##                    if bul:
##                        g.add_node(id=str(p_links[i]),radius = 5,stroke = color(r, green, b, 1),text = color(1))
##                        node2 = str(p_links[i])
##                        g.add_edge(node1, node2,
##                                   length = 50.0,
##                                   weight = random(),
##                                   stroke = color(r, green, b, 1))
                        

    
    

    # Two handy tricks to prettify the layout:
    # 1) Nodes with a higher weight (i.e. incoming traffic) appear bigger.
    for node in g.nodes:
        node.radius = 5#node.radius + node.radius*node.weight
    # 2) Nodes with only one connection ("leaf" nodes) have a shorter connection.
    for node in g.nodes:
        if len(node.edges) == 1:
            node.edges[0].length = 0.5

    g.prune(depth=0)          # Remove orphaned nodes with no connections.
    g.distance         = 25   # Overall spacing between nodes.
    g.layout.force     = 0.01 # Strength of the attractive & repulsive force.
    g.layout.repulsion = 5    # Repulsion radius.

    dragged = None

def node_convert(temp,s):
    for iCounter in range(len(s.pAll)):
        if temp == s.pAll[iCounter].id:
            return iCounter
    

def draw(canvas):

    global g
    
    canvas.clear()
    background(0)
    translate(600, 600) #800,500
    
    # With directed=True, edges have an arrowhead indicating the direction of the connection.
    # With weighted=True, Node.centrality is indicated by a shadow under high-traffic nodes.
    # With weighted=0.0-1.0, indicates nodes whose centrality > the given threshold.
    # This requires some extra calculations.
    g.draw(weighted=0.5, directed=True)
    g.update(iterations=10)
    
    # Make it interactive!
    # When the mouse is pressed, remember on which node.
    # Drag this node around when the mouse is moved.
    dx = canvas.mouse.x - 600 # Undo translate().
    dy = canvas.mouse.y - 600
    global dragged
    if canvas.mouse.pressed and not dragged:
        dragged = g.node_at(dx, dy)
    if not canvas.mouse.pressed:
        dragged = None
    if dragged:
        #dragged.x = dx
        #dragged.y = dy
        if dx < 1000 or dx > 10:
            dragged.x = dx
        if dy < 1000 or dy > 10:
            dragged.y = dy
