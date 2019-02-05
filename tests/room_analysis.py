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

f310_events = [e for e in events if e.room == "F310"]
f314_events = [e for e in events if e.room == "F314"]


def find_conflicts(first_room, second_room):
    conflicts = 0
    total_events = 0
    for e1 in first_room:
        total_events += 1
        for e2 in second_room:
            if max(e1.start, e2.start) < min(e1.end, e2.end):
                conflicts += 1
                # print(e1.description + " conflicts with " + e2.description)
                break
    return conflicts


print("F310 events: " + str(len(f310_events)))
print("F314 events: " + str(len(f314_events)))
print(str(find_conflicts(f310_events, f314_events)) + " conflicts found within " + str(len(f310_events)) +
      " total events in F310.")
print(str(find_conflicts(f314_events, f310_events)) + " conflicts found within " + str(len(f314_events)) +
      " total events in F314.")
