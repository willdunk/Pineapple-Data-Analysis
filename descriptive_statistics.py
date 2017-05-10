#! /usr/bin/env python3


import sys


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
	requests = 0
	devices  = []
	networks = []

	request_types = {}

	with open(sys.argv[1], "r") as handler:
		for line in handler.readlines():
			# tokenize the raw line
			tokens = line.split(",\t")
			# remove the newline from the SSID
			tokens[-1] = tokens[-1][:-1]
			# get individual attributes
			timestamp, request_type, mac_address, ssid = tuple(tokens)

			requests += 1
			if mac_address not in devices:
				devices.append(mac_address)
			if ssid not in networks:
				networks.append(ssid)
			if request_type not in request_types:
				request_types[request_type] = 0
			request_types[request_type] += 1

	print("FILE: {}".format(sys.argv[1]))
	
	print("-" * 80)

	print("# REQUESTS: {}".format(requests))
	print("# NETWORKS: {}".format(len(networks)))
	print("# DEVICES:  {}".format(len(devices)))

	print("-" * 80)

	for request_type, count in request_types.items():
		print("# {}: {}".format(request_type, count))

	return


if __name__ == "__main__":
	main()
