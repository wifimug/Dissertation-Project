# Making a Faster Cellular Automaton #

## Aim to precompute as much as possible before running the recursive updates ## 
Find the coordinates of the neighbours of each cell and store as a lookup table.
Faster than computing the neighbouring cells each iteration.

## Comparison ##
Using the settings: 
Radius = 5, Threshold = 3, Refractory = 10
Iterations = 500

Faster model takes around 1 minute to finish.
Previous model takes around 3 minutes to finish.

Using the settings:
Radius = 10, Threshold = 3, Refractory = 20
Iterations = 500

Faster model takes 13.6 mins to finish.
Previous model takes 17 mins to finish. (and it doesn't work)


Using the settings:
Radius = 5, Threshold = 2, Refractory = 20
Iterations = 500

Faster model takes 7.6 mins to finish