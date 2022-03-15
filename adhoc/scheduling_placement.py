# this is the background code for run_scheduler.py
# this file is only ran directly for testing purposes

# trying to recreate the algorithm you wrote on 3/11/21 and somehow didn't save. way to go lmao
# need to figure out how you implemented the regex into it
# places courses into rooms based on requested day/time/capacity
# takes 3 separate files (rooms.csv, course.csv, filled_rooms.csv)

from csv import reader
import re
import pandas as pd


# regex to convert normal day time to array of bins (e.g., TTh 11:00AM-12:30PM to [36, 37, 38, 94, 95, 96])
def convertTime(code):
    # regex variables for converting day time into bins for placement
    pattern = r"([SMTWFhu]*)\s*(\d*):(\d*)([AP]M)-(\d*):(\d*)([AP]M)"
    dayorder = ["M", "T", "W", "Th", "F", "S", "Su"]

    m = re.match(pattern, code.strip())
    days, starthh, startmm, startampm, endhh, endmm, endampm = m.groups()
    starthh, startmm, endhh, endmm = (int(k) for k in (starthh, startmm, endhh, endmm))

    if startampm == 'PM' and starthh != 12:
        starthh += 12
    if endampm == 'PM' and endhh != 12:
        endhh += 12

    starthh = (starthh - 8) * 2 + startmm//30
    endhh = (endhh - 8) * 2 + endmm//30

    slots = []
    for day in re.findall("[A-Z][hu]?", days):
        offset = dayorder.index(day) * 29 + 1
        slots.extend([offset+k for k in range(starthh, endhh)])

    return slots


class Room(object):
    room_instances = []  # list of all Room objects that have been created

    def __init__(self, name, capacity):
        self.bin_times = []
        self.bin_times.extend(range(1, 204))
        self.name = name
        self.capacity = capacity
        Room.room_instances.append(self)  # adding this to list of Room objects that have been created


class Course(object):
    course_instances = []  # list of all Course objects that have been created

    def __init__(self, name, readable_days, readable_times, need_room):
        self.name = name
        self.readable_days = readable_days
        self.readable_times = readable_times
        self.bin_times = []
        self.capacity = int
        self.need_room = need_room
        self.preassigned_room = ""
        self.assigned_room = False
        Course.course_instances.append(self)  # adding this to list of Course objects that have been created


# iterate through room file and create a room object for each room (consisting of room name and capacity)
def readRooms(room_file, verbose=False):
    for name, cap in room_file:
        x = Room(name, cap)
        if verbose:
            print("%s created" % x.name)


# create course records for each preassigned course
def createPreassigned_Courses(preassignment_file, verbose=False):
    for name, days, times, preassigned_room in preassignment_file:
        x = Course(name, days, times, need_room=False)
        x.preassigned_room = preassigned_room
        day_times = days + " " + times
        try:
            x.bin_times = convertTime(day_times)
        except AttributeError:
            if verbose:
                print("Error parsing %s." % x.name)


# remove day/time bin sets from preassigned course rooms
def preassignRooms(verbose=False):
    for course in Course.course_instances:
        if not course.need_room:
            for room in Room.room_instances:
                if course.preassigned_room == room.name:
                    for x in course.bin_times:
                        try:
                            room.bin_times.remove(x)
                        except ValueError:
                            if verbose:
                                print("%s error removing bin %s: Already removed." % (course.name, x))
                    if verbose:
                        print("Removed: %s %s %s %s" % (course.name, course.readable_days, course.readable_times,
                                                        course.preassigned_room))
                    break


# iterate through course file and create a course object for each course (consisting of ccn, times (as list of bins),
# capacity)
def createCourses(course_file, verbose=False):
    for name, days, times, cap in course_file:
        x = Course(name, days, times, need_room=True)
        x.capacity = cap
        day_times = days + " " + times
        try:
            x.bin_times = convertTime(day_times)
        except AttributeError:
            if verbose:
                print("Error parsing %s." % x.name)


# iterate through course list and compare course times to available room times. if room times are available,
# see if course fits in the room, if so, assign course to room and remove times as "available"
def scheduleCourses(verbose=False, output_file=False, loser_file=False):
    assigned = 0
    unassigned = 0
    for course in Course.course_instances:
        if course.need_room:
            for room in Room.room_instances:
                if set(course.bin_times).issubset(room.bin_times):
                    if int(room.capacity) >= int(course.capacity):
                        for x in course.bin_times:
                            room.bin_times.remove(x)
                        if verbose:
                            print("Assigned: %s %s %s %s" % (course.name, course.readable_days, course.readable_times,
                                                             room.name))
                        course.assigned_room = room.name
                        assigned += 1
                        break
    unassigned = (sum(1 for course in Course.course_instances if course.need_room))
    results = []
    losers = []
    columns = ['Schedule_ID', 'Days', 'Start Time', 'End Time', 'Room']
    for course in Course.course_instances:
        if course.assigned_room:
            results.append(
                {
                    'Schedule_ID': course.name,
                    'Days': course.readable_days,
                    'Times': course.readable_times,
                    'Room': course.assigned_room
                }
            )
        elif not course.assigned_room and course.need_room:
            losers.append(
                {
                    'Schedule_ID': course.name,
                    'Days': course.readable_days,
                    'Times': course.readable_times,
                    'Room': course.assigned_room
                }
            )
    df = pd.DataFrame(results)
    df[["Start Time", "End Time"]] = df["Times"].str.split("-", n=1, expand=True)
    loser_df = pd.DataFrame(losers)
    loser_df[["Start Time", "End Time"]] = loser_df["Times"].str.split("-", n=1, expand=True)

    if output_file:
        df[columns].to_excel(output_file)
    if loser_file:
        loser_df[columns].to_excel(loser_file)
    else:
        print(df[columns])
    print("Process complete. %s courses processsed. %s courses assigned. %s remain unassigned." % (unassigned,
                                                                                                   assigned,
                                                                                                   unassigned-assigned))


# this is only ran for testing. actual file is run_scheduler.py
# set test file variables here to see what is and isn't working.
if __name__ == "__main__":

    tests = """\
        TTh   11:00AM-12:30PM
        TTh   12:30PM-2:00PM
        MW   4:00PM-5:30PM
        TTh   6:00PM-7:30PM
        MW   12:30PM-2:00PM
        M   12:00PM-2:00PM""".splitlines()

    for test in tests:
        print(test.strip(), convertTime(test))

    # tab delimited room file (rooms.csv)
    # c132     12
    # c335     28
    room_input_file = r"C:\Work\rooms.csv"

    # tab delimited file with courses that need placement (course.csv)
    # unique course id, day, time (start and end, dash separated), course-capacity
    # 00001   MW 8:00am-9:30AM    71
    # 00002   MW 8:00am-9:30AM    41
    # 00003   MW 8:00am-9:30AM    31
    course_input_file = r"C:\Work\course.csv"

    # tab delimited pre-assigned course file (filled_rooms.csv)
    # unique course id, day, time (start and end, dash separated), room
    # 00004   MW 8:00am-9:30AM    N100
    # 00005   MW 8:00am-9:30AM    C330
    # 00006   MW 8:00am-9:30AM    C210
    preassigned_input_file = r"C:\Work\filled_rooms.csv"

    room_file = reader(open(room_input_file), delimiter='\t')
    course_file = reader(open(course_input_file), delimiter='\t')
    preassignment_file = reader(open(preassigned_input_file), delimiter='\t')

    readRooms(room_file, verbose=True)
    createPreassigned_Courses(preassignment_file, verbose=True)
    preassignRooms(verbose=True)
    createCourses(course_file, verbose=True)
    scheduleCourses(verbose=True)
