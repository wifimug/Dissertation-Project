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

THRESHOLD = 1
RADIUS = 5
REFRACTORY = 40
ITERATIONS = 500



grid = np.zeros((200,200))
active_neighbours_grid = np.zeros((200,200))
active_cells = np.zeros(ITERATIONS)
active = 0


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

                for k in range(len(x_arr[step])):
                    new_neighbours_grid[y_arr[step][k]][x_arr[step][k]] += 1

            #when current cell is ON
            if curr_grid[i][j] > 0:
                new_grid[i][j] -= 1
                if new_grid[i][j] == 0:
                    for k in range(len(x_arr[step])):
                        new_neighbours_grid[y_arr[step][k]][x_arr[step][k]] -= 1  
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
    for y in range(len(init_grid)):
        for x in range(len(init_grid[0])):
            x_temp, y_temp = points_in_circle(radius, x, y, len(init_grid[0]), len(init_grid))

            x_arr.append(x_temp)
            y_arr.append(y_temp)

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
    for y in range(y0 - radius, y0 + radius + 1):
        for x in range(x0 - radius, x0 + radius + 1):
            if (x < xub and x >= 0 and y < yub and y >= 0) and not (y == y0 and x == x0):
                if ((y - y0)**2 + (x - x0)**2)**0.5 <= radius:
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



def print_progress_bar(iteration, total, length):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent}% Complete', end = "\r")
    if iteration == total: 
        print()



def left_atrium_setup():
    #animate frame by frame
    fig, ax = plt.subplots()
    ims = []

    x_arr, y_arr = get_neighbours_array(grid, RADIUS)
    #print(x_arr[0], y_arr[0])


    c = 0
    for i in range(10):
        for j in range(10):
            rng = random.randint(0,1)
            if rng == 1:
                grid[i][j] = REFRACTORY
                active += 1

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            sum = 0
            for n in range(len(x_arr[c])):
                if grid[y_arr[c][n]][x_arr[c][n]] > 0:
                    sum += 1
            active_neighbours_grid[i][j] += sum
            c += 1


            

    # grid[0][0] = 20
    # for i in range(len(x_arr[0])):
    #     active_neighbours_grid[y_arr[0][i]][x_arr[0][i]] += 1


    # defining electrically inactive points
    # mitral valve
    for i in range(len(grid)-1, len(grid)-82-1, -1):
        for j in range(len(grid)):
            grid[i][j] = -1

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
    return fig, ax, ims







#print("x_arr length:", len(x_arr))

def main():
    fig, ax, ims = left_atrium_setup()
    start_time = start_timer()
    print_progress_bar(0, ITERATIONS, length = 50)
    for i in range(ITERATIONS):
        new_grid, new_active_neighbours_grid, active = update(grid, active_neighbours_grid, x_arr, y_arr)
        active_cells[i] = active/(len(grid[0])*len(grid[1]))
        im = ax.imshow(grid, animated=True, interpolation='nearest')
        ims.append([im])
        grid = new_grid
        active_neighbours_grid = new_active_neighbours_grid
        print_progress_bar(i+1,ITERATIONS, length = 50)
    calc_time(start_time, start_timer())

    # #write data to file
    # with open("data.txt", "w") as f:
    #     for im in ims:
    #         f.write("%s" % im)
    # with open("graph.txt", "w") as f:
    #     for i in range(len(active_cells)):
    #         f.write("active: %s" % active_cells[i])

    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=100)
    plt.show()



    plt.plot(active_cells)

    plt.show()

main()
