from os import remove
import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

"""
If enough cells in the neighbourhood are on:
- current cell is stimulated, value set to 20
- cell value will tick down each generation
- cannot be stimulated again until resting value

Neighbourhood:
- a circular neighbourhood 

"""

THRESHOLD = 3
RADIUS = 5
REFRACTORY = 10


#for one cell, c, find it's neighbours
def update(curr_grid):
    curr_grid = add_border(curr_grid)
    new_grid = copy.deepcopy(curr_grid)
    # print(curr_grid[10][10])
    for i in range(len(curr_grid)-RADIUS):
        for j in range(len(curr_grid[0])-RADIUS):
            n = num_neighbours(curr_grid, i, j, RADIUS)
            #when current cell is ON
            if curr_grid[i][j] > 0:
                new_grid[i][j] -= 1
                    
            #when current cell is OFF
            if curr_grid[i][j] == 0 and n >= THRESHOLD:
                new_grid[i][j] = REFRACTORY
    new_grid = remove_border(new_grid)
    return new_grid




def num_neighbours(grid, i, j, radius):
    counter = 0
    for r in range(1,radius+1):   
        #print("radius", ((i-r)**2 + (j-r)**2)) 
        if ((r)**2 + (r)**2) <= radius**2:
            
            NW = grid[i-r][j-r]
            N = grid[i-r][j]
            NE = grid[i-r][j+r]
            W = grid[i][j+r]
            E = grid[i][j-r]
            SW = grid[i+r][j-r]
            S = grid[i+r][j]
            SE = grid[i+r][j+r]

            if NW == 1:
                counter += 1
            if N == 1:
                counter += 1
            if NE == 1:
                counter += 1
            if W == 1:
                counter += 1
            if E == 1:
                counter += 1
            if SW == 1:
                counter += 1
            if S == 1:
                counter += 1
            if SE == 1:
                counter += 1
            #print("counter",counter)
    return counter


def add_border(grid):
    x = np.pad(grid, pad_width=RADIUS, mode='constant', constant_values=10000)
    return x

def remove_border(grid):
    for i in range(RADIUS):
        grid = np.delete(grid, len(grid)-1, 1)
        grid = np.delete(grid, len(grid)-1, 0)
        grid = np.delete(grid, 0, 1)
        grid = np.delete(grid, 0, 0)
    return grid

def printProgressBar (iteration, total, length):

    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent}% Complete', end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()
    


grid = np.zeros((50,50))
grid[0][0] = 20
grid[0][1] = 20
grid[1][1] = 20
grid [1][2] = 20

for i in range(10,21):
    for j in range(10,16):
        grid[i][j] = -1



#add padding
grid = add_border(grid)


#animate frame by frame
fig, ax = plt.subplots()
ims = []
colors = ['k', 'r', 'y', 'w']

ITERATIONS = 500
printProgressBar(0, ITERATIONS, length = 50)
for i in range(ITERATIONS):
    if i == 0:
        grid = remove_border(grid)
        ax.imshow(grid, animated=True, cmap='Oranges', interpolation='nearest')
    new = update(grid)
    grid = new
    
    im = ax.imshow(new, animated=True, cmap='Oranges', interpolation='nearest')
    ims.append([im])
    printProgressBar(i+1,ITERATIONS, length = 50)
    


ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
plt.show()

