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

    def get_location(self):
        return self.__location


    def goal_reached(self):
        return self.__location == self.__goal


    def move(self, x, y):
        self.__location = [x, y]


    def find_feasible(self, world, prev_loc, location):
        east = [location[0], location[1] + 1]
        west = [location[0], location[1] - 1]
        north = [location[0] + 1, location[1]]
        south = [location[0] - 1, location[1]]

        feasible = []

        for direction in [north, south, east, west]:
            if (direction != prev_loc) and world.is_feasible(direction[0], direction[1]):
                feasible.append(direction)

        return feasible

    # def find_path(self, world, current_path, location):
    #
    #     if not world.is_feasible(location[0], location[1]):
    #         return None
    #
    #     if location == self.__goal:
    #         print("path found!")
    #         return current_path
    #
    #     # previous_location = current_path.peek()
    #
    #     # feasible = self.find_feasible(world, previous_location, location)
    #
    #     if feasible:
    #         print("Feasible directions:", feasible)
    #         path_copy = deepcopy(current_path)
    #         path_copy.push(location)
    #         print(path_copy.peek())
    #         for direction in feasible:
    #             self.find_path(world, path_copy, direction)
    #     else:
    #         print("Process Killed")
    #         return False


    def find_path(self, world, current_path, location):

        print(location)

        if not world.is_feasible(location[0], location[1]):
            return False

        if self.path_count >= 50:
            return True

        if location == self.__goal:
            print("path found!")
            self.path_count += 1
            self.path_list.append(current_path)
            return True

        east = [location[0], location[1] + 1]
        west = [location[0], location[1] - 1]
        north = [location[0] + 1, location[1]]
        south = [location[0] - 1, location[1]]

        world.make_walls([[location[0], location[1]]])
        path_copy = deepcopy(current_path)
        path_copy.push(location)
        return (self.find_path(world, path_copy, north) or self.find_path(world, path_copy, south) or
                self.find_path(world, path_copy, east) or self.find_path(world, path_copy, west))

    def compare_paths(self):
        smallest = self.path_list[0]

        for path in self.path_list:
            print(path.size)
            if path.size < smallest.size:
                smallest = path

        return smallest


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
    start_path = ArrayStack()
    start_path.push(robot.get_location())

    pprint(world.grid)
    robot.find_path(world, start_path, robot.get_location())
    print("Path is", robot.compare_paths().size, "squares")



if __name__=="__main__":
    main()




