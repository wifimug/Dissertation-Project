import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import random
from mpl_toolkits.mplot3d import Axes3D
import time

"""
If a cell is ON and has fewer than two neighbors that are ON, it turns OFF
If a cell is ON and has either two or three neighbors that are ON, it remains ON.
If a cell is ON and has more than three neighbors that are ON, it turns OFF.
If a cell is OFF and has exactly three neighbors that are ON, it turns ON.
====
glider

   - - x
   x - x
   - x x
"""


#for one cell, c, find it's neighbours
def update(curr_grid):
    new_grid = copy.deepcopy(curr_grid)
    for i in range(len(curr_grid)-1):
        for j in range(len(curr_grid[0])-1):
            for k in range(len(curr_grid[0][0])-1):
                n = num_neighbours(curr_grid, i, j, k)
                #when current cell is ON
                if curr_grid[i][j][k] == 1:
                    if n < 5 or n > 10:
                        new_grid[i][j] = 0
                        
                #when current cell is OFF
                if curr_grid[i][j][k] == 0 and n == 3:
                    new_grid[i][j][[k]] = 1

    return new_grid




def num_neighbours(grid, i, j, k):
    counter = 0
    #26
    if grid[i-1][j-1][k-1] == 1:
        counter += 1

    if grid[i-1][j][k] == 1:
        counter += 1
    if grid[i][j-1][k] == 1:
        counter += 1
    if grid[i][j][k-1] == 1:
        counter += 1

    if grid[i][j-1][k-1] == 1:
        counter += 1
    if grid[i-1][j][k-1] == 1:
        counter += 1
    if grid[i-1][j-1][k] == 1:
        counter += 1

    if grid[i][j+1][k+1] == 1:
        counter += 1
    if grid[i+1][j][k+1] == 1:
        counter += 1
    if grid[i+1][j+1][k] == 1:
        counter += 1
    
    if grid[i-1][j+1][k+1] == 1:
        counter += 1
    if grid[i+1][j-1][k+1] == 1:
        counter += 1
    if grid[i+1][j+1][k-1] == 1:
        counter += 1

    if grid[i+1][j-1][k-1] == 1:
        counter += 1
    if grid[i-1][j+1][k-1] == 1:
        counter += 1
    if grid[i-1][j-1][k+1] == 1:
        counter += 1

    
    if grid[i+1][j][k] == 1:
        counter += 1
    if grid[i][j+1][k] == 1:
        counter += 1
    if grid[i][j][k+1] == 1:
        counter += 1
    
    if grid[i+1][j-1][k] == 1:
        counter += 1
    if grid[i-1][j+1][k] == 1:
        counter += 1
    if grid[i+1][j][k-1] == 1:
        counter += 1
    if grid[i-1][j][k+1] == 1:
        counter += 1
    if grid[i][j+1][k-1] == 1:
        counter += 1
    if grid[i][j-1][k+1] == 1:
        counter += 1

    if grid[i+1][k+1][k+1] == 1:
        counter += 1

    return counter

def add_border(grid):
    x = np.pad(grid, pad_width=1, mode='constant', constant_values=-1)
    return x

def printProgressBar (iteration, total, length):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent}% Complete', end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()

def start_timer():
    #in milliseconds
    return round(time.time())

def calc_time(start, end):
    if end - start > 100:
        print("process took:", (end - start)/60, "mins")
    else:
        print("process took:", end - start,"s")

size = 50
grid = np.random.rand(size, size, size)

# for i in range(len(grid)):
#     for j in range(len(grid)):
#         for k in range(len(grid)):
#             rng = random.randint(1,10)
#             if rng < 5:
#                 grid[i][j][k] == 1

#add padding
grid = add_border(grid)


#animate frame by frame
fig = plt.figure()
ax = plt.axes(1,1,1,projection='3d')
ims = []

x = np.arange(grid.shape[0])[:, None, None]
y = np.arange(grid.shape[1])[None, :, None]
z = np.arange(grid.shape[2])[None, None, :]
x, y, z = np.broadcast_arrays(x, y, z)


c = np.tile(grid.ravel()[:, None], [1, 3])

ITERATIONS = 40 
start_time = start_timer()

printProgressBar(0, ITERATIONS, length = 50)
for i in range(ITERATIONS):
    if i == 0:
        ax.scatter(x, y, z, alpha=0.8)
    new = update(grid)
    grid = new
    
    x = np.arange(grid.shape[0])[:, None, None]
    y = np.arange(grid.shape[1])[None, :, None]
    z = np.arange(grid.shape[2])[None, None, :]
    x, y, z = np.broadcast_arrays(x, y, z)

    im = ax.scatter(x, y, z, alpha=0.8, animated=True)
    
    ims.append([im])
    
    printProgressBar(i+1, ITERATIONS, length = 50)
calc_time(start_time, start_timer())

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
plt.show()

