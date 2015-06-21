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
			self.icona = gtk.StatusIcon()
			self.update_icon()
			glib.timeout_add(1100, self.update_icon)
		except:
			glib.timeout_add(1100, self.update_icon)
	
	def get_battery_info(self, battery = 0):
			try:
				fh = open("/sys/class/power_supply/BAT"+str(battery)+"/capacity", "r")
				level = fh.readline().rstrip()
				fh.close()
			except:
				e = sys.exc_info()[0]
				print(e)
				level = ""
			try:
				fh = open("/sys/class/power_supply/BAT"+str(battery)+"/status", "r")
				status = fh.readline().rstrip()
				fh.close()
			except:
				e = sys.exc_info()[0]
				print(e)
				status = ""

			return { 'state':status, 'percentage':level,	'tooltip': status+", "+level+"%" }
	
	def get_icon_name(self, state, percentage_s):
		icon=''
		try:
			percentage = int(percentage_s)
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
				return icon
		except:
			icon = 'battery_unknown'
			return icon

		if state in ('Charging', 'Charged', 'Unknown', 'Full'):
			icon = icon + '_ac'
		return icon
	
	def update_icon(self):
		info = self.get_battery_info()
		infoa = self.get_battery_info(1)
		icon_name = self.get_icon_name(info['state'],info['percentage'])
		icon_namea = self.get_icon_name(infoa['state'],infoa['percentage'])
		self.icona.set_from_file(os.path.dirname(os.path.realpath(__file__)) +'/icons/'+ icon_name + '.png')
		self.icona.set_tooltip_text(infoa['tooltip'])
		self.icon.set_from_file(os.path.dirname(os.path.realpath(__file__)) +'/icons/'+ icon_name + '.png')
		self.icon.set_tooltip_text(info['tooltip'])
		return True

if __name__ == "__main__":
	try:
		MainApp()
		gtk.main()
	except KeyboardInterrupt:
		pass

