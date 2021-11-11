import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

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
            n = num_neighbours(curr_grid, i, j)
            #when current cell is ON
            if curr_grid[i][j] == 1:
                if n < 2 or n > 3:
                    new_grid[i][j] = 0
                    
            #when current cell is OFF
            if curr_grid[i][j] == 0 and n == 3:
                new_grid[i][j] = 1

    return new_grid




def num_neighbours(grid, i, j):
    counter = 0
    if grid[i-1][j-1] == 1:
        counter += 1
    if grid[i-1][j] == 1:
        counter += 1
    if grid[i-1][j+1]:
        counter += 1
    if grid[i][j-1] == 1:
        counter += 1
    if grid[i][j+1] == 1:
        counter += 1
    if grid[i+1][j-1] == 1:
        counter += 1
    if grid[i+1][j] == 1:
        counter += 1
    if grid[i+1][j+1] == 1:
        counter += 1

    return counter

def add_border(grid):
    x = np.pad(grid, pad_width=1, mode='constant', constant_values=0)
    print(x)
    return x

#read input matrix
with open('input_matrix.txt', 'r') as f:
    grid = [[int(num) for num in line.split(',')] for line in f]


#add padding
grid = add_border(grid)


#animate frame by frame
fig, ax = plt.subplots()
ims = []

for i in range(40):
    if i == 0:
        ax.imshow(grid)
    new = update(grid)
    grid = new
    im = ax.imshow(new, animated=True)
    
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
plt.show()

