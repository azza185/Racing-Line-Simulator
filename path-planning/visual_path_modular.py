##general imports for calculations and animation
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import make_interp_spline
import math
import random

##importing cone posisitons for the tracks
from mock_path_planning import Cone,mm1, mm2

##to turn the calculated coords into the normal orientation of the track so it can be animated and ploted on the normal graph
total_theta = 0

##this will rotate the x and y values by a value theta radians
def roation_matrix(x,y,theta):
    rx = x*math.cos(theta) - y*math.sin(theta)
    ry = x*math.sin(theta) + y*math.cos(theta)
    return rx,ry

##this will clear what is plotted on the graph and apply the rotation matrix to each cone in inner and outer then store the new coords
##with the rotation applied
def rotate_track(currentx,currenty,theta):
    rotated_inner = []
    rotated_outer = []
    rotated_orange = []
    plt.cla()
    for cone in inner_cones:
        rx,ry = roation_matrix(cone[0],cone[1],theta)
        rotated_inner.append([rx,ry,cone[2]])
    for cone in outer_cones:
        rx,ry = roation_matrix(cone[0],cone[1],theta)
        rotated_outer.append([rx,ry,cone[2]])
    for cone in orange_cones:
        rx,ry = roation_matrix(cone[0],cone[1],theta)
        plt.plot(rx,ry,'o',c='orange')
        rotated_orange.append([rx,ry,cone[2]])
    
    rx,ry = roation_matrix(currentx,currenty,theta)

    return rotated_inner,rotated_outer,rx,ry,rotated_orange


inner_cones = []
outer_cones = []
orange_cones = []
path_calculated=[]
total_track_path = []


def track(map_mock):
    global cone_pos
    for cone in map_mock:
        cone_pos.append([cone.x_pos,cone.y_pos,cone.colour])
    

##plotting the points on the graph
def make_track():
    inner_x = []
    inner_y = []
    outer_x=[]
    outer_y=[]
    
    for i in range(len(outer_cones)):
        outer_x.append(outer_cones[i][0])
        outer_y.append(outer_cones[i][1])

    for i in range(len(inner_cones)):
        inner_x.append(inner_cones[i][0])
        inner_y.append(inner_cones[i][1])
    

    plt.plot(outer_x,outer_y,'bo')
    plt.plot(inner_x,inner_y,'yo')
    plt.plot(orange_cones[0][0],orange_cones[0][1], 'o', c='orange')
    plt.plot(orange_cones[1][0],orange_cones[1][1], 'o', c='orange')


##sorts cones into inner outer and orange so they can be used for detection in the algorithm
def sort_cone(colour):
        if colour == 'yellow':
            inner_cones.append(cone_pos[i])
        elif colour == 'blue':
            outer_cones.append(cone_pos[i])
        elif colour == 'orange':
            orange_cones.append(cone_pos[i])
        elif colour == None:
            orange_cones.append(cone_pos[i])

starting_x = 0
starting_y = 0

##allows for the starting coords to be calculated between the two trakcs and when the rotation matrix has been applied
def start_coords(orange):
     starting_x = (orange[0][0] + orange[1][0])/2
     starting_y = (orange[0][1] + orange[1][1])/2
     total_track_path.append([starting_x,starting_y])
     return starting_x,starting_y


cone_pos = []

##functions for the different track layouts
# track(mm1)
track(mm2)


##sorting cones into inner and outer cones
for i in range(len(cone_pos)):
    sort_cone(cone_pos[i][2])

make_track()


close_cones = []
def alg(currentx,currenty,outer_cones,inner_cones):
    yellow = False
    blue = False
    orange = False
    ##checking for inner cones that are near the point and have  a x value greater than the current
    ##with the rotation matrix this will allow it to do the whole track without implementation of direction
    for i in range(len(inner_cones)):
        if math.isclose(currentx,inner_cones[i][0],rel_tol =1.5) and math.isclose(currenty,inner_cones[i][1],rel_tol = 1.25):
            if inner_cones[i][0] > currentx:##just to test the code for finding closest mid point of all the cones need to find a way to implemnt direction in simulator
                # if random.random() < 0.3:#0.2
                yellow = True
                close_cones.append([inner_cones[i][0],inner_cones[i][1]])
                pointsx = [currentx,inner_cones[i][0]]
                pointsy = [currenty,inner_cones[i][1]]
        
                
                    
    ##checking for outer cones that are nearby and have a x value greater than the current
    for i in range(len(outer_cones)):
        if math.isclose(currentx,outer_cones[i][0],rel_tol = 1.5) and math.isclose(currenty,outer_cones[i][1],rel_tol = 1.25):
            if outer_cones[i][0] > currentx:
                ##the random function is to test if the algorithm can run with limited perception
                # if random.random() < 0.3:
                blue = True
                close_cones.append([outer_cones[i][0],outer_cones[i][1]])
                pointsx = [currentx,outer_cones[i][0]]
                pointsy = [currenty,outer_cones[i][1]]
                #plt.plot(pointsx,pointsy,'go-')
    for i in range(len(orange_cones)):
        if math.isclose(currentx,orange_cones[i][0],rel_tol = 1.5) and math.isclose(currenty,orange_cones[i][1],rel_tol = 1.25):
            if orange_cones[i][0] > currentx:
                orange = True
                close_cones.append([orange_cones[i][0],orange_cones[i][1]])


            
                

    midpoints = []


    ##all the code for finding midpoints needs edititng once we find a way to do direction to use the current position not starting so it can run until 
    ##it crosses orange cones

    ##connecting all cones and finding the midpoints between them all
    for cone in close_cones:
        for neighbour in close_cones:
            if cone != neighbour:
                x = [currentx,cone[0],neighbour[0]]
                y = [currenty,cone[1],neighbour[1]]
                midpointx = (neighbour[0] + cone[0])/2
                midpointy = (cone[1] + neighbour[1])/2
                midpoints.append([midpointx,midpointy])
                #plt.plot(midpointx,midpointy,'go', c='green')
                #plt.plot(x,y,'-',c='green')

    distances = []

    ##finding the distance from a point to the midpoints whihc can then be sorted to find the shortest length
    for midpoint in midpoints:
        x = midpoint[0] - currentx
        y = midpoint[1] - currenty
        distance = math.sqrt((x**2)+(y**2))
        distances.append([distance,midpoint[0],midpoint[1]])
    sorted_dis = (sorted(distances))

    ##adding the point found to the list of points that are calculated whihc then can be used as the next point to do the calculations
    if len(sorted_dis)  > 0:
        rx,ry = roation_matrix(sorted_dis[0][1],sorted_dis[0][2],-total_theta)
        total_track_path.append([rx,ry])
        path_calculated.append([sorted_dis[0][1],sorted_dis[0][2]])

    
    return yellow,blue,orange


rotate_track(starting_x,starting_y,np.deg2rad(90))


## setting variable to be used to run the algorithm for the whole track and stop
racing = True
seen_orange = False ##used to test if the orange cones have been spotted
##getting the start coordinates for the simulator
currentx,currenty = start_coords(orange_cones)
i = 0
##for the moment this uses a for loop but we could implement detection of orange cones and use a while loop
while racing is True:
    i+=1
    yellow,blue,orange = alg(currentx,currenty,outer_cones,inner_cones)
    currentx = path_calculated[-1][0]
    currenty = path_calculated[-1][1]
    close_cones = []
    if orange is True and i > 2:##checking if the orange cones have been detected after the start line
        seen_orange = True
    ##checking if both yellow and blue cones have been detected
    if yellow is False and blue is True:
        yellow = True
        total_theta += np.deg2rad(90)##1.6
        theta = np.deg2rad(90)
        total_track_path.pop(-1)
        total_track_path.pop(-1)
        inner_cones,outer_cones,currentx,currenty,orange_cones=rotate_track(currentx,currenty,theta)
    elif blue is False and yellow is True:
        total_theta -= np.deg2rad(90)##1.6
        theta = -np.deg2rad(90)
        total_track_path.pop(-1)
        inner_cones,outer_cones,currentx,currenty,orange_cones=rotate_track(currentx,currenty,theta)
    elif blue is True and yellow is True:
        theta = 0
        inner_cones,outer_cones,currentx,currenty,orange_cones=rotate_track(currentx,currenty,theta)
    if orange is False and seen_orange is True: ##checking if orange cones have been detected and have been passed
        racing = False

##rotating track back to normal layout after the algorithm has calculated all the midpoints
plt.cla()
rotated_inner,rotated_outer,rx,ry,rotated_orange=rotate_track(starting_x,starting_y,-total_theta)
for item in rotated_orange:
    plt.plot(item[0],item[1],'o',c='orange')

for item in rotated_inner:
    plt.plot(item[0],item[1],'yo')

for item in rotated_outer:
    plt.plot(item[0],item[1],'bo')

starting_x,starting_y = start_coords(orange_cones)

i = 0

##plot all the calculated points with green dots
# for item in total_track_path:
#     plt.plot(item[0],item[1],'go')
#     print(item[0],item[1])
#     print(i)
#     i+=1
#     pass


##applying a spline to the line so the animation is smoother without changing the curve of the line too much
xbase = []
ybase = []
for point in total_track_path:
    xbase.append(point[0])
    ybase.append(point[1])

xbase = np.array(xbase)
ybase = np.array(ybase)

param = np.linspace(0, 1, xbase.size)
spl = make_interp_spline(param, np.c_[xbase,ybase], k=1) #(1)
xnewbase, y_smooth = spl(np.linspace(0, 1, xbase.size * 5)).T #(2)

xbasenew = []
ybasenew = []

##animation of the spline
def animate2(k):
    xbasenew.append(xnewbase[k])
    ybasenew.append(y_smooth[k])
    plt.plot(xbasenew,ybasenew)

xnew = []
ynew = []

##animation of all the points calculated without the spline
def animate(j):
    xnew.append(total_track_path[j][0])
    ynew.append(total_track_path[j][1])
    plt.plot(xnew,ynew)

##the animations for the calculated line around the track
#animation_1 = animation.FuncAnimation(plt.gcf(),animate,interval=50,save_count=69)
animation_2 = animation.FuncAnimation(plt.gcf(),animate2,interval=1)
plt.show()