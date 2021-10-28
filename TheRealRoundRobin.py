import pygame
import numpy as np
import csv
from assgnopts import *
print(color.t.OKGREEN+"Round Robin Chart"+color.end)
"There's an errror with self.vals that return 0 array"
def Interface():
    # Init font pygame
    pygame.font.init()

    # Set display
    screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)

    # Title and Icon
    pygame.display.set_caption("Round Robin Solver")
    img = pygame.image.load('global.jpg')
    pygame.display.set_icon(img)

    clock = pygame.time.Clock()
    FPS = 24


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
                if blockSize > 15:
                    pygame.draw.rect(screen, (255,255,255), rect, 1)

    while True:
        screen.fill((25,25,25))

        drawGrid()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        clock.tick(FPS)
def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string
# Get ABCDEFGH...
chars = []
def DefaultInputs():
    global abc, t, ti , tf , te, quantum
    abc = Assgn(Ar2Dict(["cuants procesos"],"units"),vals=range(1,1001),rules=[False,False,True],ui=False)
    abc.ans = 3
    quantum = 1
    for o in range(1,abc.ans+1):
        chars.append(colnum_string(o))

    t = Assgn(Ar2Dict(chars,"t"),conj="com a",rules=[False,False,True])
    t = [5,5,5]
    ti = Assgn(Ar2Dict(chars,"ti"),conj="com a",rules=[True,False,True])
    ti = [0,1,0]

    # Set tf and te to 0
    tf = [0] * abc.ans
    te = [0] * abc.ans
def inputs():
    global abc, t, ti , tf , te, quantum
    # Set values of inputs

    abc = Assgn(Ar2Dict(["cuants procesos"],"units"),vals=range(1,1001),rules=[False,False,True],ui=False)
    abc.input()
    quantum = Assgn(Ar2Dict(["quantum"],"units"),vals=range(1,1001),rules=[False,False,True],ui=False)
    quantum.input()
    quantum = quantum.ans
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
def HowManyZeros(arr):
    temp = arr.copy()
    count = 0
    for h in arr:
        if h == 0:
            temp.remove(h)
            count +=1
    return count


def minval(array):
    arr = array.copy()
    while 0 in arr:
        arr.remove(0)
    if len(arr) == 0:
        return False
    return min(arr)

def QTable():
    global quantum_table
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
    for idx,k in enumerate(current):
        # The first is wich is min TI and and its tf
        count = 0
        first = ( current[idx] , current[idx] + t[idx] -1 )
        # Index of current x for chart is first[0]
        for x in range(first[0],first[1]+1):
            count += 1/quantum
            quant[idx] = count
            try:
                quantum_table[idx][x] = quant[idx]
            except IndexError:
                # If the above code bounds the limits here breaks loop
                break

def UpdateQuantum():
    global quantum_table
    # Calculate tf with quantum and ti copy to know wich is first
    current = ti.copy()
    time = -1
    for idx,x in enumerate(ti):
        first = min(current)
        tf[ti.index(first)] = time + t[ti.index(first)]
        time += t[ti.index(first)]
        current.remove(first)
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
            quant[idx] = count
            try:
                if quantum_table[idx][x] == -1:
                    count = 0
                    quantum_table[idx][x] = 1/quantum
                    for others in range(abc.ans):
                        if idx != others and quantum_table[others][x] > 0:
                            quantum_table[others][x] += 1/quantum
            except IndexError:
                # If the above code bounds the limits here breaks loop
                break
        # remove from temp
        current.remove(min(current))
def ResolveQ():
    global table
    cprocesses = list(range(abc.ans))
    for x in range(table.shape[1]):
        # If duplicates 
        cquantum_column = column(quantum_table,x)
        if len(set(column(quantum_table,x))) != len(column(quantum_table,x)):
            if len(cquantum_column) > 1:
                currentmin = column(quantum_table,x).index(minval(column(quantum_table,x)))
                print(currentmin)
                cquantum_column.remove(minval(column(quantum_table,x)))
            else:
                currentmin = 0
            quantum_table[currentmin][x] = -1
        else:
            quantum_table[currentmin][x] = -1 if quantum_table[currentmin][x] == minval(column(quantum_table,x)) else quantum_table[currentmin][x]
def Draw():
    global table
    # Make a 2D chart of 0 of length sum(t)
    current = ti.copy()

    # Calculate wait or run
    for idx,k in enumerate(ti):
        # The first is wich is min TI and and its tf
        first = (min(current),tf[ti.index(min(current))])
        # Index of current x for chart is first[0]
        for x in range(first[0],first[1]+1):
            try:
                other = column(quantum_table,x)
                other.remove(minval(other))
                column_set = set(column(quantum_table,x))
                if 0 in column_set:
                    column_set.remove(0)
                column_arr = column(quantum_table,x)
                for h in column(quantum_table,x):
                    if h == 0:
                        column_arr.remove(h)
                if len(column_set) != len(column_arr):
                    pass
                table[np.where(column(quantum_table,x) == minval(column(quantum_table,x)))[0][0]][x] = 1
                if minval(other):
                    for _ in other:
                        if minval(other):
                            if table[np.where(column(quantum_table,x) == minval(other))[0][0]][x] == 1:
                                other.remove(minval(other))
                            other.remove(minval(other))
                for k in range(abc.ans):
                    if table[k][x] != 1:
                        if quantum_table[k][x] != 0:
                            table[k][x] = 2

            except IndexError as err:
                # If the above code bounds the limits here breaks loop
                break
        # remove from temp
        current.remove(min(current))




if __name__ == "__main__":
    DefaultInputs()
    table = np.zeros((abc.ans,sum(t)))
    QTable()
    ResolveQ()
    Draw()
    # Reverse table and update chart
    table = table[::-1]
    quantum_table = quantum_table[::-1]

    total = np.array([table,quantum_table])

    print("Processes    Burst Time(ti)     Final Time(TF)    Waiting(te)",
                        "Time(t)    Turn-Around Time(te+t)")
    for i in range(abc.ans): 
            print(" ", chars[i], "\t\t", ti[i],
                "\t\t", tf[i], "\t\t   ", te[i], "\t\t",t[i], "\t\t",te[i]+t[i])
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
    #Interface()