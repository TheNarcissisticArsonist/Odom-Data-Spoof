#!/usr/bin/env python

# Modules used for the websocket server
import socket
import wspy

connectionOpened = False # If there's a connection, this will be True
nextMessageToSend = 0

# The websocket server object
class WebSocketServer(wspy.Connection):
	# Run upon opening the connection
	def onopen(self):
		print 'Connection opened at %s:%d' % self.sock.getpeername()
		global connectionOpened, dataFile, nextMessageToSend
		connectionOpened = True
		nextMessageToSend = 0
	# Run upon receiving a message
	def onmessage(self, message):
		print 'Received message "%s"' % message.payload
		global nextMessageToSend
		print nextMessageToSend
		messageDetails = getMessage(nextMessageToSend)
		nextMessageToSend += 1
		stringToSend = messageDetails[0] + "\n\n" + messageDetails[1]
		if message.payload == "ready" and messageDetails[0] != "": # If the webpage is ready, give it data
			self.send(wspy.TextMessage(unicode(stringToSend, "utf-8")))
	# Run upon closing the connection
	def onclose(self, code, reason):
		global connectionOpened
		print 'Connection closed'
		connectionOpened = False

def getMessage(goalMessageNumber):
	dataFile = open("Data.txt", "r")
	currentMessageNumber = 0
	currentOdomMessage = ""
	currentScanMessage = ""
	while currentMessageNumber != goalMessageNumber:
		for i in range(1, 47+1):
			dataFile.readline()
		currentMessageNumber += 1
	for i in range(1, 30+1):
		currentOdomMessage += dataFile.readline()
	currentOdomMessage = currentOdomMessage[:-2]
	dataFile.readline()
	for i in range(32, 46+1):
		currentScanMessage += dataFile.readline()
	currentScanMessage = currentScanMessage[:-2]
	dataFile.readline()
	dataFile.close()
	return [currentOdomMessage, currentScanMessage]

# Start the websocket server on 127.0.0.1:12345 (aka localhost:12345)
server = wspy.websocket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 12345))
server.listen(5)

# Run the websocket server
while True:
	client, addr = server.accept()
	WebSocketServer(client).receive_forever()