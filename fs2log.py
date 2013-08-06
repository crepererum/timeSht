#!/usr/bin/env python3

import argparse
import os
import subprocess
import timesht
import time

# command line arguments
parser = timesht.S2LArgparser("file system activities")
parser.add_argument("--path", required=True, help="Path that should be scanned")
parser.add_argument("--suffixes", default="", help="Legal file suffixes, comma seperated list")
parser.add_argument("--exiftool", action="store_true", help="Use exiftool to extract metadata from files")

args = parser.parse_args()

# prepare scan
timeMin = time.mktime((args.year,args.month,1,0,0,0,0,0,0))
nextMonth = args.month + 1
nextYear = args.year
if nextMonth > 12:
	nextMonth = 1
	nextYear = nextYear + 1
timeMax = time.mktime((nextYear,nextMonth,1,0,0,0,0,0,0))

# scan
for root, dirs, files in os.walk(args.path):
	# check all files
	for file in files:
		# check if file is valid (name)
		valid = True
		if len(args.suffixes) > 0:
			valid = False
			for suffix in args.suffixes.split(","):
				if file.endswith(suffix):
					valid = True

		# get file metadata #1
		if valid:
			path = "%s/%s" % (root, file)
			stat = os.stat(path)
			ftime = None

			# next check (time)
			valid = False
			if timeMin <= stat.st_atime < timeMax:
				valid = True
				ftime = stat.st_atime

			if timeMin <= stat.st_mtime < timeMax:
				valid = True
				ftime = stat.st_mtime

			if valid:
				lt = time.localtime(ftime)
				day = lt.tm_mday
				hour = lt.tm_hour
				message = file

				# get file metadata #2
				if args.exiftool:
					title = subprocess.check_output(["exiftool", "-m", "-p", "$Title", path]).rstrip()
					if len(title) > 0:
						message = str(title, "utf-8")

				args.output.write("%i %i %s\n" % (day, hour, message))

# clean up
args.output.close()

