#!/usr/bin/env python3

import argparse
from calendar import monthrange
from collections import OrderedDict
from datetime import date
import random
import timesht

# constants
WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# command line arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Converts merged log to time sheet")
parser.add_argument("--input", type=open, default="timesht.log", help="Merged log file")
parser.add_argument("--total", type=int, default=40, help="Wanted number of total hours per month")
parser.add_argument("--maxPerDay", type=int, default=8, help="Maximum working hours per day")
parser.add_argument("--year", type=int, default=timesht.defaultYear, help="Year of the timesheet (used to calculate the day of the week)")
parser.add_argument("--month", type=int, default=timesht.defaultMonth, help="Month of the timesheet (used to calculate the day of the week)")

args = parser.parse_args()

# fix up some date stuff
days = monthrange(args.year, args.month)[1]

# parse log file
log = OrderedDict()
totalDay = [0] * days
for line in args.input:
	parts = line.split(" ")
	if len(parts) > 2:
		day = int(parts[0])
		time = int(parts[1])
		timestamp = (day - 1) * 24 + time
		message = " ".join(parts[2:]).rstrip()

		if totalDay[day - 1] < args.maxPerDay:
			log[timestamp] = message
			totalDay[day - 1] += 1

args.input.close()


# boostrap
free = []
for t in range(0, 31 * 24):
	if (not t in log) and ((t + 1) in log):
		free.append(t)

random.shuffle(free)

# allocate remaning hours
while (len(log) < args.total) and (len(free) > 0):
	t = free.pop()
	d = int(t / 24)
	source = t + 1

	while (totalDay[d] >= args.maxPerDay) or (t in log):
		t -= 1
		d = int(t / 24)

	log[t] = log[source]
	totalDay[d] += 1

	if (not (t - 1) in log) and (t > 0):
		free.append(t - 1)
		random.shuffle(free)

# output
total = 0
for day in range(0, days):
	entries = set()
	hours = 0
	dayOfTheWeek = ""
	dayOfTheWeek = WEEK[date(args.year, args.month, day + 1).weekday()]

	for t in range(day * 24, (day + 1) * 24):
		if t in log:
			entries.add(log[t])
			hours += 1

	if len(entries) > 0:
		print("%i (%s): %ih - %s" % (day + 1, dayOfTheWeek, hours, ", ".join(entries)))

	total += hours

print("total: %ih" % total)

