#!/usr/bin/env python3

import argparse
import email.header
from email.parser import HeaderParser
import email.utils
import getpass
import imaplib
import time

# command line arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Converts imap folder to timeSht log")
parser.add_argument("--output", type=argparse.FileType("a"), default="timesht.log", help="timeSht log file")
parser.add_argument("--server", required=True, help="IMAP server")
parser.add_argument("--user", default=getpass.getuser(), help="IMAP username")
parser.add_argument("--mailboxes", default="Sent", help="IMAP mailboxes (comma seperated list)")
parser.add_argument("--month", type=int, required=True, help="The interesting month")
parser.add_argument("--year", type=int, required=True, help="The year of the interesting month")
parser.add_argument("--sender", default="", help="Comma seperated list of possible senders")
parser.add_argument("--to", default="", help="Comma seperated list of possible recipients")
parser.add_argument("--ssl", type=bool, default=True, help="Use SSL for server connenction")

args = parser.parse_args()

# connect and login
m = None
if args.ssl:
	m = imaplib.IMAP4_SSL(args.server)
else:
	m = imaplib.IMAP4(args.server)
m.login(args.user, getpass.getpass())

# prepare IMAP arguments
isSince = time.strftime("%d-%b-%Y", (args.year,args.month,1,0,0,0,0,0,0))
nextMonth = args.month + 1
nextYear = args.year
if nextMonth > 12:
	nextMonth = 1
	nextYear = nextYear + 1
isBefore = time.strftime("%d-%b-%Y", (nextYear,nextMonth,1,0,0,0,0,0,0))
isFilter = "(SINCE %s BEFORE %s)" % (isSince, isBefore)

# fetch all mailboxs
hp = HeaderParser()
for mailbox in args.mailboxes.split(","):
	m.select("\"%s\"" % mailbox, readonly=True)
	status, data = m.search(None, isFilter)
	if status == "OK":
		# fetch all messages
		for mid in data[0].split():
			status, data = m.fetch(mid, "(BODY[HEADER])")
			if status == "OK":
				# parse message
				raw = data[0][1]
				header = hp.parsestr(raw.decode("utf-8"))
				date = email.utils.parsedate(header["Date"])
				day = date[2]
				hour = date[3]
				messageRaw = email.header.decode_header(header["Subject"])
				message = messageRaw[0][0]
				if type(message) is bytes:
					message = message.decode(messageRaw[0][1])

				# check if message is valid
				valid = True
				if len(args.sender) > 0:
					valid = False
					for sender in args.sender.split(","):
						if not sender in header["From"]:
							valid = True
				if len(args.to) > 0:
					valid = False
					for recipient in args.to.split(","):
						if not recipient in header["To"]:
							valid = True

				# output
				if valid:
					args.output.write("%i %i %s\n" % (day, hour, message))
	m.close()

# exit
m.logout()
args.output.close()
