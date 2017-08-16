'''
Created on Jul 14, 2017

@author: picard
'''
import pygame
import numpy as np


########################################################## 
# Modified after Steve LaValle
# 2011
# http://msl.cs.illinois.edu/~lavalle/sub/rrt.py
#
#########                         

class Node():
    
    _next_p = None
    _previous_p = None
    _point = None
    
    def __init__(self, point, previous_p, next_p):
        
        if not isinstance(point,tuple):
            raise Exception("Wrong type of point, should be tuple but is " + str(type(point)) + " - " + str(point))
        
        self._next_p = next_p
        self._previous_p = previous_p
        self._point = point

def dist(p1, p2):
    if not isinstance(p1, Node):
        raise Exception("Wrong type of p1, should be Node but is " + str(type(p1)) + " - " + str(p1))
    if not isinstance(p2, Node):
        raise Exception("Wrong type of p2, should be Node but is " + str(type(p2)) + " - " + str(p2))
    
        
    p1 = p1._point
    p2 = p2._point
    
    return np.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

def step_from_to(p1, p2, epsilon):
    
        previous_node = p1

        if dist(p1, p2) < epsilon:
            return Node(p2._point, previous_node, None)
        else:
                    
            p1 = p1._point
            p2 = p2._point
            
            theta = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
            return Node((p1[0] + epsilon * np.cos(theta), p1[1] + epsilon * np.sin(theta)), previous_node, None)

 
 
def get_safe_path(own_xy, other_xys, goal_xy, safety_range, distance_to_goal, radius_arena, timestep):
    
     
    visualize = False
     
    XDIM = 640
    YDIM = 480
    WINSIZE = [XDIM, YDIM]
     
    if visualize:
        pygame.init()
        screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption('RRT      S. LaValle    May 2011')
        white = 255, 240, 200
        black = 20, 20, 40
        red = 255,0,0
        screen.fill(black)
    seed = 42
    np.random.seed(seed)
    numnodes = 5000
    nodes = []
    other_current_xy = []
    epsilon = 0.4
    own_point = Node((own_xy[0], own_xy[1]), None, None)
    scale_factor = 50
    shift_factor = 50
    nodes.append(own_point)
 
    # Add the other positions to a short list
    for other_xy in other_xys:
            # Right now we look at the current situation and search a path. 
            # It is repeated each time in the future we look for a path.
            other_current_xy.append(other_xy[timestep])
 
    for i in range(numnodes):
         
        next_node = nodes[0]
         
        random_point_safe = False
        while not random_point_safe:
            random_point = Node((np.random.uniform(low=-1.0,high=1.0) * radius_arena, np.random.uniform(low=-1.0,high=1.0) * radius_arena), None, None)
            random_point_safe = True
            # Check if new point is not too close to obstacle
            for other_xy in other_current_xy:
                if dist(random_point, Node(other_xy, None, None)) < safety_range:
                    random_point_safe = False
                    break
         
        for act_node in nodes:
         
            if dist(act_node, random_point) < dist(next_node, random_point):
                next_node = act_node
                 
        newnode = step_from_to(next_node, random_point, epsilon)
             
        # Check if new point is not too close to obstacle
        newnode_safe = True
        for other_xy in other_current_xy:
            if dist(newnode, Node(other_xy, None, None)) < safety_range:
                # If it is too close, the node will not be appended
                newnode_safe = False
                break
             
        if not newnode_safe:
            continue
             
        nodes.append(newnode)
         
        if visualize:
           
            vis_point_a = (next_node._point[0]*scale_factor+4*shift_factor,next_node._point[1]*scale_factor+shift_factor)
            vis_point_b = (newnode._point[0]*scale_factor+4*shift_factor,newnode._point[1]*scale_factor+shift_factor)
             
            pygame.draw.line(screen, white, vis_point_a,vis_point_b)
            pygame.display.update()
 
        if dist(newnode, Node(goal_xy,None,None)) < distance_to_goal:
            return_path = []
             
            previous = newnode._previous_p
            return_path.append(newnode)
             
            while(previous != None):
                return_path.append(previous)
                previous = previous._previous_p
                 
            return return_path
             

#########
# Modified after Steve LaValle
# 2011
# http://msl.cs.illinois.edu/~lavalle/sub/rrt.py
#
##########################################################
