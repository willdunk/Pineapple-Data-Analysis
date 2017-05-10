#! /usr/bin/env python3
import plotly.offline as offline
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import plotly.plotly as py
from plotly.graph_objs import *
# import plotly.graph_objs as go
import igraph as ig
import numpy as np

import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import sys

import time
from datetime import datetime
from time import mktime

def average(data):
	return float(sum(data)) / len(data)


def median(data):
	length = len(data)
	if length % 2 == 0:
		lower = length / 2 - 1
		upper = length / 2 + 1
		return average(data[lower:upper])
	else:
		return data[length // 2]


def main():
	ssid_devices = {}
	with open("pineap.log", "r") as handler:
		for line in handler.readlines():
			# tokenize the raw line
			tokens = line.split(",\t")
			# remove the newline from the SSID
			tokens[-1] = tokens[-1][:-1]
			# get individual attributes
			timestamp, request_type, mac_address, ssid = tuple(tokens)
			if ssid not in ssid_devices:
				ssid_devices[ssid] = []
			if mac_address not in ssid_devices[ssid]:
				ssid_devices[ssid].append(mac_address)

	mac_devices = {}
	with open("pineap.log", "r") as handler:
		for line in handler.readlines():
			# tokenize the raw line
			tokens = line.split(",\t")
			# remove the newline from the SSID
			tokens[-1] = tokens[-1][:-1]
			# get individual attributes
			timestamp, request_type, mac_address, ssid = tuple(tokens)
			if mac_address not in mac_devices:
				mac_devices[mac_address] = []
			if ssid not in mac_devices[mac_address]:
				mac_devices[mac_address].append(ssid)

	days = []
	daysmm = []
	di = -1
	with open("pineap.log", "r") as handler:
		for line in handler.readlines():
			# tokenize the raw line
			tokens = line.split(",\t")
			# remove the newline from the SSID
			tokens[-1] = tokens[-1][:-1]
			# get individual attributes
			timestamp, request_type, mac_address, ssid = tuple(tokens)
			timestamp = "2017" + timestamp
			tt = time.strptime(timestamp, "%Y%b  %d %H:%M:%S")
			dt = datetime.fromtimestamp(mktime(tt))
			if((tt.tm_year,tt.tm_mon,tt.tm_mday) in days):
				# our day is already in our set, edit min and max if needed
				timehours = (dt-datetime(1970,1,1)).total_seconds() / 3600.0
				if(timehours < daysmm[di][0]):
					# we need to change our min
					daysmm[di][0] = timehours
				elif(timehours > daysmm[di][1]):
					# we need to change our max
					daysmm[di][1] = timehours
			else:
				# set both min an max (min, max), because the day doesnt exist yet
				days.append((tt.tm_year,tt.tm_mon,tt.tm_mday))
				timehours = (dt-datetime(1970,1,1)).total_seconds() / 3600.0
				daysmm.append([timehours, timehours])
				di= di + 1

	tothours = 0.0
	for day in daysmm:
		tothours = tothours + (day[1] - day[0])

	mac_occurances = {}
	with open("pineap.log", "r") as handler:
		for line in handler.readlines():
			# tokenize the raw line
			tokens = line.split(",\t")
			# remove the newline from the SSID
			tokens[-1] = tokens[-1][:-1]
			# get individual attributes
			timestamp, request_type, mac_address, ssid = tuple(tokens)
			if mac_address not in mac_occurances:
				mac_occurances[mac_address] = 1
			else:
				mac_occurances[mac_address] = mac_occurances[mac_address] + 1

	mac_frequencies = {}
	for mac in mac_occurances:
		mac_frequencies[mac] = mac_occurances[mac]/tothours

	print(tothours)


	init_notebook_mode(connected = False)

	# Number of ssids per device
	reqnums = []
	for lst in mac_devices:
		reqnums.append(len(mac_devices[lst]))

	data = [Histogram(x=reqnums)]
	layout = Layout(title="Histogram of SSIDs/MAC address")
	fig=Figure(data=data, layout=layout)
	offline.plot(fig, filename='ssidspermac.html')
	

	# Number of devices per ssid
	reqnums = []
	for lst in ssid_devices:
		reqnums.append(len(ssid_devices[lst]))
	data = [Histogram(x=reqnums)]
	layout = Layout(title="Histogram of MAC addresses/SSID")
	fig=Figure(data=data, layout=layout)
	offline.plot(fig, filename='macperssid.html')


	# Requests/Hour for each device
	reqnums = []
	for mac in mac_frequencies:
		reqnums.append(mac_frequencies[mac])

	data = [Histogram(x=reqnums)]
	layout = Layout(title="Histogram of Requests/Hour for devices")
	fig=Figure(data=data, layout=layout)
	offline.plot(fig, filename='requestsperhour.html')

	print("-" * 80)
	print("SSID POPULATION STATISTICS")
	print("-" * 80)
	
	ssid_population = sorted([len(ssid_devices[ssid]) for ssid in ssid_devices])

	print("SSIDs Detected:       {}".format(len(ssid_population)))
	print("Max Clients Per SSID: {}".format(max(ssid_population)))
	print("Med Clients Per SSID: {}".format(median(ssid_population)))
	print("Min Clients Per SSID: {}".format(min(ssid_population)))
	print("Avg Clients Per SSID: {}".format(average(ssid_population)))

	print("-" * 80)
	print("STATS WITHOUT 1 CLIENT PER SSID")
	print("-" * 80)

	ssid_population[:] = [x for x in ssid_population if x != 1]

	print("SSIDs Detected:       {}".format(len(ssid_population)))
	print("Max Clients Per SSID: {}".format(max(ssid_population)))
	print("Med Clients Per SSID: {}".format(median(ssid_population)))
	print("Min Clients Per SSID: {}".format(min(ssid_population)))
	print("Avg Clients Per SSID: {}".format(average(ssid_population)))
	return


if __name__ == "__main__":
	main()
