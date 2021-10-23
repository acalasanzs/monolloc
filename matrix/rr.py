import numpy as np
import csv
from assgnopts import *
print("First Input First Output")
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

abc = Assgn(Ar2Dict(["cuants procesos (max: 1000)"],"units"),vals=range(1,1001),rules=[False,False,True])
abc.input()
quantum = Assgn(Ar2Dict(["quantum"],"quantum"))
quantum.input()
quantum = quantum.ans

for o in range(1,abc.ans+1):
    chars.append(colnum_string(o))

t = Assgn(Ar2Dict(chars,"t"),conj="com a",rules=[False,False,True])
t.input()
ti = Assgn(Ar2Dict(chars,"ti"),conj="com a",rules=[True,False,True])
ti.input()

# Set tf and te to 0
tf = np.zeros((abc.ans,)).tolist()
te = np.zeros((abc.ans,)).tolist()

# Simplify
ti = ti.array
t = t.array



wt = [0] * abc.ans
tat = [0] * abc.ans



def findWaitingTime(n, bt,
                         wt, quantum):
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
                 
                # If burst time is smaller than or equal 
                # to quantum. Last cycle for this process
                else:
                 
                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    t = t + rem_bt[i]
 
                    # Waiting time is current time minus
                    # time used by this process
                    wt[i] = t - bt[i]
 
                    # As the process gets fully executed
                    # make its remaining burst time = 0
                    rem_bt[i] = 0
                 
        # If all processes are done
        if (done == True):
            break
def findTurnAroundTime(n, bt, wt, tat):
    # Calculating turnaround time
    for i in range(n):
        tat[i] = bt[i] + wt[i]

findWaitingTime(abc.ans, ti, wt, quantum)
findTurnAroundTime(abc.ans, ti, wt, tat)


# Make a 2D chart of 0 of length sum(t)
table = np.zeros((abc.ans,sum(t)))
tabley = 0
current = ti.copy()
print(" | ".join([str(tuple(a)) for a in zip(ti,tf)]))

cquantum = 0
# Calculate wait or run
for idx,k in enumerate(ti):
    # The first is wich is min TI and and its tf
    first = (min(current),tf[ti.index(min(current))])
    tablex = first[0]
    rem_bt = [0] * abc.ans
 
    # Copy the burst time into rt[]
    for i in range(abc.ans):
        rem_bt[i] = ti[i]
    t = 0 # Current time
 
    # Keep traversing processes in round
    # robin manner until all of them are
    # not done.
    while(1):
        done = True
 
        # Traverse all processes one by
        # one repeatedly
        for i in range(abc.ans):
             
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
                    tabley += 1
                    try:
                        table[tabley][tablex] = 2
                    except:
                        pass
                 
                # If burst time is smaller than or equal 
                # to quantum. Last cycle for this process
                else:
                 
                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    t = t + rem_bt[i]
 
                    # Waiting time is current time minus
                    # time used by this process
                    wt[i] = t - ti[i]
 
                    # As the process gets fully executed
                    # make its remaining burst time = 0
                    rem_bt[i] = 0
                    tabley -= 1
                    try:
                        table[tabley][tablex] = 1
                    except:
                        pass
            tablex += 1     
        # If all processes are done
        if (done == True):
            break
    # remove from temp
    current.remove(min(current))

# Reverse table and update chart
table = table[::-1]

""" print("Processes    Burst Time(ti)     Final Time(TF)    Waiting(te)",
                     "Time(t)    Turn-Around Time(te+t)")
for i in range(abc.ans): 
        print(" ", chars[i], "\t\t", ti[i],
              "\t\t", tf[i], "\t\t   ", wt[i], "\t",t[i], "\t\t",tat[i])
print("\nAverage waiting time = %.5f "%(te[i] /abc.ans) )
print("Average turn around time = %.5f "% (te[i]+t[i] / abc.ans)) """
# Convert to int
print(table.astype(int))

# Save as csv
with open('data.csv', mode='w',newline='') as file:
    file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for x in table:
        file.writerow([int(i) for i in x])