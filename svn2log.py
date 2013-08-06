#!/usr/bin/env python3

import argparse
import getpass
import timesht

# command line arguments
parser = timesht.S2LArgparser("'svn log' output")
parser.add_argument("--input", type=open, default="svn.log", help="Output from 'svn log'")
parser.add_argument("--user", default=getpass.getuser(), help="Your SVN username")

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
			args.output.write("%s %s\n" % (timestamp, ", ".join(messageParts)))
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
			hour = int(clockParts[0])
			if (year == args.year) and (month == args.month):
				timestamp = "%i %i" % (day, hour)
				valid = True

	# parse log message
	if (delta > 2) and (len(line.rstrip()) > 0):
		messageParts.append(line.rstrip())

	delta += 1

args.input.close()
args.output.close()

