import os
from copy import deepcopy
from pprint import *
from src import ADT


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for x in range(height)] for y in range(width)]

    def make_walls(self, mylist):
        for coord in mylist:
            x = int(coord[0])
            y = int(coord[1])
            self.grid[x][y] = 1

    def is_feasible(self, x, y):
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
        return self.__location

    def move(self, x, y):
        self.__location = []


    def find_path(self, world, current_path, location):

        if self.goal_reached:
            return False

        if not world.is_feasible(location[0], location[1]):
            return False

        if location == self.__goal:
            self.goal_reached = True
            return current_path

        east = [location[0], location[1] + 1]
        west = [location[0], location[1] - 1]
        north = [location[0] + 1, location[1]]
        south = [location[0] - 1, location[1]]

        world.make_walls([[location[0], location[1]]])
        path_copy = deepcopy(current_path)
        path_copy.push(location)
        return (self.find_path(world, path_copy, north) or self.find_path(world, path_copy, south) or
                self.find_path(world, path_copy, east) or self.find_path(world, path_copy, west))


def parse_file(fname):
    if os.path.exists(fname):
        buffer = open(fname).read().split("\n")
    else:
        return "Error! File does not exist"

    height = buffer[0][0]
    width = buffer[0][2]
    walls = []
    robot_location = None
    goal = None

    for i in range(1, len(buffer) -1):
        if buffer[i][0] == "w":
            walls.append([buffer[i][2], buffer[i][4]])
        elif buffer[i][0:4] == "r2d2":
            robot_location = [int(buffer[i][5]), int(buffer[i][7])]
        elif buffer[i][0:4] == "goal":
            goal = [int(buffer[i][5]), int(buffer[i][7])]

    return int(height), int(width), walls, robot_location, goal


def main():
    height, width, walls, robot_location, goal = parse_file("joe_test.txt")
    print("Goal:", goal)
    world = World(height, width)
    # world.make_walls([[0, 0], [0,1], [0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]])
    world.make_walls(walls)


    robot = Robot(robot_location, goal)
    start_path = ADT.LinkedStack()
    start_path.push(robot.get_location())

    pprint(world.grid)
    path = robot.find_path(world, start_path, robot.get_location())
    if path:
        print("Path found! Size:", path.size)
        print("Route:", path.print_stack())
        pprint(world.grid)

    else:
        print("No path found")
        pprint(world.grid)



if __name__=="__main__":
    main()



