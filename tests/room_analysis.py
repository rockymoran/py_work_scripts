from datetime import datetime
from collections import namedtuple
import csv

# Range = namedtuple('Range', ['start', 'end'])
#
# r1 = Range(start=datetime(2012, 1, 15), end=datetime(2012, 5, 10))
# r2 = Range(start=datetime(2012, 3, 20), end=datetime(2012, 9, 15))
# latest_start = max(r1.start, r2.start)
# earliest_end = min(r1.end, r2.end)
# delta = (earliest_end - latest_start).days + 1
# overlap = max(0, delta)
# print(overlap)

# file format (tab delimited)
# room, event, start, end, date, user

with open(r"C:\work\rooms_310-314.txt") as csvfile:
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        converted_stime = datetime.strptime(row[4] + " " + row[2], '%m/%d/%Y %a %I:%M %p')
        converted_etime = datetime.strptime(row[4] + " " + row[3], '%m/%d/%Y %a %I:%M %p')

        print(str(converted_stime) + " - " + str(converted_etime))
