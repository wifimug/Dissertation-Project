import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import time
import random

'''
Precompute the neighbourhood cells
- 1 array for x coords of neighbours
- 1 array for y coords of neighbours
> neighbourhood adjustable based on radius set
'''

THRESHOLD = 5
RADIUS = 5
REFRACTORY = 20



def update(curr_grid, x_arr, y_arr):
    """
    Updates the state of the current grid given
    the x and y coordinates of the neighbours

    return: state of the new grid
    """
    new_grid = copy.deepcopy(curr_grid)
    step = 0
    active = 0
    for i in range(len(curr_grid)):
        for j in range(len(curr_grid[0])):
            n = get_neighbours(curr_grid, x_arr, y_arr, step)
            # print(n)
            # [ 0 0 0 0 0 0 ]
            # [ 0 0 0 0 0 0 ]
            step += 1

            #when current cell is ON
            if curr_grid[i][j] > 0:
                new_grid[i][j] -= 1
                    
            #when current cell is OFF
            if curr_grid[i][j] == 0 and n >= THRESHOLD:
                new_grid[i][j] = REFRACTORY
                active += 1
            # if i == len(curr_grid)-1 and j == len(curr_grid[0])-1:
            #     print(step)
    return new_grid, active




def get_neighbours_array(init_grid, radius):
    """
    Takes in the init_grid and radius of
    neighbourhood and outputs the x and y coordinates
    of the neighbours for each cell in the init_grid

    return: x and y coordinates as 2 arrays
    """
    x_arr = []
    y_arr = []
    for i in range(len(init_grid)):
        for j in range(len(init_grid[0])):
            x_temp, y_temp = points_in_circle(radius, i, j, 0, len(init_grid))

            x_arr.append(x_temp)
            y_arr.append(y_temp)

    #print(x_arr[:100])
    #print(y_arr[:100])
    return x_arr, y_arr

def points_in_circle(radius, x0, y0, lb, ub):
    x_arr = []
    y_arr = []
    x_ = np.arange(x0 - radius - 1, x0 + radius + 1, dtype=int)
    y_ = np.arange(y0 - radius - 1, y0 + radius + 1, dtype=int)
    x, y = np.where((x_[:,np.newaxis] - x0)**2 + (y_ - y0)**2 <= radius**2)
    for x, y in zip(x_[x], y_[y]):
        if x < ub and x > lb and y < ub and y > lb:
            if not (x == x0 and y == y0):
                x_arr.append(x)
                y_arr.append(y)
    return x_arr, y_arr

def get_neighbours(grid, x_arr, y_arr, s):
    """
    For a cell (i,j) in the grid, get the number of active 
    neighbours.

    return: number of active neighbours
    """
    n = 0
    x = x_arr[s]
    y = y_arr[s]

    for i in range(len(x)):
        if grid[y[i]][x[i]] > 0:
            n += 1
    return n


def start_timer():
    """
    Gets a time in seconds
    
    return: unix time in seconds
    """
    return round(time.time())



def calc_time(start, end):
    """
    Calculates the time elapsed from start time to
    end time. Prints the time elapsed in seconds if 
    time elapsed is less than 100 seconds, else
    prints in minutes.
    """
    if end - start > 100:
        print("process took:", (end - start)/60, "mins")
    else:
        print("process took:", end - start,"s")



def printProgressBar (iteration, total, length):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent}% Complete', end = "\r")
    if iteration == total: 
        print()

    
grid = np.zeros((200,200))
active = 0
for i in range(10):
    for j in range(10):
        rng = random.randint(0,1)
        if rng == 1:
            grid[i][j] = 20
            active += 1
# grid[0][0] = 20

# defining electrically inactive points
# mitral valve
# for i in range(len(grid)-1):
#     for j in range(len(grid)-1, len(grid)-82-1, -1):
#         grid[j][i] = -1

# vein centres
veins_x = [25, 50, len(grid[0])-25, len(grid[0])-50]
veins_y = [25, 50, 25, 50]
vein_radius = 15

# the 4 veins
for v in range(len(veins_x)):
    for i in range(max(veins_y) + vein_radius):
        for j in range(max(veins_x) + vein_radius):
            if ((j-veins_x[v])**2+(i-veins_y[v])**2) <= vein_radius**2:
                grid[i][j] = -1


#animate frame by frame
fig, ax = plt.subplots()
ims = []

ITERATIONS = 500


active_cells = np.zeros(ITERATIONS)

x_arr, y_arr = get_neighbours_array(grid, RADIUS)

print("x_arr length:", len(x_arr))

ax.imshow(grid, animated=False)

start_time = start_timer()
printProgressBar(0, ITERATIONS, length = 50)
for i in range(ITERATIONS):
    if i == 0:
        ax.imshow(grid, animated=True, interpolation='nearest')
    new, active = update(grid, x_arr, y_arr)
    grid = new
    active_cells[i] = active
    im = ax.imshow(new, animated=True, interpolation='nearest')
    ims.append([im])
    printProgressBar(i+1,ITERATIONS, length = 50)
calc_time(start_time, start_timer())

#write data to file
with open("data.txt", "w") as f:
    for im in ims:
        f.write("%s" % i)
with open("graph.txt", "w") as f:
    f.write("active cells over iterations %s" % active)

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=10)
plt.show()

plt.plot(active_cells)
plt.show()

