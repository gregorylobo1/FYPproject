#!/usr/bin/env python
# attempts to subscribe and print data from the pointcloud data

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3
import math

global ang_min
global a_inc
radius = 0.55                # swing diameter of 52 cm, with tolerancing of +3cm
rmin = 0.040
rmax = 2.5

rospy.init_node('leg_find')

#ns_pub = rospy.Publisher("vector", Vector3, queue_size = 1)

def polar_dist(r1, a1, r2, a2):
    '''calculate polar distance between points'''
    global ang_min
    global a_inc

    th1 = ang_min + a1*a_inc
    th2 = ang_min + a2*a_inc
    dist = math.sqrt(r1*r1 + r2*r2 - 2*r1*r2*math.cos(th1 - th2))
    return dist

def read_cb(data):
    global ang_min
    global a_inc
    global radius
    global rmin
    global rmax

    # reset feature variables
    angle = []
    far = 0
    vector = Vector3()
    temp_i = 0
    temp_f = 0
    leg = []
    leg_c = 0

    # ensure laser variables are up to date
    ang_min = data.angle_min
    ang_max = data.angle_max
    a_inc = data.angle_increment

    # initialise scan data to be mutable object
    new_scan = list(data.ranges)
    print('New Leg')

    # reject invalid data and initialise new data to be published
    for c, data_l in enumerate(data.ranges):
        angle.append(ang_min + c*a_inc)
        if data_l < rmin or data_l > rmax or math.isnan(data_l):
            new_scan[c] = float('nan')
            continue
        if c == (len(data.ranges)-1):
            break
        if abs(data_l - new_scan[c+1]) < 0.3:
            if temp_i == 0:
                temp_i = c
            continue
        elif temp_i != 0:
            temp_f = c
            if 0.05 < polar_dist(new_scan[temp_i],angle[temp_i],new_scan[temp_f],angle[temp_f]) < 0.15:
                mid = int(math.ceil((temp_f - temp_i)/2)+temp_i)
                if (new_scan[temp_i] - new_scan[mid]) < 0.06 and (new_scan[temp_f] - new_scan[mid]) < 0.06:
                    leg.append([temp_i, temp_f])
                    leg_c += 1
                    ini_angle = round(180/math.pi*(angle[temp_i]),3)
                    fin_angle = round(180/math.pi*(angle[temp_f]),3)
                    print('Leg between {:f} and {:f}'.format(ini_angle, fin_angle))
            else:
                temp_i = 0
                temp_f = 0

    # vector.x = rmax * math.cos(angle[mid])
    # vector.y = rmax * math.sin(angle[mid])
    # vector.z = 1
    #
    # ns_pub.publish(vector)

def listener():
    rospy.Subscriber("/scan", LaserScan, read_cb, queue_size = 1)

    #spin forever
    rospy.spin()

listener()
