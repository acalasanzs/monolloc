import pygame
import pandas as pd
import numpy as np
import csv
from assgnopts import *
import string
print("First Input First Output")
"There's an errror with self.vals that return 0 array"

# Get ABCDEFGH...
chars = [x for x in string.ascii_uppercase]

# Set values of inputs

abc = Assgn(Ar2Dict(["cuants procesos (max: 26)"],"units"),vals=range(1,27),rules=[False,False,True])
abc.input()
t = Assgn(Ar2Dict(chars[:abc.ans],"t"),conj="com a",rules=[False,False,True])
t.input()
ti = Assgn(Ar2Dict(chars[:abc.ans],"ti"),conj="com a",rules=[True,False,True])
ti.input()

# Set tf and te to 0
tf = np.zeros((len(chars[:abc.ans]),)).tolist()
te = np.zeros((len(chars[:abc.ans]),)).tolist()

# Simplify
ti = ti.array
t = t.array

# Update chart
data = {}
def update():
    for idx,x in enumerate(chars[:abc.ans]):
        data[x] = [t[idx],ti[idx],tf[idx],te[idx]]
update()

# Calculate tf with quantum and ti copy to know wich is first
current = ti.copy()
quantum = -1
for idx,x in enumerate(ti):
    first = min(current)
    tf[ti.index(first)] = quantum + t[ti.index(first)]
    quantum += t[ti.index(first)]
    current.remove(first)

# Make a 2D chart of 0 of length sum(t)
table = np.zeros((len(chars[:abc.ans]),sum(t)))
tabley = 0
current = ti.copy()
print(" | ".join([str(tuple(a)) for a in zip(ti,tf)]))

# Calculate wait or run
for idx,k in enumerate(ti):
    # The first is wich is min TI and and its tf
    first = (min(current),tf[ti.index(min(current))])
    # Index of current x for chart is first[0]
    tablex = first[0]
    for x in range(first[0],first[1]+1):
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
    else:
        tabley += 1
    # remove from temp
    current.remove(min(current))

# Reverse table and update chart
table = table[::-1]
update()
print(pd.DataFrame(data))
print("0:t,1:ti,2:tf,3:te")
# Convert to int
print(table.astype(int))

# Save as csv
with open('data.csv', mode='w',newline='') as file:
    file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for x in table:
        file.writerow([int(i) for i in x])



# Init font pygame
pygame.font.init()

# Set display
screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)

# Title and Icon
pygame.display.set_caption("FIFO SOLVER")
img = pygame.image.load('fifo.jpg')
pygame.display.set_icon(img)

run = True

clock = pygame.time.Clock()

dif = 1000/table.shape[0]


def drawGrid():
    global blockSize
    blockSize = int(150/table.shape[0]) #Set the size of the grid block
    while screen.get_width() % blockSize > 0:
        blockSize -= 1  # Make it fit the grid
    for x in range(0, screen.get_width(), blockSize):
        for y in range(0, screen.get_height(), blockSize):
            try:
                assert table[int(y/blockSize)][int(x/blockSize)] == 1
                color = (0, 184, 148)   # If 1 color green
            except:
                try:
                    assert table[int(y/blockSize)][int(x/blockSize)] == 2
                    color = (225, 112, 85) # If 2 color red
                except:
                    color = (25,25,25) # Else color black
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, color, rect)
            # Draw square border
            pygame.draw.rect(screen, (255,255,255), rect, 1)

while True:
    dif = screen.get_width()/table.shape[0]
    screen.fill((25,25,25))

    drawGrid()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)