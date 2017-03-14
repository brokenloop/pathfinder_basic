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

    def get_location(self):
        """ Returns the location of the robot
        """
        return self.__location


    def find_path(self, world, current_path, location):
        """ This program recursively searches for self.goal
            detailed explanation can be found in the report.
        """

        # Checks whether goal has already been found
        if self.goal_reached:
            return False

        # Checks whether location is feasible
        if not world.is_feasible(location[0], location[1]):
            return False

        # Checks whether location is goal
        # If true, it lets other functions know with self.goal_reached
        if location == self.__goal:
            self.goal_reached = True
            return current_path

        # Marks location as impassable, creates copy of current_path
        world.make_walls([[location[0], location[1]]])
        path_copy = deepcopy(current_path)
        path_copy.push(location)

        east = [location[0], location[1] + 1]
        west = [location[0], location[1] - 1]
        north = [location[0] + 1, location[1]]
        south = [location[0] - 1, location[1]]

        # Recursively calls self in all directions
        return (self.find_path(world, path_copy, north) or
                self.find_path(world, path_copy, south) or
                self.find_path(world, path_copy, east) or
                self.find_path(world, path_copy, west))


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


def main(fname):
    """ Main function of the program
    """

    # parse file for information
    height, width, walls, robot_location, goal = parse_file(fname)

    # initialize world
    world = World(height, width)
    world.make_walls(walls)

    # initialise robot & path stack
    robot = Robot(robot_location, goal)
    start_path = ADT.LinkedStack()
    start_path.push(robot.get_location())

    print("Robot location:", robot_location)
    print("Goal:", goal)
    pprint(world.grid)

    # call path-finding algorithm
    path = robot.find_path(world, start_path, robot.get_location())
    if path:
        print("Path found! Size:", path.size)
        print("Route:", path.print_stack())

    else:
        print("No path found")


if __name__=="__main__":
    main("world1.txt")


