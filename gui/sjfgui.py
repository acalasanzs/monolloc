import pygame
import pandas as pd
import numpy as np
import csv
from assgnopts import *
print("Short Job First")
"There's an errror with self.vals that return 0 array"

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string
# Get ABCDEFGH...
chars = []

abc = Assgn(Ar2Dict(["cuants procesos (max: 26)"],"units"),vals=range(1,27),rules=[False,False,True])
abc.input()

for o in range(1,abc.ans):
    chars.append(colnum_string(o))

t = Assgn(Ar2Dict(chars,"t"),conj="com a",rules=[False,False,True])
t.input()
ti = Assgn(Ar2Dict(chars,"ti"),conj="com a",rules=[True,False,True])
ti.input()

tf = np.zeros((abc.ans,)).tolist()
te = np.zeros((abc.ans,)).tolist()
""" process = np.array(chars).reshape(len(chars),1)
print(process) """
ti = ti.array
t = t.array
data = {}
def update():
    for idx,x in enumerate(chars):
        data[x] = [t[idx],ti[idx],tf[idx],te[idx]]
update()
dt = pd.DataFrame(data)
print(dt)
print("0:t,1:ti,2:tf,3:te")
print("Zeros are x")
current = ti.copy()
quantum = 0
for idx,x in enumerate(ti):
    first = min(current)
    tf[ti.index(first)] = quantum + t[ti.index(first)]
    quantum += t[ti.index(first)]
    current.remove(first)
    #del current[ti.index(first)]
tf = [int(a) for a in tf]
table = np.zeros((abc.ans,sum(t)))
tabley = 0
current = ti.copy()
ranges = [tuple(a) for a in zip(ti,tf)]
print(" | ".join([str(a) for a in ranges]))
print(tf)
for idx,k in enumerate(ti):
    minu = []
    for rang in ranges:
        minu.append(len(range(rang[0],rang[1])))
    first2 = min(minu)
    tablex = ranges[[len(range(x[0],x[1])) for x in ranges].index(first2)][0]
    print(range(ranges[[len(range(x[0],x[1])) for x in ranges].index(first2)][0],ranges[[len(range(x[0],x[1])) for x in ranges].index(first2)][1]))
    for x in range(ranges[[len(range(x[0],x[1])) for x in ranges].index(first2)][0],ranges[[len(range(x[0],x[1])) for x in ranges].index(first2)][1]):
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
    ranges.remove(ranges[[len(range(x[0],x[1])) for x in ranges].index(first2)])


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
pygame.display.set_caption("SJF SOLVER")
img = pygame.image.load('global.jpg')
pygame.display.set_icon(img)

run = True

clock = pygame.time.Clock()

dif = 1000/table.shape[0]


def drawGrid():
    global blockSize
    blockSize = int(150/table.shape[0]) #Set the size of the grid block
    while screen.get_width() % blockSize > 0:
        blockSize -= 1
    for x in range(0, screen.get_width(), blockSize):
        for y in range(0, screen.get_height(), blockSize):
            try:
                assert table[int(y/blockSize)][int(x/blockSize)] == 1
                color = (0, 184, 148)
            except:
                try:
                    assert table[int(y/blockSize)][int(x/blockSize)] == 2
                    color = (225, 112, 85)
                except:
                    color = (25,25,25)
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255,255,255), rect, 1)

while True:
    dif = screen.get_width()/table.shape[0]
    screen.fill((25,25,25))

    """ # Draw a red rectangle that resizes with the window.
    pygame.draw.rect(screen, (255,255,255), (screen.get_width()/3,
      screen.get_height()/3, screen.get_width()/3,
      screen.get_height()/3)) """
    drawGrid()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)