import numpy as np
import csv
from assgnopts import *
print(color.t.OKGREEN+"First Input First Output"+color.end)
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
quantum = 2
for o in range(1,abc.ans+1):
    chars.append(colnum_string(o))

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



def column(table,x):
    column = [0] * table.shape[0]
    for h in range(len(column)):
        column[h] = table[h][x]
    return column










# Calculate tf with quantum and ti copy to know wich is first
current = ti.copy()
time = -1
for idx,x in enumerate(ti):
    first = min(current)
    tf[ti.index(first)] = time + t[ti.index(first)]
    time += t[ti.index(first)]
    current.remove(first)

quantum_table = np.zeros((abc.ans,sum(t)))
current = ti.copy()
quant = [0] * abc.ans
# Calculate wait or run
for idx,k in enumerate(ti):
    # The first is wich is min TI and and its tf
    count = 0
    first = (min(current),tf[ti.index(min(current))])
    # Index of current x for chart is first[0]
    for x in range(first[0],first[1]+1):
        count += 1/quantum
        """ if int(count) < 1:
            quant[idx] = 1
        else:
            quant[idx] = int(count) """
        quant[idx] = count
        try:
            quantum_table[idx][x] = quant[idx]
        except IndexError:
            # If the above code bounds the limits here breaks loop
            break
    # remove from temp
    current.remove(min(current))


# Make a 2D chart of 0 of length sum(t)
table = np.zeros((abc.ans,sum(t)))
tabley = 0
current = ti.copy()
print(" | ".join([str(tuple(a)) for a in zip(ti,tf)]))

# Calculate wait or run
for idx,k in enumerate(ti):
    # The first is wich is min TI and and its tf
    first = (min(current),tf[ti.index(min(current))])
    # Index of current x for chart is first[0]
    for x in range(first[0],first[1]+1):
        try:
            quantum_column = column(quantum_table,x)
            print(quantum_column,quantum_column.index(min(quantum_column)))
            table[quantum_column.index(min(quantum_column))-1][x] = 1
        except IndexError:
            # If the above code bounds the limits here breaks loop
            break
    # remove from temp
    current.remove(min(current))






























# Reverse table and update chart
table = table[::-1]
quantum_table = quantum_table[::-1]

total = np.array([table,quantum_table])

print("Processes    Burst Time(ti)     Final Time(TF)    Waiting(te)",
                     "Time(t)    Turn-Around Time(te+t)")
for i in range(abc.ans): 
        print(" ", chars[i], "\t\t", ti[i],
              "\t\t", tf[i], "\t\t   ", te[i], "\t",t[i], "\t\t",te[i]+t[i])
print("\nAverage waiting time = %.5f "%(te[i] /abc.ans) )
print("Average turn around time = %.5f "% (te[i]+t[i] / abc.ans))
# Convert to int
#print(table.astype(int))
print(total.astype(float))
# Save as csv
with open('data.csv', mode='w',newline='') as file:
    file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for x in table:
        file.writerow([int(i) for i in x])