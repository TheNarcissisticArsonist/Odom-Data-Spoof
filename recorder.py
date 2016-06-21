#!/usr/bin/env python2

# Modules used for the ROS node
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

# sleep() is a delay function
from time import sleep

lastOdomMessage = "";
lastScanMessage = "";
odomMessageRecorded = True;
scanMessageRecorded = True;
numDataPoints = 0

def odomCallback(data):
	global lastOdomMessage, odomMessageRecorded
	lastOdomMessage = data.__str__()
	odomMessageRecorded = False
def odomListener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/odom", Odometry, odomCallback)

def laserCallback(data):
	global lastScanMessage, scanMessageRecorded
	lastScanMessage = data.__str__()
	scanMessageRecorded = False
def laserListener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/base_scan", LaserScan, laserCallback)

odomListener()
laserListener()

dataFile = open("Data.txt", "w")

try:
	while True:
		if (not odomMessageRecorded) and (not scanMessageRecorded):
			dataFile.write(lastOdomMessage+"\n|\n"+lastScanMessage+"\n\n")
			dataFile.flush()
			odomMessageRecorded = True
			scanMessageRecorded = True
			numDataPoints += 1
			print "%s" % numDataPoints
		sleep(0.1)
except KeyboardInterrupt:
	dataFile.close()