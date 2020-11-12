from bst import Node
import json

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
schedule = [[]for i in range(period)]
with open('./data.txt') as json_file:
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

#print the array with the schedule        
#print(schedule)

# Gets the free slots of time based on the period or working_hours_start and working_hours_end
def getFreeTimeSlots():
    result = [[]for i in range(period)]
    start = working_hours_start
    for i in range(period):
        while(start< working_hours_end):
            if not schedule[i].count(start) > 0:
                result[i].append(start)
            start += 1
        start = working_hours_start
    return result
freeSlot = getFreeTimeSlots()

# This is the schedule of the person
# This is not needed is just the fake appointments for testing
search_busySchedule = [Node(mean) for i in range(period)]

#This is the tree with the free slots of time
search_freeSchedule = [Node(mean) for i in range(period)]

###Second: we put it in the tree
for i in range(period):
    for j in range(len(schedule[i])):
        search_busySchedule[i] = Node.insert(search_busySchedule[i],schedule[i][j])

for i in range(period):
    for j in range(len(freeSlot[i])):
        search_freeSchedule[i] = Node.insert(search_freeSchedule[i],freeSlot[i][j])

# Print the tree
# for i in range(period):
#     print("tree of", days[i])
#     Node.inorder( search_freeSchedule[i])


# a and b are array of bsts 
def getFreeHoursInCommon(a,b):
        result = [[]for i in range(period)]
        leader = [Node.inorderarr(a[x],[]) for x in range(period)] #without time in common
        #leader = [[12, 13, 13.5], [10, 13.5, 15], [13.5, 15], [13.5, 14], [11, 13.5], [13.5], [13.5]] #with time in common 
         #print(leader)
        for i in range(len(leader)):
                for j in range(len(leader[i])):
                        if Node.search(b[i],leader[i][j]) != None and Node.search(b[i],leader[i][j]) != b[i] :
                                result[i].append(leader[i][j]) 

        return result

print(getFreeHoursInCommon(search_busySchedule,search_freeSchedule))
