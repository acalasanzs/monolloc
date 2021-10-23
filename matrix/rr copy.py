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
tf = np.zeros((abc.ans,)).tolist()
te = np.zeros((abc.ans,)).tolist()

# Simplify
ti = ti.array
t = t.array


# Calculate tf with quantum and ti copy to know wich is first
current = ti.copy()
quant = -1
for idx,x in enumerate(ti):
    first = min(current)
    tf[ti.index(first)] = quant + t[ti.index(first)]
    quant += t[ti.index(first)]
    current.remove(first)

# Make a 2D chart of 0 of length sum(t)
table = np.zeros((abc.ans,sum(t)))
tabley = 0
current = ti.copy()
print(" | ".join([str(tuple(a)) for a in zip(ti,tf)]))

def AnyGreaterThan(a,list):
    for x in list:
        if x > a:
            return True
def matrix(first):
    timer = 0
    global tabley, tablex, idx
    for x in range(first[0],first[1]+1):
        timer += 1
        print(memory)
        if timer > quantum and not AnyGreaterThan(0,[len(range(x[0],x[1]+1)) for x in memory[idx] for idx,a in range(len(memory))]):
            tabley += 1
            break
        print(tablex,quantum)
        memory[idx] = (x,first[1])
        try:
            # if (x-1,y) is 1 or 2
            assert table[tabley-1][tablex] in (1,2)
            # Convert (x,y) to 2
            table[tabley][tablex] = 2
            # Add to wait number
            te[idx] += 1
        except:
            try:
                table[tabley][tablex] = 1
            except IndexError:
                # If the above code bounds the limits here breaks loop
                break
        tablex += 1
idx = 0
# Calculate wait or run
tabley = 0
for idx,k in enumerate(ti):
    idx = idx
    memory = {}
    # The first is wich is min TI and and its tf
    first = (min(current),tf[ti.index(min(current))])
    # Index of current x for chart is first[0]
    tablex = first[0]
    
    matrix(first)
    # remove from temp
    current.remove(min(current))
    print(memory)

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