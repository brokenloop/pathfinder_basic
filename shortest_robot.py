import os
import re
from copy import deepcopy
from pprint import *
from src import ADT


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for x in range(height)] for y in range(width)]

    def make_walls(self, mylist):
        """ This function takes a list or coordinates (mylist) and uses them to add walls to self.grid
            Walls are stored as 1, whereas open space is stored as 0
         """
        for coord in mylist:
            x = int(coord[0])
            y = int(coord[1])
            self.grid[x][y] = 1

    def unmake_walls(self, mylist):
        """ This function takes a list or coordinates (mylist) and uses them to remove walls from self.grid
            Walls are stored as 1, whereas open space is stored as 0
         """
        for coord in mylist:
            x = int(coord[0])
            y = int(coord[1])
            self.grid[x][y] = 0

    def is_feasible(self, x, y):
        """ This function checks that the coordinates x and y refer to a
            coordinate within the grid that is passable (0)
        """
        if not (x >= 0 and x < self.width):
            return False
        if not (y >= 0 and y < self.height):
            return False
        return self.grid[x][y] == 0


class Robot:
    def __init__(self, location, goal):
        self.__location = location
        self.__goal = goal
        self.goal_reached = False
        self.path_list = []
        self.smallest = None
        self.smallest_length = None


    def get_location(self):
        """ Returns the location of the robot
        """
        return self.__location


    def find_path(self, world, current_path, location):
        """ This program recursively searches for self.goal
            detailed explanation can be found in the report.
        """

        # checks that this path isn't longer than the shortest path
        if self.smallest != None:
            if current_path.size >= self.smallest.size:
                return False

        # checks that this location is feasible
        if not world.is_feasible(location[0], location[1]):
            return False

        # checks whether this location is the goal
        # if it is, information is stored in self.smallest and self.path_length
        if location == self.__goal:
            path_copy = deepcopy(current_path)
            self.smallest = path_copy
            self.path_length = path_copy.size
            print("Current smallest:", self.smallest.size)
            return False


        east = [location[0], location[1] + 1]
        west = [location[0], location[1] - 1]
        north = [location[0] + 1, location[1]]
        south = [location[0] - 1, location[1]]

        # push location to stack, mark location impassable
        current_path.push(location)
        world.make_walls([[location[0], location[1]]])

        # call function recursively in all directions
        self.find_path(world, current_path, north)
        self.find_path(world, current_path, south)
        self.find_path(world, current_path, east)
        self.find_path(world, current_path, west)

        # pop location from stack, mark location as passable
        current_path.pop()
        world.unmake_walls([location])
        return False


def parse_file(fname):
    """ This function uses regex to parse the input file for variables to be used in the program
    """

    # open file
    if os.path.exists(fname):
        buffer = open(fname).read().split("\n")
    else:
        return "Error! File does not exist"

    # initialise variables
    height, width = buffer[0].split("x")
    walls = []
    robot_location = None
    goal = None

    for i in range(1, len(buffer) -1):

        # check for wall coordinates
        wall_pattern = re.compile("\s*w\s*(-{0,1}\d+)\s*,*\s*(-{0,1}\d+)\s*")
        if wall_pattern.match(buffer[i]):
            wall_contents = wall_pattern.match(buffer[i]).groups()
            walls.append([int(wall_contents[0]), int(wall_contents[1])])

        # check for robot coordinates
        robot_pattern = re.compile("\s*r2d2\s*(-{0,1}\d+)\s*,*\s*(-{0,1}\d+)\s*")
        if robot_pattern.match(buffer[i]):
            robot_contents = robot_pattern.match(buffer[i]).groups()
            robot_location = [int(robot_contents[0]), int(robot_contents[1])]

        # check for goal coordinates
        goal_pattern = re.compile("\s*goal\s*(-{0,1}\d+)\s*,*\s*(-{0,1}\d+)\s*")
        if goal_pattern.match(buffer[i]):
            goal_contents = goal_pattern.match(buffer[i]).groups()
            goal = [int(goal_contents[0]), int(goal_contents[1])]

    return int(height), int(width), walls, robot_location, goal


def main():
    """ Main function for the program
    """
    # parse input file, assign contents to variables
    height, width, walls, robot_location, goal = parse_file("world1.txt")

    # initialise world object
    world = World(8, 8)
    world.make_walls(walls)

    # initialise robot object
    robot = Robot(robot_location, [5, 5])
    start_path = ADT.LinkedStack()
    start_path.push(robot_location)

    # print world & robot info
    print("robot_location:", robot_location)
    print("Goal:", goal)
    pprint(world.grid)

    # find shortest path
    robot.find_path(world, start_path, robot.get_location())
    if robot.smallest:
        print("Smallest path: ", robot.smallest.print_stack())
    else:
        print("No path found")


if __name__=="__main__":
    main()


