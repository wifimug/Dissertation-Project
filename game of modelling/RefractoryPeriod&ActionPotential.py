import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import time 


"""
If a cell is ON and has fewer than two neighbors that are ON, it turns OFF
If a cell is ON and has either two or three neighbors that are ON, it remains ON.
If a cell is ON and has more than three neighbors that are ON, it turns OFF.
If a cell is OFF and has exactly three neighbors that are ON, it turns ON.
====
Aims:
- add refractory period
- add threshold potential
===
Each cell stimulates all neighbours around it if it is 
stimulated above a threshold, T
Each cell produces a stimulation of a set amplitude A
Stimulation is accumulated from all the neighbours
Stimulation lasts a 0.5 seconds
0.8 seconds following the stimulation, cells cannot be stimulated
"""

'''
When the cell is on:
- the active time starts from zero and starts counting
- the refractory period is zero
When the cell is off:
- the active time is zero
- refractory period starts counting
'''

#set amplitude of stimulation
AMPLITUDE = 0.1

#threshold for each cell
THRESHOLD = 0.2

#refractory period
REFRACTORY_PERIOD = 0.2

#time active
ACTIVE_TIME = 1.5

#start time
START_TIME = time.time() 

def start_timer():
    #in milliseconds
    return round(time.time() * 1000)

#for one cell, c, find it's neighbours
def update(curr_display_grid, curr_rp_grid, curr_ap_grid, curr_at_grid):
    new_display_grid = copy.deepcopy(curr_display_grid)
    new_rp_grid = copy.deepcopy(curr_rp_grid)
    new_ap_grid = copy.deepcopy(curr_ap_grid)
    new_at_grid = copy.deepcopy(curr_at_grid)
    #at stores the start times, to calculate at
    #find the difference of start time and current time
    


    for i in range(len(curr_display_grid)-1): 
        for j in range(len(curr_display_grid[0])-1):
            ap = neighbour_ap(curr_display_grid, i, j)
            new_rp_time = time_elapsed(curr_rp_grid, i, j)
            at_time = time_elapsed(curr_at_grid, i, j)
            curr_ap_grid[i][j] = ap

            
            #when current cell is ON
            if curr_display_grid[i][j] == 1:
                if at_time >= ACTIVE_TIME:
                    #cell turns off
                    new_display_grid[i][j] = 0
                    #ap is 0 now that it's OFF
                    new_ap_grid[i][j] = 0
                    new_at_grid[i][j] = ap
                    new_rp_grid[i][j] = start_timer()

            #when current cell is OFF
            if curr_display_grid[i][j] == 0:
                #cell turns ON if 
                    #stimulated above threshold
                    #past refractory period
                new_ap_grid[i][j] = ap
                if ap >= THRESHOLD and new_rp_time >= REFRACTORY_PERIOD:
                    new_display_grid[i][j] = 1
                    new_ap_grid[i][j] = 0
                    #rp starts from 0
                    new_rp_grid[i][j] = 0
                    #gets current time, where cell starts being active
                    new_at_grid[i][j] = start_timer()


    return new_display_grid, new_rp_grid, new_ap_grid, new_at_grid

def time_elapsed(rp_grid, i, j):
    curr_time = round(time.time() * 1000)
    time_elapsed = curr_time - rp_grid[i][j]

    return time_elapsed


def neighbour_ap(ap_grid, i, j):
    counter = 0
    if ap_grid[i-1][j-1] == 1:
        counter += AMPLITUDE
    if ap_grid[i-1][j] == 1:
        counter += AMPLITUDE
    if ap_grid[i-1][j+1]:
        counter += AMPLITUDE
    if ap_grid[i][j-1] == 1:
        counter += AMPLITUDE
    if ap_grid[i][j+1] == 1:
        counter += AMPLITUDE
    if ap_grid[i+1][j-1] == 1:
        counter += AMPLITUDE
    if ap_grid[i+1][j] == 1:
        counter += AMPLITUDE
    if ap_grid[i+1][j+1] == 1:
        counter += AMPLITUDE

    return counter


def add_border(grid):
    x = np.pad(grid, pad_width=1, mode='constant', constant_values=0)
    print(x)
    return x


#read input matrix
with open('input_matrix.txt', 'r') as f:
    og_grid = [[float(num) for num in line.split(',')] for line in f]


#add padding
og_grid = add_border(og_grid)
#refractory period and action potential grid
size = (len(og_grid), len(og_grid))
rp_grid = np.zeros(size)
ap_grid = np.zeros(size)
at_grid = np.full(size, START_TIME)



#animate frame by frame
fig, ax = plt.subplots()
ims = []

for i in range(100):
    if i == 0:
        ax.imshow(og_grid)
    new = update(og_grid, rp_grid, ap_grid, at_grid)
    og_grid, rp_grid, ap_grid, at_grid = new
    im = ax.imshow(og_grid, animated=True)
    
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
plt.show()

