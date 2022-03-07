# --------------------------------------
# COMP 361 - Introduction to Robotics
# Assignment 1: Grassfire Algorithm, taking inputs for number of rows, columns, obstacle probability, and starting column
# Nick Pio, 300170169
# Done using Python3.9.7, NumPy and matplotlib
# ---------------------------------------

#Using the class from the algorithm file
from GrassfireAlgorithm import Grassfire
#Importing necessary libraries, I'll be using the matplotlib library to create a GUI involving the 2D grid as shown on the handout
import numpy
import matplotlib.pyplot as plot
import matplotlib.animation as animation
import __future__

#User input for number of rows and columns
rows = int(input("Number of Rows: "))
cols = int(input("Number of Columns: "))
#Error for entering an invalid row or column amount
if rows < 8 or cols < 8:
    print("Error encountered, rows/cols must be 8 or greater")
    exit()
obstProb = float(input("Enter probability of a node being an obstacle(between 0.1 and 0.2): "))
#Error for entering an invalid obstacle probability percentage
if obstProb > 0.2 or obstProb < 0.1:
    print("Error encountered, probability must be between 0.1 and 0.2")
    exit()

#Initializing a grid and the associated colors for the nodes
Grassfire = Grassfire()
grid = Grassfire.gridGen(rows=rows, cols=cols, obstProb=obstProb)
colorNodes = Grassfire.colorNodes(grid)

figure = plot.figure()
grid_plot = plot.imshow(colorNodes, interpolation='nearest')
axes = grid_plot._axes
axes.grid(visible=True, ls='solid', color='peru', lw=3)
axes.set_xticklabels([])
axes.set_yticklabels([])

#Removing the tick marks from the grid
axes.tick_params(axis='both', which='both', bottom=False, top=False, left=False)

def set_axis_properties(rows, cols):
    #Setting up properties based on the number of rows and columns in the grid
    axes.set_xlim((0, cols))
    axes.set_ylim((rows,0))
    axes.set_xticks(numpy.arange(0, cols+1, 1))
    axes.set_yticks(numpy.arange(0, rows+1, 1))

    grid_plot.set_extent([0, cols, 0, rows])

set_axis_properties(rows, cols)

figure.canvas.mpl_disconnect(figure.canvas.manager.key_press_handler_id)

#Key press events
def on_key_press(event):
    global grid, rows, cols, obstProb
    #Hit escape to exit
    if event.key == 'escape':
        animation._stop()
        exit()

figure.canvas.mpl_connect('key_press_event', on_key_press)

def initialize_animation():
    Grassfire.gridReset(grid)
    colorNodes = Grassfire.colorNodes(grid)
    grid_plot.set_data(colorNodes)

def update_animation(dummyFrameArgument):
    colorNodes = Grassfire.colorNodes(grid)
    grid_plot.set_data(colorNodes)

animation = animation.FuncAnimation(figure, update_animation, init_func=initialize_animation, frames=Grassfire.pathfinding(grid), repeat=True, interval=150)

plot.ion()
plot.show(block=True)
