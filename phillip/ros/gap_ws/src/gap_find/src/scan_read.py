#!/usr/bin/env python
# attempts to subscribe and print data from the pointcloud data
''' last editted on 31/05/2019
by Phillip Luu '''
import rospy
from sensor_msgs.msg import LaserScan
import math

rospy.init_node('scan_read')

ns_pub = rospy.Publisher("new_scan", LaserScan, queue_size = 1)

def read_cb(data):
    # reset feature variables
    angle = []
    rmin = 0.060
    rmax = 2.5

    # new data that is shortened
    newdata = data

    # ensure laser variables are up to date
    ang_min = data.angle_min
    ang_max = data.angle_max
    a_inc = data.angle_increment

    scan = list(data.ranges)
    # reject invalid data and initialise new data to be published
    for c, _data_ in enumerate(data.ranges):
        if _data_ < rmin or _data_ > rmax or math.isnan(_data_):
            scan[c] = float('nan')
        else:
            scan[c] = round(_data_,10)
        # angle_d = round(180/math.pi*(ang_min + c*a_inc),3)
        angle_d = round((ang_min + c*a_inc),5)
        angle.append((angle_d,scan[c]))
    print('new data = ' + str(angle))

    newdata.ranges = list(scan)
    ns_pub.publish(newdata)

def listener():
    rospy.Subscriber("/scan", LaserScan, read_cb, queue_size = 1)

    #spin forever
    rospy.spin()

listener()
