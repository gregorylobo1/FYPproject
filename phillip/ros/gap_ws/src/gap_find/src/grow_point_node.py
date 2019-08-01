#!/usr/bin/env python
# attempts to subscribe and print data from the pointcloud data

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header
import math

global ang_min
global ang_max
global a_inc
radius = 0.55                # swing diameter of 52 cm, with tolerancing of +3cm
rmin = 0.060
rmax = 4

rospy.init_node('gap_find')

ns_pub = rospy.Publisher("new_scan", LaserScan, queue_size = 1)

def read_cb(data):
    global ang_min
    global ang_max
    global a_inc
    global radius
    global rmin
    global rmax

    # reset feature variables
    nan_c = 0
    angle = []

    new_data = data

    # ensure laser variables are up to date
    ang_min = data.angle_min
    ang_max = data.angle_max
    a_inc = data.angle_increment

    # initialise scan data to be mutable object
    scan_d = list(data.ranges)

    # reject invalid data and initialise new data to be published
    for c, data in enumerate(data.ranges):
        angle.append(ang_min + c*a_inc)
        if data < rmin or data > rmax or math.isnan(data):
            scan_d[c] = float('nan')
            nan_c += 1

    scant = tuple(scan_d)
    new_scan = list(scant)
    for i, scan in enumerate(scant):
        if math.isnan(scan):
            continue
        theta = math.atan(0.5*radius/scan)
        devi = int(math.floor(theta/a_inc))
        #print('range=' + str(scan) + ' devi=' + str(devi))
        for x in range(-devi,devi):
            # check if valid value in array
            if (i+x) < 0 or (i+x) > (len(scant) - 1):
                continue
            r_dash = scan/math.cos(x*a_inc)
            #print(math.cos(x*a_inc))
            if (scant[i+x] > r_dash and r_dash < new_scan[i+x]) or math.isnan(scant[i+x]):
                #print('replaced ' + str(scan_d[i+x]) + ' at angle ' + str(angle[i]) + ' with ' + str(r_dash))
                new_scan[i+x] = r_dash
                #print('scan = ' + str(scan_d[i+x]) + ' new = ' + str(r_dash))

    new_data.ranges = new_scan
    ns_pub.publish(new_data)
    print('nans detected = ' + str(nan_c))

def listener():
    rospy.Subscriber("/scan", LaserScan, read_cb, queue_size = 1)

    #spin forever
    rospy.spin()

listener()
