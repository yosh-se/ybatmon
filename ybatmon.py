#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import gtk
import glib
import traceback

class MainApp:
    batteries = {} 
    def __init__(self):
        try:
            self.update()
            glib.timeout_add(5000, self.update)
        except:
            glib.timeout_add(5000, self.update)

    def update(self):
        self.find_batteries()
        try:
            for index, battery in self.batteries.iteritems():
                self.get_battery_info(battery)
                self.get_icon_name(battery)
                battery['icon'].set_from_file(os.path.dirname(os.path.realpath(__file__)) +'/icons/'+ battery['icon_name'] + '.png')
                battery['icon'].set_tooltip_text(battery['tooltip'])
            return True
        except:
            traceback.print_exc(file=sys.stdout)
    '''
    This whole thing is just wrong. Just list the directory and use the filenames instead of iterating.
    '''
    def find_batteries(self):
        batt_no = 0
        new_batteries = {}
        while True:
            try:
                batt_str = "/sys/class/power_supply/BAT"+str(batt_no)+"/"
                fh = open(batt_str+'status', "r")
                fh.close()
                try:
                    new_batteries[batt_no] = {'path': batt_str, 'percentage': '', 'status': '', 'tooltip':'', 'icon': self.batteries[batt_no]['icon'], 'icon_name':''}
                except KeyError:
                    new_batteries[batt_no] = {'path': batt_str, 'percentage': '', 'status': '', 'tooltip':'', 'icon': gtk.StatusIcon(), 'icon_name':''}
                batt_no += 1
            except IOError:
                self.batteries = new_batteries
                return
            except:
                self.batteries = new_batteries
                traceback.print_exc(file=sys.stdout)
                return
            self.batteries = new_batteries
    
    def get_battery_info(self, b):
        try:
            fh = open(b['path']+"status", "r")
            b['status'] = fh.readline().rstrip()
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            status = ""
        try:
            fh = open(b['path']+"capacity", "r")
            b['percentage'] = fh.readline().rstrip()
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            status = ""
        b['tooltip'] = b['status'] +", "+ b['percentage'] + "%"
    
    def get_icon_name(self, b):
        icon=''
        try:
            percentage = int(b['percentage'])
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
                b['icon_name'] = icon
        except:
            icon = 'battery_unknown'
            b['icon_name'] = icon
            traceback.print_exc(file=sys.stdout)
            return
         
        if b['status'] in ('Charging', 'Charged', 'Unknown', 'Full'):
            icon = icon + '_ac'
        b['icon_name'] = icon        
        return
    
if __name__ == "__main__":
    try:
        MainApp()
        gtk.main()
    except KeyboardInterrupt:
        pass
