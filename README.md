timeSht
=======

You know how many hours you worked last month but forgot to write a time sheet? So here is a small collection of scripts who collect information from different sources and guess the original time sheet.

Usage
-----
Use the `SOURCE2log` scripts to generate a log file or add you own entries to it. After it, run the `log2timesheet` script to get your personal time sheet.

Requirements
------------
[Python3](http://www.python.org) and a terminal. I've tested it using version 3.3 but it may also run with others.

Log Format
----------
A log file contains multiple, non sorted lines of the following structure:

    DAY HOUR a short message describing your work

Do not use multiple spaces to seperate words, day and hour. The range of days is 1-28/29/30/31, the range of hours is 1-24. When collecting entries, put them into the hour you finish the described task. For the visual thinkers, here is an example:

    10 8 preparing coffee
    11 8 preparing better coffee
    10 12 ask Frank to make me a coffee
    10 13 ask Elena to make me a coffee
    11 7 initial checkout
    12 23 still searching for another job

