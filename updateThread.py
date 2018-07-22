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

# import class to interface with mqtt
from mosquitto_sender import Mosquitto_Sender

# create a can bus on the can0 interface
# requires interface be set up before opening as detailed here (done on Pi already): http://skpang.co.uk/blog/archives/1220
# you may need to "bring up" the interface first with: sudo /sbin/ip link set can0 up type can bitrate 500000
# ^ not yet tested without doing this - if required will need to be automated
import os
bus=can.interface.Bus(channel='can0', bustype='socketcan_native')

import arbitration_ids
from toggleable_warnings import *

MSTIMEOUT = 100 # in milliseconds
WARNING_DISPLAY_DURATION = 0.75 # in seconds, as most things in this app
WARNINGS_DEMO = False

import random as rn # for the purposes of the warning demo

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

		self.timeout_warning = Toggleable_warning("Timed out", "T/O")
		self.warnings = [self.timeout_warning]
		self.current_warning = None

		self.sender = Mosquitto_Sender()
		self.sender.connect("192.168.1.221")
		self.sender.start_handler()

		if WARNINGS_DEMO:
			# this block for warning demo stuff
			example_texts = ["COLD", "HOT", "FUEL", "CHRG", "OOPS", "LEAN", "OUCH", "RICH", "SIN", "COS"]
			self.example_warnings = [Toggleable_warning("Example warning %d" % n, example_texts[n]) for n in range(10)]
			self.demo_interval = 5
			self.demo_altered = time.time()
			self.warnings += self.example_warnings

	

	def __del__(self):

		self.wait()

	def stop(self):

		self.exiting = True
		self.terminate()

	def run(self):

		while not self.exiting:

			self.checkForUpdates()

		return


	def set_status_colour(self, status):
		if status.upper() == "OK":
			self.statusColor.emit(str("#07DD07")) # green
		elif status.upper() == "TIMED OUT":
			self.statusColor.emit(str("#880707")) # red
		elif status.upper() == "WARNING":
			self.statusColor.emit(str("#DD6607")) # orange
		else:
			raise Error("Unrecognized status colour: %s" % status)


	def active_warnings(self):
		"""Returns a list of the active warnings, sorted in order of last time displayed"""
		return sorted([wn for wn in self.warnings if wn.on], key=lambda wn: wn.last_focused)


	def wfocus(self, warning):
		"""Switches the currently displayed warning"""
		self.current_warning = warning
		if not warning is None:
			self.statusText.emit(warning.code)
			warning.mark_focused()


	def display_status(self):
		"""Displays the least recently displayed active warning.

		Returns warning displayed, or None"""

		active_warnings = self.active_warnings()

		if active_warnings == []: # status is OK
			self.statusText.emit(str("OK"))
			self.set_status_colour("OK")
			self.wfocus(None) # make sure we know we're not displaying a warning
			return None

		elif self.timeout_warning:
			self.set_status_colour("TIMED OUT")

		else:
			self.set_status_colour("WARNING")

		
		last_warning = active_warnings[-1] # the least recently focused active warning

		if len(active_warnings) == 1:

			if not self.current_warning is last_warning:
				# That means we are switching to this warning for some reason
				self.wfocus(last_warning)
			else:
				# This is the only warning and we continue to display it
				last_warning.mark_seen()

			return last_warning

		elif last_warning.last_seen - last_warning.last_focused <= WARNING_DISPLAY_DURATION:
			# continue displaying last warning
			last_warning.mark_seen()
			return last_warning

		else: # switch it up
			warning = active_warnings[0]
			self.wfocus(warning)
			return warning


	def checkForUpdates(self):

		# see if the server is connected and if not retry
		#if(self.sender.connection_success == False):
		#	self.sender.retry_connect()
		
		# recieve a message on the bus and timeout after MSTIMEOUT ms, in which case the gui will show a timeout
		message = bus.recv(MSTIMEOUT/1000)

		if message is None: # bus timed out
			# set the statusText to TIMED OUT and red
			self.timeout_warning.switch_on()
			self.display_status()
			return None
		else:
			self.timeout_warning.switch_off()
		
		# Commented out to display coolant temperature in the warning zone.
		# self.display_status()

		
		if WARNINGS_DEMO:
			# demo the warning system:
			aw = self.active_warnings()
			#if aw != []: timer = time.time() - aw[-1].last_focused
			#else: timer = None
			#print("Warnings: %s Timer?: %s" % (aw, timer))
			if time.time() - self.demo_altered > self.demo_interval:
				self.example_warnings[rn.randint(0,9)].toggle()
				self.demo_altered = time.time()
				self.demo_interval = rn.uniform(3,10)
				if rn.uniform(0,1) < 0.333:
					for warning in self.example_warnings:
						warning.switch_off()

		if message.arbitration_id == arbitration_ids.rpm:

			# rpm is sent as two bits which needs to be combined again after
			rpm = int(message.data[6]<<8 | message.data[7])
			self.sender.send("hybrid/dash/rpm", str(time.time()) + ":" + str(rpm))

			# rpmAngle is what is sent to the UI current which is from -150 to 150 corresponding to 0 to 12000
			rpmAngle = rpm/40.0-150.0
			self.rpm.emit(rpmAngle)

			# pulse width is the the next two bits / 1000
			pw = str(int(message.data[2]<<8 | message.data[3])/1000.0)
			self.sender.send("hybrid/engine/pw", str(time.time()) + ":" + str(pw))

		elif message.arbitration_id == arbitration_ids.groundspeed:

			powersplit = str(message.data[0])
			self.sender.send("hybrid/dash/powersplit", str(time.time()) + ":" + str(powersplit))
			
			gear = str(message.data[6]&0b1111)
			self.gear.emit(gear) # gear is a string
			self.sender.send("hybrid/dash/gear", str(time.time()) + ":" + str(gear))

			speed = str(message.data[4])
			self.speed.emit(speed) # speed is is a string
			self.sender.send("hybrid/dash/speed", str(time.time()) + ":" + str(speed))

			chargePercent = message.data[5]
			self.chargePercent.emit(chargePercent) # chargePercent is an integer
			self.sender.send("hybrid/dash/charge", str(time.time()) + ":" + str(chargePercent))

		elif message.arbitration_id == arbitration_ids.fuel:

			fuelPercent = int(message.data[4])
			self.fuelPercent.emit(fuelPercent) # fuelPercent is an integer
			self.sender.send("hybrid/engine/fuel", str(time.time()) + ":" + str(fuelPercent))

		elif message.arbitration_id == arbitration_ids.coolant:

			coolantTemp = str(int(message.data[6]<<8 | message.data[7])/10.0)
			self.statusText.emit(coolantTemp) # status text needs to come out as strin
			self.sender.send("hybrid/engine/temperature", str(time.time()) + ":" + str(coolantTemp))

			MAT = str(int(message.data[4]<<8 | message.data[5])/10.0)
			self.sender.send("hybrid/engine/MAT", str(time.time()) + ":" + str(MAT))

		elif message.arbitration_id == arbitration_ids.vehicle_slow:

			# Send the throttle driver input
			driverThrottle = int(message.data[2])
			self.sender.send("hybrid/driverinputs/throttle", str(time.time()) + ":" + str(driverThrottle))

			# Send the brake driver input
			driverBrake = int(message.data[3])
			self.sender.send("hybrid/driverinputs/brake", str(time.time()) + ":" + str(driverBrake))

		elif message.arbitration_id == arbitration_ids.tps:

			# Send the throttle position
			TPS = str(int(message.data[0]<<8 | message.data[1])/10.0)
			self.sender.send("hybrid/engine/TPS", str(time.time()) + ":" + str(TPS))

			# Send the AFR
			AFR = int(message.data[4]<<8 | message.data[5])/10.0
			self.sender.send("hybrid/engine/AFR", str(time.time()) + ":" + str(AFR))

			# Send the battery voltage
			GLVolts = int(message.data[2]<<8 | message.data[3])/10.0
			self.sender.send("hybrid/dash/GLVoltage", str(time.time()) + ":" + str(GLVolts))

		elif message.arbitration_id == arbitration_ids.advance:

			# Send the spark advance
			spkadv = str(int(message.data[0]<<8 | message.data[1])/10.0)
			self.sender.send("hybrid/engine/spkadv", str(time.time()) + ":" + str(spkadv))

			# Send the target AFR
			AFRtgt = int(message.data[4])/10.0
			self.sender.send("hybrid/engine/AFRtgt", str(time.time()) + ":" + str(AFRtgt))

		elif message.arbitration_id == arbitration_ids.ams1:

			voltage = int(message.data[0] << 8 | message.data[1])/100.0
			self.sender.send("hybrid/ams/voltage", str(time.time()) + ":" + str(voltage))

			current1 = message.data[6]
			current2 = message.data[7]
			self.sender.send("hybrid/ams/current", str(time.time()) + ": byte1 - " + "{0:b}".format(current1) + "byte 2 - " + "{0:b}".format(current2))

			ams_status = int(message.data[4] & 0b00000010 >> 1)
			self.sender.send("hybrid/ams/ams_status", str(time.time()) + ":" + str(ams_status))

			regen_status = int(message.data[4] & 0b00000001)
			self.sender.send("hybrid/ams/regen_status", str(time.time()) + ":" + str(regen_status))

		elif message.arbitration_id == arbitration_ids.ams2:

			max_cell_num = int(message.data[0])
			self.sender.send("hybrid/ams/max_cell_num", str(time.time()) + ":" + str(max_cell_num))

			max_cell_volts = int(message.data[1] << 8 | message.data[2])/1000.0
			self.sender.send("hybrid/ams/max_cell_volts", str(time.time()) + ":" + str(max_cell_volts))

			min_cell_num = int(message.data[3])
			self.sender.send("hybrid/ams/min_cell_num", str(time.time()) + ":" + str(min_cell_num))

			min_cell_volts = int(message.data[4] << 8 | message.data[5])/1000.0
			self.sender.send("hybrid/ams/min_cell_volts", str(time.time()) + ":" + str(min_cell_volts))
