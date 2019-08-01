#!/usr/bin/env python
# attempts to subscribe and print data from the pointcloud data

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header
import math

global ang_min
global ang_max
global a_inc
radius = 0.55                # swing radius of 52 cm, with tolerancing of +3cm
con_dist = 0.15              # connectivity test
feat = 1
fea_no = []
angle = []
rmin = 0.060
rmax = 4

rospy.init_node('sub_reader')

ns_pub = rospy.Publisher("new_scan", LaserScan, queue_size = 1)

def polar_dist(r1, a1, r2, a2):
    global ang_min
    global a_inc

    th1 = ang_min + a1*a_inc
    th2 = ang_min + a2*a_inc
    dist = math.sqrt(r1*r1 + r2*r2 - 2*r1*r2*math.cos(th1 - th2))
    return dist

def read_cb(data):
    global ang_min
    global ang_max
    global a_inc
    global radius
    global fea_no
    global feat
    global angle
    global rmin
    global rmax

    # reset feature variables
    nan_c = 0
    n_z = 0
    feat = 1
    fea_no = []
    angle = []

    # ensure laser variables are up to date
    ang_min = data.angle_min
    ang_max = data.angle_max
    a_inc = data.angle_increment

    print(str(rmax))
    # initialise scan data to be mutable object
    scan_d = list(data.ranges)

    # reject invalid data and initialise new data to be published
    for c, data in enumerate(data.ranges):
        angle.append(ang_min + a_inc*c)
        if data < rmin or data > rmax or math.isnan(data):
            scan_d[c] = float('nan')
            nan_c += 1
        elif n_z == 0:
            n_z = 1
            print('first data at ' + str(angle[c]) + ' index = ' + str(c))

    for i, scan in enumerate(scan_d):
        dist = 0

        if math.isnan(scan) or i == (len(scan_d) - 1):
            fea_no.append(float('nan'))
            continue
        for x in range(1,len(scan_d) - i):
            if math.isnan(scan_d[i+x]):
                continue
            else:
                dist = polar_dist(scan, i, scan_d[i+x], i+x)
                fea_no.append(feat)
                if dist > con_dist:
                    print('i = ' + str(i) + ' x = ' + str(x) + ' dist = ' + str(dist))
                    feat += 1
                break

    print(str(feat))
    print(str(fea_no))
    print('nans detected = ' + str(nan_c))
    print(len(scan_d))

def listener():
    rospy.Subscriber("/scan", LaserScan, read_cb, queue_size = 1)

    #spin forever
    rospy.spin()

listener()
