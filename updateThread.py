# import from python library
from random import randint
import time
import math

# import all the neccessary PyQt5 modules - requires PyQt5
from PyQt5.QtCore import QThread, pyqtSignal

# import neccesssary mqtt module - requires paho-mqtt
import paho.mqtt.client as mqtt

# import can - requires python-can
import can

# create a can bus on the can0 interface
# requires interface be set up before opening as detailed here (done on Pi already): http://skpang.co.uk/blog/archives/1220
# you may need to "bring up" the interface first with: sudo /sbin/ip link set can0 up type can bitrate 500000
# ^ not yet tested without doing this - if required will need to be automated
bus=can.interface.Bus(channel='can0', bustype='socketcan_native')

class UpdateThread(QThread):

	# create signals that can be linked to update functions for the UI
	gear = pyqtSignal(str)
	speed = pyqtSignal(str)
	rpm = pyqtSignal(int)
	statusText = pyqtSignal(str)
	statusColor = pyqtSignal(str)
	chargePercent = pyqtSignal(int)
	fuelPercent = pyqtSignal(int)

	def __init__(self,parent=None):

		super(UpdateThread,self).__init__(parent)
		self.exiting = False

	def __del__(self):

		self.wait()

	def stop(self):

		self.exiting = True
		self.terminate()

	def run(self):

		while not self.exiting:

			self.checkForUpdates()

		return

	def checkForUpdates(self):

		# set the statusText to ok and green
		self.statusText.emit(str("OK"))
		self.statusColor.emit(str("#07DD07"))

		# set the fuel and charge to 100%
		self.fuelPercent.emit(int(100))
		self.chargePercent.emit(int(100))

		# recieve a message on the bus and timeout after 1ms (note if it recieves nothign it'll return a message of "none" not sure how to handle that as right now it breaks the code)
		message = bus.recv(1)
		if(message.arbitration_id == 1512):

			# if the id of the message is 1512 it is rpm which is sent as two bits which needs to be combined again after
			rpm = message.data[0]<<8 | message.data[0]

			# rpmAngle is what is sent to the UI current which is from -150 to 150 corresponding to 0 to 12000
			rpmAngle = int(rpm/40.0-150.0)
			self.rpm.emit(rpmAngle)

