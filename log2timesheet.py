#!/usr/bin/env python3

import argparse
from collections import OrderedDict
import random

# command line arguments
parser = argparse.ArgumentParser(description="Converts merged log to time sheet")
parser.add_argument("--input", type=open, default="timesht.log", help="Merged log file")
parser.add_argument("--days", type=int, default=31, help="Number of days of this month")
parser.add_argument("--total", type=int, default=40, help="Wanted number of total hours per month")

args = parser.parse_args()

# parse log file
log = OrderedDict()
for line in args.input:
	parts = line.split(" ")
	if len(parts) > 2:
		day = int(parts[0])
		time = int(parts[1])
		timestamp = (day - 1) * 24 + time
		message = " ".join(parts[2:]).rstrip()
		log[timestamp] = message

args.input.close()


# boostrap
free = []
for t in range(0, 31 * 24):
	if (not t in log) and ((t + 1) in log):
		free.append(t)

random.shuffle(free)

# allocate remaning hours
while len(log) < args.total:
	t = free.pop()
	log[t] = log[t + 1]
	if (not (t - 1) in log) and (t > 0):
		free.append(t - 1)
		random.shuffle(free)

# output
total = 0
for day in range(0, args.days):
	entries = set()
	hours = 0

	for t in range(day * 24, (day + 1) * 24):
		if t in log:
			entries.add(log[t])
			hours += 1

	if len(entries) > 0:
		print("%i: %ih - %s" % (day + 1, hours, ", ".join(entries)))

	total += hours

print("total: %ih" % total)

