import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import copy
import time 


"""
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

#each cell emits this amplitude of stimulation
AMPLITUDE = 0.5

#threshold level to reach for cell to be activated
THRESHOLD = 1

#refractory period after being activated in seconds
REFRACTORY_PERIOD = 1

#active cell time in seconds
ACTIVE_TIME = 0.5

RADIUS = 3

def start_timer():
    #in milliseconds
    return round(time.time())

'''
ap - action potential
rp - refractory period
at - active time
'''

#for one cell, c, find it's neighbours
def update(curr_display_grid, curr_rp_grid, curr_at_grid):
    new_display_grid = copy.deepcopy(curr_display_grid)
    new_rp_grid = copy.deepcopy(curr_rp_grid)
    new_at_grid = copy.deepcopy(curr_at_grid)
    #at stores the start times, to calculate at
    #find the difference of start time and current time
    


    for i in range(len(curr_display_grid)): 
        for j in range(len(curr_display_grid[0])):
            ap = neighbour_ap(curr_display_grid, i, j, RADIUS)
            rp_time = time_elapsed(curr_rp_grid[i][j])
            at_time = time_elapsed(curr_at_grid[i][j])
            checked = False
           
            #when current cell is ON
            '''
            if active time is reached
            CELL IS TURNED OFF:
            active time should be zero
            refractory period should start counting
            '''
            if curr_display_grid[i][j] == 1:
                
                if at_time >= ACTIVE_TIME:
                    # print("at_time", at_time)
                    #cell turns off
                    # print("cell turning off")
                    new_display_grid[i][j] = 0
                    #ap is 0 now that it's OFF
                    new_at_grid[i][j] = start_timer()
                    new_rp_grid[i][j] = start_timer()
 

                    #print("timer started:", new_rp_grid[i][j])
                   

            #when current cell is OFF
            '''
            if action potential threshold is reached
            if refractory period has passed
            CELL IS TURNED ON:
            active time should start counting
            refractory time should be 0
            '''
            if curr_display_grid[i][j] == 0:
                #cell turns ON if 
                #stimulated above threshold
                #past refractory period
                if ap >= THRESHOLD and rp_time >= REFRACTORY_PERIOD:

                    new_display_grid[i][j] = 1
                    #rp starts from 0
                    #print("rp time: ", rp_time)
                    #gets current time, where refractory period starts
                    new_rp_grid[i][j] = start_timer()
                    #gets current time, where cell starts being active
                    new_at_grid[i][j] = start_timer()


                    
    #print("ap:", grid[0][25], "at:", at_grid[0][25], "rp:", rp_grid[0][25])
    return new_display_grid, new_rp_grid, new_at_grid


def time_elapsed(rp_grid):
    curr_time = round(time.time())
    time_elapsed = curr_time - rp_grid
    return time_elapsed


def get_cell(grid, i , j):
    cell_i = i
    cell_j = j
    if i > len(grid) - 1:
        cell_i = i - len(grid)
    if i < 0:
        cell_i = len(grid) + i
    if j > len(grid) - 1:
        cell_j = j - len(grid) 
    if j < 0:
        cell_j = len(grid) + j
    return grid[cell_i][cell_j]




def neighbour_ap(grid, i, j, radius):
    counter = 0
    for r in range(1,radius+1):   
        #print("radius", ((i-r)**2 + (j-r)**2)) 
        if ((r)**2 + (r)**2) <= radius**2:
            
            NW = get_cell(grid, i-r, j-r)
            N = get_cell(grid, i-r, j)
            NE = get_cell(grid, i-r, j+r)
            W = get_cell(grid, i, j+r)
            E = get_cell(grid, i, j-r)
            SW = get_cell(grid, i+r, j-r)
            S = get_cell(grid, i+r, j)
            SE = get_cell(grid, i+r, j+r)
            # NW = (grid[i-r][j-r])
            # N = (grid[i-r][j])
            # NE = (grid[i-r][j+r])
            # W = (grid[i][j+r])
            # E = (grid[i][j-r])
            # SW = (grid[i+r][j-r])
            # S = (grid[i+r][j])
            # SE = (grid[i+r][j+r])
            if NW == 1:
                counter += AMPLITUDE
            if N == 1:
                counter += AMPLITUDE
            if NE == 1:
                counter += AMPLITUDE
            if W == 1:
                counter += AMPLITUDE
            if E == 1:
                counter += AMPLITUDE
            if SW == 1:
                counter += AMPLITUDE
            if S == 1:
                counter += AMPLITUDE
            if SE == 1:
                counter += AMPLITUDE
            #print("counter",counter)
    return counter


def add_border(grid):
    x = np.pad(grid, pad_width=RADIUS, mode='constant', constant_values=0)
    return x


#read input matrix
# with open('input_matrix.txt', 'r') as f:
#     og_grid = [[float(num) for num in line.split(',')] for line in f]

SIZE = (50,50)
#start time
START_TIME = time.time()
og_grid = np.zeros(SIZE)
og_grid[0][0] = 1
og_grid[0][1] = 1





# #add padding
#og_grid = add_border(og_grid)
#refractory period and action potential grid
rp_grid = np.zeros(SIZE)
at_grid = np.full(SIZE, START_TIME)



#fixing colours to numbers
cmap = ListedColormap(['r', 'y'])

#animate frame by frame
fig, ax = plt.subplots()
ax.axis(False)
ims = []

for i in range(100):
    if i == 0:
        ax.imshow(og_grid,cmap=cmap)
    new = update(og_grid, rp_grid, at_grid)
    og_grid, rp_grid, at_grid = new
    im = ax.imshow(og_grid, animated=True, cmap=cmap)
    
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
plt.show()

