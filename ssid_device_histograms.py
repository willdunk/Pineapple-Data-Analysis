#! /usr/bin/env python3


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
	
	print("-" * 80)
	print("SSID POPULATION STATISTICS")
	print("-" * 80)
	
	ssid_population = sorted([len(ssid_devices[ssid]) for ssid in ssid_devices])

	print("SSIDs Detected:       {}".format(len(ssid_population)))
	print("Max Clients Per SSID: {}".format(max(ssid_population)))
	print("50% Clients Per SSID: {}".format(median(ssid_population)))
	print("Min Clients Per SSID: {}".format(min(ssid_population)))
	print("Avg Clients Per SSID: {}".format(average(ssid_population)))
	return


if __name__ == "__main__":
	main()
