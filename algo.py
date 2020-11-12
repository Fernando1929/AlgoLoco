from bst import Node
import json
import timeit
#Another issue do we use the leaders working hours or persons working hours 

#Utils (Maybe a class later) Not used for now
days = ['Monday','Thuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

####First: we get the data
#working period of the person
working_hours_start = 10
working_hours_end = 17
mean = 10 + (working_hours_end - working_hours_start)/2

#Period of for looking for a free slot (Basically if looking for a meeting in a week period is 7)
period = 7

# Now we need the persons schedule
# get appointments in the json data
leader_schedule = [[]for i in range(period)]
with open('./leaderschedule.txt') as json_file:
    data = json.load(json_file)
    for e in data['data']['schedule']:
        event = e['start_date_time'][-14:]
        day = e['start_date_time'][-14:][0]
        if day == ("M"):
                leader_schedule[0].append(int(event[1:3]))
        if day == ("T"):
                leader_schedule[1].append(int(event[1:3]))
        if day == ("W"):
                leader_schedule[2].append(int(event[1:3]))
        if day == ("R"):
                leader_schedule[3].append(int(event[1:3]))
        if day == ("F"):
                leader_schedule[4].append(int(event[1:3]))
        if day == ("S"):
                leader_schedule[5].append(int(event[1:3]))
        if day == ("U"):
                leader_schedule[6].append(int(event[1:3]))

member_schedule = [[]for i in range(period)]
with open('./memberschedule.txt') as json_file:
    data = json.load(json_file)
    for e in data['data']['schedule']:
        event = e['start_date_time'][-14:]
        day = e['start_date_time'][-14:][0]
        if day == ("M"):
                member_schedule[0].append(int(event[1:3]))
        if day == ("T"):
                member_schedule[1].append(int(event[1:3]))
        if day == ("W"):
                member_schedule[2].append(int(event[1:3]))
        if day == ("R"):
                member_schedule[3].append(int(event[1:3]))
        if day == ("F"):
                member_schedule[4].append(int(event[1:3]))
        if day == ("S"):
                member_schedule[5].append(int(event[1:3]))
        if day == ("U"):
                member_schedule[6].append(int(event[1:3]))

#print the array with the schedule        
#print(schedule)

# Gets the free slots of time based on the period or working_hours_start and working_hours_end
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
        
s1 = timeit.default_timer()
print(getFreeHoursInCommon1(leader_searchFreeSchedule,member_searchFreeSchedule))
s2 = timeit.default_timer()
print('Time with loops: ', s2 - s1)  

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

start = timeit.default_timer() 
print(getFreeHoursInCommon(leader_searchFreeSchedule,member_searchFreeSchedule))
stop = timeit.default_timer()

print('Time with recursion: ', stop - start)  

# for i in range(period):
#     print("leader")
#     print("tree of", days[i])
#     Node.inorder(leader_searchFreeSchedule[i])
#     print("member")
#     print("tree of", days[i])
#     Node.inorder(member_searchFreeSchedule[i])
#     print(res[i])







