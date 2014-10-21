#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import gtk
import glib

class MainApp:
	def __init__(self):
		try:
			self.icon = gtk.StatusIcon()
			self.update_icon()
			glib.timeout_add(1100, self.update_icon)
		except:
			glib.timeout_add(1100, self.update_icon)
	
	def get_battery_info(self):
			try:
				fh = open("/sys/class/power_supply/BAT0/capacity", "r")
				level = fh.readline().rstrip()
				fh.close()
			except:
				e = sys.exc_info()[0]
				print(e)
				level = ""
			try:
				fh = open("/sys/class/power_supply/BAT0/status", "r")
				status = fh.readline().rstrip()
				fh.close()
			except:
				e = sys.exc_info()[0]
				print(e)
				status = ""

			return { 'state':status, 'percentage':level,	'tooltip': status+", "+level+"%" }
	
	def get_icon_name(self, state, percentage):
		icon=''
		if percentage < 10:
			icon = 'battery_10'
		elif percentage < 20:
		  icon = 'battery_20'
		elif percentage < 50:
			icon = 'battery_50'
		elif percentage < 75:
			icon = 'battery_75'
		elif percentage < 101:
			icon = 'battery_100'
		else:
			icon = 'battery_unknown'

		if state in ('Charging', 'Charged', 'Unknown', 'Full'):
			icon = icon + '_ac'
		return icon
	
	def update_icon(self):
		info = self.get_battery_info()
		icon_name = self.get_icon_name(info['state'],int(info['percentage']))
		self.icon.set_from_file(os.path.dirname(os.path.realpath(__file__)) +'/icons/'+ icon_name + '.png')
		self.icon.set_tooltip_text(info['tooltip'])
		return True

if __name__ == "__main__":
	try:
		MainApp()
		gtk.main()
	except KeyboardInterrupt:
		pass
