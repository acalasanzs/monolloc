import pygame
import pandas as pd
import numpy as np
import csv
from assgnopts import *
import string

chars = [x for x in string.ascii_uppercase]

abc = Assgn(Ar2Dict(["cuants procesos (max: 26)"],"units"),vals=range(1,27),rules=[False,False,True])
abc.input()
t = Assgn(Ar2Dict(chars[:abc.ans],"t"),conj="com a",rules=[False,False,True])
t.input()
ti = Assgn(Ar2Dict(chars[:abc.ans],"ti"),conj="com a",rules=[True,False,True])
ti.input()

tf = np.zeros((len(chars[:abc.ans]),)).tolist()
te = np.zeros((len(chars[:abc.ans]),)).tolist()

ti = ti.array
t = t.array

data = {}
def update():
    for idx,x in enumerate(chars[:abc.ans]):
        data[x] = [t[idx],ti[idx],tf[idx],te[idx]]
update()
dt = pd.DataFrame(data)

current = ti.copy()
quantum = -1
for idx,x in enumerate(ti):
    first = min(current)
    tf[ti.index(first)] = quantum + t[ti.index(first)]
    quantum += t[ti.index(first)]
    current.remove(first)
table = np.zeros((len(chars[:abc.ans]),sum(t)))
tabley = 0
current = ti.copy()
# print(" | ".join([str(tuple(a)) for a in zip(ti,tf)]))

for idx,k in enumerate(ti):
    first = (min(current),tf[ti.index(min(current))])
    tablex = first[0]
    for x in range(first[0],first[1]+1):
        try:
            assert table[tabley-1][tablex] in (1,2)
            table[tabley][tablex] = 2
            te[idx] += 1
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
print(table.astype(int))
with open('data.csv', mode='w',newline='') as file:
    file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for x in table:
        file.writerow([int(i) for i in x])




pygame.font.init()

screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)

# Title and Icon
pygame.display.set_caption("FIFO SOLVER")
img = pygame.image.load('fifo.jpg')
pygame.display.set_icon(img)

run = True

clock = pygame.time.Clock()
  
while True:
    screen.fill((0,184,148))

    # Draw a red rectangle that resizes with the window.
    pygame.draw.rect(screen, (255,255,255), (screen.get_width()/3,
      screen.get_height()/3, screen.get_width()/3,
      screen.get_height()/3))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)