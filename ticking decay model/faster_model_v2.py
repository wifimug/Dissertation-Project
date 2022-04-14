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
- 1 array of total active neighbour states for each cell
> active neighbour states changed each iteration instead
  of calculating number of active neighbours each iteration
> neighbourhood adjustable based on radius set
'''

THRESHOLD = 10
RADIUS = 5
REFRACTORY = 40



def update(curr_grid, active_neighbours_grid, x_arr, y_arr):
    """
    Updates the state of the current grid given
    the number of active neighbours in a circle radius
    given the x and y coordinates of points in the circle

    return: state of the new grid
    """
    new_grid = copy.deepcopy(curr_grid)
    new_neighbours_grid = copy.deepcopy(active_neighbours_grid)
    step = 0
    active = 0
    for i in range(len(curr_grid)):
        for j in range(len(curr_grid[0])):
            #when current cell is OFF
            if curr_grid[i][j] == 0 and active_neighbours_grid[i][j] >= THRESHOLD:
                new_grid[i][j] = REFRACTORY
                active += 1
                x = x_arr[step]
                y = y_arr[step]
                for k in range(len(x)):
                    new_neighbours_grid[y[k]][x[k]] += 1

            #when current cell is ON
            if curr_grid[i][j] > 0:
                new_grid[i][j] -= 1
                if new_grid[i][j] == 0:
                    x = x_arr[step]
                    y = y_arr[step]
                    for k in range(len(x)):
                        new_neighbours_grid[y[k]][x[k]] -= 1
                        #print("hi")
                    
            
            step += 1
    return new_grid, new_neighbours_grid, active




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
            x_temp, y_temp = points_in_circle(radius, i, j, len(init_grid[0]), len(init_grid))

            x_arr.append(x_temp)
            y_arr.append(y_temp)

    #print(x_arr[:100])
    #print(y_arr[:100])
    return x_arr, y_arr


def points_in_circle(radius, x0, y0, xub, yub):
    """
    Takes the centre of the circle and the upper-bound
    limits of the display grid and calculates all the 
    points in the circle excluding the centres and points 
    not on the display grid

    return: array of x coordinates and array of y coordinates
            of points for a given centre
    """
    x_arr = []
    y_arr = []
    x_ = np.arange(x0 - radius - 1, x0 + radius + 1, dtype=int)
    y_ = np.arange(y0 - radius - 1, y0 + radius + 1, dtype=int)
    x, y = np.where((x_[:,np.newaxis] - x0)**2 + (y_ - y0)**2 <= radius**2)
    for x, y in zip(x_[x], y_[y]):
        if (x < xub and x >= 0) and (y < yub and y >= 0):
            if not (x == x0 and y == y0):
                x_arr.append(x)
                y_arr.append(y)
    return x_arr, y_arr





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
x_arr, y_arr = get_neighbours_array(grid, RADIUS)
#print(x_arr[0], y_arr[0])
active_neighbours_grid = np.zeros((200,200))

active = 0
for i in range(10):
    for j in range(10):
        rng = random.randint(0,1)
        if rng == 1:
            grid[i][j] = 20
            active += 1
            for r in range(RADIUS):
                if (r-j)**2+(r-i)**2 <= RADIUS**2:
                    active_neighbours_grid[i+r][j+r] += 1
                    active_neighbours_grid[i][j+r] += 1
                    active_neighbours_grid[i+r][j] += 1
                    if not(i < r or j < r):
                        
                        active_neighbours_grid[i-r][j-r] += 1
                        active_neighbours_grid[i+r][j-r] += 1
                        active_neighbours_grid[i-r][j+r] += 1
                        active_neighbours_grid[i-r][j] += 1
                        active_neighbours_grid[i][j-r] += 1
# grid[0][0] = 20

# defining electrically inactive points
#mitral valve
# for i in range(len(grid)-1):
#     for j in range(len(grid)-1, len(grid)-82-1, -1):
#         grid[j][i] = -2

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


print("x_arr length:", len(x_arr))


start_time = start_timer()
printProgressBar(0, ITERATIONS, length = 50)
for i in range(ITERATIONS):
    if i == 0:
        ax.imshow(grid, animated=True, interpolation='nearest')
    grid, active_neighbours_grid, active = update(grid, active_neighbours_grid, x_arr, y_arr)
    #grid = new
    active_cells[i] = active
    im = ax.imshow(grid, animated=True, interpolation='nearest')
    ims.append([im])
    printProgressBar(i+1,ITERATIONS, length = 50)
calc_time(start_time, start_timer())

#write data to file
with open("data.txt", "w") as f:
    for im in ims:
        f.write("%s" % im)
with open("graph.txt", "w") as f:
    f.write("active cells over iterations %s" % active)

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=10)
plt.show()

plt.plot(active_cells)
plt.show()

