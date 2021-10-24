import numpy as np
import csv
from assgnopts import *
print(color.t.OKGREEN+"Round Robin"+color.end)
"There's an errror with self.vals that return 0 array"

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string
# Get ABCDEFGH...
chars = []

# Set values of inputs

abc = Assgn(Ar2Dict(["cuants procesos"],"units"),vals=range(1,1001),rules=[False,False,True],ui=False)
abc.input()

for o in range(1,abc.ans+1):
    chars.append(colnum_string(o))
quantum = Assgn(Ar2Dict(["quantum"],"units"),vals=range(1,1001),rules=[False,False,True],ui=False)
quantum.input()
quantum = quantum.ans

t = Assgn(Ar2Dict(chars,"t"),conj="com a",rules=[False,False,True])
t.input()
ti = Assgn(Ar2Dict(chars,"ti"),conj="com a",rules=[True,False,True])
ti.input()

# Set tf and te to 0
tf = [0] * abc.ans
te = [0] * abc.ans

# Simplify
ti = ti.array
t = t.array








def findWaitingTime(n, bt,
                         wt, quantum):
    global i3table
    i3table = []
    rem_bt = [0] * n
    # Copy the burst time into rt[]
    for i in range(n):
        rem_bt[i] = bt[i]
    t = 0 # Current time
 
    # Keep traversing processes in round
    # robin manner until all of them are
    # not done.
    while(1):
        done = True
        i2table = []
 
        # Traverse all processes one by
        # one repeatedly
        for i in range(n):
             
            # If burst time of a process is greater
            # than 0 then only need to process further
            if (rem_bt[i] > 0) :
                done = False # There is a pending process
                 
                if (rem_bt[i] > quantum) :
                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    t += quantum
 
                    # Decrease the burst_time of current
                    # process by quantum
                    rem_bt[i] -= quantum
                    for _ in range(quantum):
                        i2table.append(1)
                    
                 
                # If burst time is smaller than or equal 
                # to quantum. Last cycle for this process
                else:
                    a = rem_bt[i]
                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    t = t + rem_bt[i]
                    # Waiting time is current time minus
                    # time used by this process
                    wt[i] = t - bt[i]
 
                    # As the process gets fully executed
                    # make its remaining burst time = 0
                    rem_bt[i] = 0
                    for i in range(a):
                        i2table.append(2)
        else:
            i3table.append(i2table)
                 
        # If all processes are done
        if (done == True):
            break
             
# Function to calculate turn around time
def findTurnAroundTime(n, bt, wt, tat):
     
    # Calculating turnaround time
    for i in range(n):
        tat[i] = bt[i] + wt[i]




#findWaitingTime(abc.ans,ti,te,quantum)
findTurnAroundTime(abc.ans,ti,te,tf)
print(i3table)


# Make a 2D chart of 0 of length sum(t)
table = np.zeros((abc.ans,sum(t)))
current = ti.copy()
print(" | ".join([str(tuple(a)) for a in zip(ti,tf)]))
def AnyGreaterThan(a,ar):
    for x in ar:
        if a > x:
            return True
# Calculate wait or run
count = 0
for idx,k in enumerate(i3table):
    # The first is wich is min TI and and its tf
    for x in range(len(i3table[idx])):
        # Index of current x for chart is first[0]
        try:
            if table[idx-1][count] == 0:
                i3table[idx][x] = 1
            table[idx][count] = i3table[idx][x]
            if i3table[idx][x] == 1:
                count +=1
        except:
            break

# Reverse table and update chart
table = table[::-1]

print("Processes    Burst Time(ti)     Final Time(TF)    Waiting(te)",
                     "Time(t)    Turn-Around Time(te+t)")
for i in range(abc.ans): 
        print(" ", chars[i], "\t\t", ti[i],
              "\t\t", tf[i], "\t\t   ", te[i], "\t",t[i], "\t\t",te[i]+t[i])
print("\nAverage waiting time = %.5f "%(te[i] /abc.ans) )
print("Average turn around time = %.5f "% (te[i]+t[i] / abc.ans))
# Convert to int
print(table.astype(int))

# Save as csv
with open('data.csv', mode='w',newline='') as file:
    file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for x in table:
        file.writerow([int(i) for i in x])