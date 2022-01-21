# this is the one you run (scheduling_placement.py is the code it uses)

from csv import reader
import scheduling_placement

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

output_file = r"C:\Work\scheduled_rooms.xlsx"
loser_file = r"C:\Work\losers.xlsx"


room_file = reader(open(room_input_file), delimiter='\t')
course_file = reader(open(course_input_file), delimiter='\t')
preassignment_file = reader(open(preassigned_input_file), delimiter='\t')

scheduling_placement.readRooms(room_file)
scheduling_placement.createPreassigned_Courses(preassignment_file)
scheduling_placement.preassignRooms()
scheduling_placement.createCourses(course_file)
scheduling_placement.scheduleCourses(output_file=output_file, loser_file=loser_file)
