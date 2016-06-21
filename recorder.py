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
	odomMessageRecorded = False # This is a new message, so it hasn't been recorded yet
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

dataFile = open("Data.txt", "w") # Open the text file in write mode. This will erase the last data set

try:
	while True:
		if (not odomMessageRecorded) and (not scanMessageRecorded): # If both the odom and scan haven't been recorded, record them
			messageBeingWritten = lastOdomMessage+"\n\n"+lastScanMessage+"\n|\n"
			dataFile.write(messageBeingWritten)
			dataFile.flush()
			odomMessageRecorded = True
			scanMessageRecorded = True
			numDataPoints += 1
			print "%s" % numDataPoints
		sleep(0.1)
except KeyboardInterrupt:
	dataFile.close()