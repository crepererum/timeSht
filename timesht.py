#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from datetime import date

# guess default time parameter
defaultYear = date.today().year
defaultMonth = date.today().month
defaultMonth -= 1
if defaultMonth == 0:
	defaultMonth = 12
	defaultYear -=1

class S2LArgparser(ArgumentParser):
	def __init__(self, stuff):
		ArgumentParser.__init__(self, formatter_class=ArgumentDefaultsHelpFormatter, description="Converts " + stuff + " to timeSht log file")


		# command line arguments
		self.add_argument("--output", type=FileType("a"), default="timesht.log", help="timeSht log file")
		self.add_argument("--year", type=int, default=defaultYear, help="The year that contains your magic month")
		self.add_argument("--month", type=int, default=defaultMonth, help="The month you are looking for")


