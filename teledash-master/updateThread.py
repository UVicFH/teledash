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
        speedAngle = pyqtSignal(int)
        rpm = pyqtSignal(str)
        rpmAngle = pyqtSignal(int)
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
                        rpmdata = message.data[6]<<8 | message.data[7]

			# rpmAngle is what is sent to the UI current which is from -150 to 150 corresponding to 0 to 12000
                        rpmAngledata = rpmdata/52.17 - 115;
                        self.rpm.emit(str(rpmdata))
                        self.rpmAngle.emit(rpmAngledata)

		# the rest of these are strightforward

		elif message.arbitration_id == arbitration_ids.groundspeed:
			self.gear.emit(str(message.data[6]&0b1111)) # gear is a string
                        self.speed.emit(str(message.data[4])) # speed is is a string
                        speedAngledata = (message.data[4])/0.52 - 115;
                        self.speedAngle.emit(speedAngledata)
			self.chargePercent.emit(message.data[5]) # chargePercent is an integer

		elif message.arbitration_id == arbitration_ids.fuel:
			self.fuelPercent.emit(message.data[4]) # fuelPercent is an integer

		elif message.arbitration_id == arbitration_ids.coolant:
			self.statusText.emit(str(int(message.data[6]<<8 | message.data[7])/10) # status text needs to come out as string
