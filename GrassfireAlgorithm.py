# --------------------------------------
# COMP 361 - Introduction to Robotics
# Assignment 1: Grassfire Algorithm, taking inputs for number of rows, columns, obstacle probability, and starting column
# Nick Pio, 300170169
# Done using Python3.9.7, NumPy, and matplotlib
# ---------------------------------------

#Importing the libraries to be used
#NumPy is important as it allows for easy creation of arrays
import random
import math
import numpy

class Grassfire:

    #Creating different variables for areas of the grid

    start = 0
    goal = -1
    untouched = -2
    obstacle = -3
    path = -4

    #Visited squares will have a number greater than 0

    #Each square needs to have a color associated
    #As in the image in the assignment handout:
    #GOAL = RED, START = GREEN, UNTOUCHED SQUARE = WHITE, OBSTACLE = BLACK, VISITED SQUARE = GREY, PATH FOUND = BLUE
    start_color = numpy.array([0, 0.70, 0])
    untouched_color = numpy.array([1, 1, 1])
    visited_color = numpy.array([0.66, 0.66, 0.66])
    obstacle_color = numpy.array([0,0,0])
    goal_color = numpy.array([0.80, 0, 0])
    path_color = numpy.array([0,0, 0.75])

    #Function for generating a random grid at size 8x8, with a 20% probability for a node to be an obstacle
    def gridGen(self, rows=8, cols=8, obstProb=0.2):
        obstGrid = numpy.random.random_sample((rows, cols))
        grid = Grassfire.untouched * numpy.ones((rows, cols), dtype=numpy.int)
        grid[obstGrid <= obstProb] = self.obstacle

        #Set start and goal nodes/squares at random
        self.set_start_goal(grid)
        return grid
    
    #Function to set a random start and goal node
    def set_start_goal(self, grid):
        (rows, cols) = grid.shape

        #Remove any start/goal nodes currently present
        grid[grid == Grassfire.start] = Grassfire.untouched
        grid[grid == Grassfire.goal] = Grassfire.untouched

        #Generate a random starting node
        validStart = False
        while validStart == False:
            startInput = int(input("Enter a position for the start node (less than number of cols): "))
            startI = startInput - 1
            if startI >= cols:
                print("Invalid number, must be less than number of columns")
                exit()
            startIs = numpy.unravel_index(startI, (rows, cols))
            #Starting node cannot be on an obstacle
            if grid[startIs] != Grassfire.obstacle:
                validStart = True
                grid[startIs] = Grassfire.start
        
        #Generate a random goal node
        validGoal = False
        while validGoal == False:
            goalI = random.randint(0, rows * cols - 1)
            goalIs = numpy.unravel_index(goalI, (rows, cols))
            #Goal cannot be on the starting square or an obstacle
            if grid[goalIs] != Grassfire.start and grid[goalIs] != Grassfire.obstacle:
                validGoal = True
                grid[goalIs] = Grassfire.goal

    #Create a colored grid based on the decided colors
    def colorNodes(self, grid):
        (rows, cols) = grid.shape
        colorNodes = numpy.zeros((rows, cols, 3), dtype = numpy.float)
        
        #Setting each node type to their corresponding color from above
        colorNodes[grid == Grassfire.start, :] = Grassfire.start_color #START = GREEN
        colorNodes[grid == Grassfire.goal, :] = Grassfire.goal_color #GOAL = RED
        colorNodes[grid == Grassfire.obstacle, :] = Grassfire.obstacle_color #OBSTACLES = BLACK
        colorNodes[grid == Grassfire.untouched, :] = Grassfire.untouched_color #UNTOUCHED NODES = WHITE
        colorNodes[grid == Grassfire.path, :] = Grassfire.path_color #PATH = BLUE
        colorNodes[grid > Grassfire.start, :] = Grassfire.visited_color #VISITED NODES = GREY
        return colorNodes
    
    #Function to check the nodes adjacent to the current node and see their value as set above
    def check(self, grid, node, depth):
        (rows, cols) = grid.shape

        #Tracking the nodes we've done
        nodesUpdated = 0

        #Examine adjacent nodes using the math import
        # right adjacent cell (col + 1), left adjacent cell (col - 1)
        # top adjacent cell (row - 1), below adjacent cell (row + 1)

        #Using a range of 4 because there are 4 adjacent nodes to whichever node we are on (presumably; this is why we check to see that we aren't going out of bounds)
        for square in range(4):
            rowCheck = node[0] + int(math.sin((math.pi/2) * square))
            colCheck = node[1] + int(math.cos((math.pi/2) * square))
            #Make sure we arent counting an area outside of the grid
            if (0 <= rowCheck < rows and 0 <= colCheck < cols) == False:
                continue
            #Make sure we aren't already at the goal node
            if grid[rowCheck, colCheck] == Grassfire.goal:
                return Grassfire.goal
            if (grid[rowCheck, colCheck] == Grassfire.untouched or grid[rowCheck, colCheck] > depth + 1):
                grid[rowCheck, colCheck] = depth + 1
                nodesUpdated += 1
        return nodesUpdated

    #Function used when the goal is reached, to determine where the last part of the path is
    def lastNode(self, grid, node, depth):
        (rows, cols) = grid.shape

        #Uses essentially the same parts as the check function
        for square in range(4):
            rowCheck = node[0] + int(math.sin((math.pi/2) * square))
            colCheck = node[1] + int(math.cos((math.pi/2) * square))
            

            #Again making sure we do not go out of the grid boundary
            if (0 <= rowCheck < rows and 0 <= colCheck < cols) == False:
                continue
            #If the node matches, set it to be part of the path
            if grid[rowCheck, colCheck] == depth:
                nextNode = (rowCheck, colCheck)
                grid[nextNode] = Grassfire.path
                return nextNode
    
    #Actual pathfinding function
    def pathfinding(self, grid):
        dict = {'grid': grid}

        def pathfindingGen():
            grid = dict['grid']
            depth = 0
            goalReached = False
            outofNodes = False

            #While we still have nodes left on the grid that haven't been touched, and we haven't reached the goal node
            while goalReached == False and outofNodes == False:
                nodesChanged = 0
                depthIs = numpy.where(grid == depth)
                nodesMatched = list(zip(depthIs[0], depthIs[1]))

                for node in nodesMatched:
                    adj = self.check(grid, node, depth)
                    if adj == Grassfire.goal:
                        goalReached = True
                        break
                    else:
                        nodesChanged += adj
                if nodesChanged == 0:
                    outofNodes = True
                elif goalReached == False:
                    depth += 1
                yield
            if goalReached:
                goalNode = numpy.where(grid == Grassfire.goal)
                backNode = (goalNode[0].item(), goalNode[1].item())

                while depth > 0:
                    nextNode = self.lastNode(grid, backNode, depth)
                    backNode = nextNode
                    depth -= 1
                    yield
        return pathfindingGen
    #Reset the grid back to untouched nodes
    def gridReset(self, grid):
        nodes_reset = ~((grid == Grassfire.obstacle) + (grid == Grassfire.goal) + (grid == Grassfire.start))
        grid[nodes_reset] = Grassfire.untouched
    



