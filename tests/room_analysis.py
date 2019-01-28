from datetime import datetime
import csv


class RoomEvent:
    def __init__(self, room, description, start, end, date, user):
        self.room = room
        self.description = description
        self.start = datetime.strptime(date + " " + start, '%m/%d/%Y %a %I:%M %p')
        self.end = datetime.strptime(date + " " + end, '%m/%d/%Y %a %I:%M %p')
        self.date = date
        self.user = user


def import_data():
    with open(r"C:\work\rooms_310-314.txt", 'r') as input_file:
        reader = csv.reader(input_file, delimiter='\t')
        return [RoomEvent(row[0], row[1], row[2], row[3], row[4], row[5]) for row in reader]


events = import_data()
events.sort(key=lambda i: i.start)

f310_events = [events for events in events if events.room == "F310"]
f314_events = [events for events in events if events.room == "F314"]

conflicts = 0


for i in f314_events:
    for x in f310_events:
        if max(i.start, x.start) < min(i.end, x.end):
            conflicts += 1
            break


print(conflicts)
