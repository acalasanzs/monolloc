import pandas as pd
import numpy as np
from assgnopts import *
import string
"There's an errror with self.vals that return 0 array"

chars = [x for x in string.ascii_uppercase]

abc = Assgn(Ar2Dict(["cuants procesos (max: 26)"],"units"),vals=range(1,27),rules=[False,False,True])
abc.input()
t = Assgn(Ar2Dict(chars[:abc.ans],"t"),conj="com a",rules=[False,False,True])
t.input()
ti = Assgn(Ar2Dict(chars[:abc.ans],"ti"),conj="com a",rules=[True,False,True])
ti.input()

tf = np.zeros((len(chars[:abc.ans]),)).tolist()
te = np.zeros((len(chars[:abc.ans]),)).tolist()
""" process = np.array(chars[:abc.ans]).reshape(len(chars[:abc.ans]),1)
print(process) """
ti = ti.array
t = t.array
data = {}
def update():
    for idx,x in enumerate(chars[:abc.ans]):
        data[x] = [t[idx],ti[idx],tf[idx],te[idx]]
update()
dt = pd.DataFrame(data)
print(dt)
print("0:t,1:ti,2:tf,3:te")
print("Zeros are x")
current = ti.copy()
quantum = -1
for idx,x in enumerate(ti):
    first = min(current)
    tf[ti.index(first)] = quantum + t[ti.index(first)]
    quantum += t[ti.index(first)]
    current.remove(first)
    #del current[ti.index(first)]
table = np.zeros((len(chars[:abc.ans]),quantum+1))
tablex = 0
tabley = 0
current = ti.copy()
print(" | ".join([str(tuple(a)) for a in zip(ti,tf)]))

for k in ti:
    first = (min(current),tf[ti.index(min(current))])
    if first == (0,1):
        first = (0,1+1)
    for x in range(first[0],first[1]):
        try:
            assert table[tabley-1][tablex-1] == 1
            table[tabley][tablex-1] = 2
            table[tabley][tablex] = 1
        except:
            try:
                table[tabley][tablex] = 1
            except IndexError:
                break
        tablex += 1
    else:
        tabley += 1
    current.remove(min(current))


table = table[::-1]
update()
print(pd.DataFrame(data))
print("0:t,1:ti,2:tf,3:te")
print(table)