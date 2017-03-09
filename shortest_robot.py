import os
from copy import deepcopy
from pprint import *
from src import linked_list



class ArrayStack:
    def __init__(self):
        self.size = 0
        self.__contents = []

    def push(self, elem):
        self.__contents.append(elem)
        self.size += 1

    def pop(self):
        self.__contents.pop(1)
        self.size -= 1

    def peek(self):
        if self.size > 0:
            return self.__contents[self.size - 1]
        else:
            return None

    def print_stack(self):
        while self.size > 1:
            print(self.peek())
            self.pop()


class LinkedStack:
    def __init__(self):
        self.__contents = linked_list.LinkedList()

    def push(self, elem):
        self.__contents.add_head(linked_list.Node(elem))

    def pop(self):
        self.__contents.remove_head()

    def peek(self):
        if self.__contents.head():
            return self.__contents.head().get_element()
        else:
            return None


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
        if self.grid[x][y] == 0:
            return True
        else:
            return False


class Robot:
    def __init__(self, location, goal):
        self.__location = location
        self.__goal = goal
        self.path_list = []
        self.path_count = 0
        self.path_length = None

    def get_location(self):
        return self.__location


    def find_path(self, world, current_path, location):

        if self.path_length:
            if len(current_path) >= self.path_length:
                return False

        if not world.is_feasible(location[0], location[1]):
            return False

        if location in current_path:
            return False

        if location == self.__goal:
            self.path_count += 1
            self.path_list.append(current_path)
            self.path_length = len(current_path)
            print("Current smallest:", self.path_length)
            return True

        path_copy = list(current_path)
        path_copy.append(location)

        east = [location[0], location[1] + 1]
        west = [location[0], location[1] - 1]
        north = [location[0] + 1, location[1]]
        south = [location[0] - 1, location[1]]
        #
        self.find_path(world, path_copy, north)
        self.find_path(world, path_copy, south)
        self.find_path(world, path_copy, east)
        self.find_path(world, path_copy, west)

        return False


    def compare_paths(self):
        smallest = self.path_list[0]

        for path in self.path_list:
            if len(path) < len(smallest):
                smallest = path

        return smallest, len(smallest)

    def direction(self, x1, y1, x2, y2):
        pass


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
    height, width, walls, robot_location, goal = parse_file("world1.txt")

    print("Goal:", goal)


    world = World(height, width)
    world.make_walls(walls)

    robot = Robot(robot_location, goal)
    start_path = []

    pprint(world.grid)
    robot.find_path(world, start_path, robot.get_location())
    try:
        smallest, len_smallest = robot.compare_paths()
        print("Smallest path is", smallest, "\nTotal:", len_smallest, "squares")
    except:
        print("No path")

if __name__=="__main__":
    main()




