from bst import Node
import json
import timeit

# Data from the DB
leaderScheduleFile = "./leaderschedule.txt"
memeberScheduleFile =  "./memberschedule.txt"

# Params from the DB data
# working period of the person
working_hours_start = 10
working_hours_end = 17
mean = 10 + (working_hours_end - working_hours_start)/2 # Help balance the trees 

#Period for looking for a free slot (Basically if looking for a meeting in a week period is 7)
period = 7

# Now we need the persons schedule
# get appointments in the json data
def readSchedule(file):
    schedule = [[]for i in range(period)]
    with open(file) as json_file:
        data = json.load(json_file)
    for e in data['data']['schedule']:
            event = e['start_date_time'][-14:]
            day = e['start_date_time'][-14:][0]
            if day == ("M"):
                    schedule[0].append(int(event[1:3]))
            if day == ("T"):
                    schedule[1].append(int(event[1:3]))
            if day == ("W"):
                    schedule[2].append(int(event[1:3]))
            if day == ("R"):
                    schedule[3].append(int(event[1:3]))
            if day == ("F"):
                    schedule[4].append(int(event[1:3]))
            if day == ("S"):
                    schedule[5].append(int(event[1:3]))
            if day == ("U"):
                    schedule[6].append(int(event[1:3]))
    return schedule

#Gets the free slots of time based on the period 
# or working_hours_start and working_hours_end
def getFreeTimeSlots(ws,we,s):
    result = [[]for i in range(period)]
    start = ws
    for i in range(period):
        while(start< we):
            if not s[i].count(start) > 0:
                result[i].append(start)
            start += 1
        start = ws
    return result

leader_schedule = readSchedule(leaderScheduleFile)
member_schedule = readSchedule(memeberScheduleFile)
leader_freeSlots = getFreeTimeSlots(working_hours_start,working_hours_end, leader_schedule)
member_freeSlots = getFreeTimeSlots(working_hours_start,working_hours_end, member_schedule)

# This is the schedule of the person
# This is not needed is just the fake appointments for testing
search_busySchedule = [Node(mean) for i in range(period)]

#This is the tree with the free slots of time
leader_searchFreeSchedule = [Node(mean) for i in range(period)]
member_searchFreeSchedule =[Node(mean) for i in range(period)]

###Second: we put it in the tree
for i in range(period):
    for j in range(len(leader_schedule[i])):
        search_busySchedule[i] = Node.insert(search_busySchedule[i],leader_schedule[i][j])

for i in range(period):
    for j in range(len(leader_freeSlots[i])):
        leader_searchFreeSchedule[i] = Node.insert(leader_searchFreeSchedule[i],leader_freeSlots[i][j])

for i in range(period):
    for j in range(len(member_freeSlots[i])):
        member_searchFreeSchedule[i] = Node.insert(member_searchFreeSchedule[i],member_freeSlots[i][j])

# a and b are array of bsts 
def getFreeHoursInCommon1(a,b):
        result = [[]for i in range(period)]
        leader = [Node.inorderarr(a[x],[]) for x in range(period)] #without time in common
        #leader = [[12, 13, 13.5], [10, 13.5, 15], [13.5, 15], [13.5, 14], [11, 13.5], [13.5], [13.5]] #with time in common 
        #print(leader)
        for i in range(len(leader)):
            for j in range(len(leader[i])):
                if Node.search(b[i],leader[i][j]) != None and Node.search(b[i],leader[i][j]) != b[i] :
                    result[i].append(leader[i][j]) 
        return result
        
#receive the leader root of the day and member root of the day returns the array of slots in common
def inordersearch(lroot, mroot):
        arr = []
        if lroot:
                arr = arr + inordersearch(lroot.left, mroot)
                if lroot.val != None and Node.search(mroot,lroot.val) != None and Node.search(mroot,lroot.val) != mroot :
                        arr.append(lroot.val) 
                arr = arr + inordersearch(lroot.right, mroot)
        return arr

# a and b are array of bsts 
def getFreeHoursInCommon(a,b):
        result = [[]for i in range(period)]
        for i in range(period):
                result[i] = inordersearch(a[i],b[i])
        return result

## Time Recursion
start = timeit.default_timer() 
print(getFreeHoursInCommon(leader_searchFreeSchedule,member_searchFreeSchedule))
stop = timeit.default_timer()
print('Time with recursion: ', stop - start)  

## Time Loops
s1 = timeit.default_timer()
print(getFreeHoursInCommon1(leader_searchFreeSchedule,member_searchFreeSchedule))
s2 = timeit.default_timer()
print('Time with loops: ', s2 - s1)  





