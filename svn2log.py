#!/usr/bin/env python3

import argparse
from datetime import date
import getpass

# guess default time parameter
defaultYear = date.today().year
defaultMonth = date.today().month
defaultMonth -= 1
if defaultMonth == 0:
	defaultMonth = 12
	defaultYear -=1

# command line arguments
parser = argparse.ArgumentParser(description="Converts 'svn log' output to timeSht log file")
parser.add_argument("--input", type=open, default="svn.log", help="Output from 'svn log'")
parser.add_argument("--output", type=argparse.FileType("a"), default="timesht.log", help="timeSht log file")
parser.add_argument("--user", default=getpass.getuser(), help="Your SVN username")
parser.add_argument("--year", type=int, default=defaultYear, help="The year that contains your magic month")
parser.add_argument("--month", type=int, default=defaultMonth, help="The month you are looking for")

args = parser.parse_args()

# read file and parse entries
valid = False
timestamp = ""
messageParts = []
delta = 0

for line in args.input.readlines():
	# next log entry?
	if line.startswith("-------"):
		if valid:
			args.output.write("%s %s\n" % (timestamp, ", ".join(messageParts).rstrip()))
		messageParts = []
		valid = False
		delta = 0

	# parse entry header
	if delta == 1:
		headerParts = line.split(" | ")
		user = headerParts[1]
		time = headerParts[2]
		if user == args.user:
			timeParts = time.split(" ")
			date = timeParts[0]
			clock = timeParts[1]
			dateParts = date.split("-")
			clockParts = clock.split(":")
			year = int(dateParts[0])
			month = int(dateParts[1])
			day = int(dateParts[2])
			hour = int(clockParts[1])
			if (year == args.year) and (month == args.month):
				timestamp = "%i %i" % (day, hour)
				valid = True

	# parse log message
	if delta > 2:
		messageParts.append(line)

	delta += 1

args.input.close()

