#!/usr/bin/env python
# first test at writing a laserScan to PointCloud2 message

import sensor_msgs.point_cloud2 as pc2
import rospy
from sensor_msgs.msg import PointCloud2, LaserScan
import laser_geometry.laser_geometry as lg

# intialise node
rospy.init_node("laserscan_to_pointcloud")

# simplfy LaserProjection function call
lp = lg.LaserProjection()

# intialise publisher
pc_pub = rospy.Publisher("converted_pc", PointCloud2, queue_size = 1)

def scan_cb(msg):
    # convert message from type LaserScan to PointCloud2
    pc2_msg = lp.projectLaser(msg)

    # now can publish the data
    pc_pub.publish(pc2_msg)

    # convert it to a generator?? (what does this do????)
    point_generator = pc2.read_points(pc2_msg)

# subscribe to the scan data
rospy.Subscriber("/scan", LaserScan, scan_cb, queue_size = 1)
rospy.spin()
