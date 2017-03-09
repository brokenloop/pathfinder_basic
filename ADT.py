class Node(object):
    """ A Node in a Linked List
    """

    def __init__(self, element=None):
        self.__next = None
        self.__element = element

    def get_next(self):
        return self.__next

    def get_element(self):
        return self.__element

    def set_next(self, next):
        self.__next = next

    def set_element(self, element):
        self.__element = element


class LinkedList(object):
    """ The List itself
    """

    def __init__(self, node=None):
        self.__first = node

    def head(self):
        return self.__first

    def add_tail(self, node):
        current = self.head()
        while not current.get_next() == None:
            #             if current.get_next() == None:
            #                 current.set_next(node)
            current = current.get_next()
        current.set_next(node)

    def add_head(self, node):
        node.set_next(self.head())
        self.__first = node

    def remove_head(self):
        self.__first = self.__first.get_next()

    def __repr__(self):
        result = ""
        current = self.head()
        while not (current is None):
            result += " -> " + str(current)
            current = current.get_next()
        return result


class ArrayStack:
    def __init__(self):
        self.size = 0
        self.__contents = []

    def push(self, elem):
        self.__contents.append(elem)
        self.size += 1

    def pop(self):
        if self.size > 0:
            del self.__contents[-1]
            self.size -= 1
        else:
            pass

    def peek(self):
        if self.size > 1:
            return self.__contents[self.size - 1]
        else:
            return None

    def print_stack(self):
        while self.size > 1:
            print(self.peek())
            self.pop()


class LinkedStack:
    def __init__(self):
        self.__contents = LinkedList()

    def push(self, elem):
        self.__contents.add_head(Node(elem))

    def pop(self):
        self.__contents.remove_head()

    def peek(self):
        if self.__contents.head():
            return self.__contents.head().get_element()
        else:
            return None


if __name__ == "__main__":

    l = LinkedList()
    l.add_head(Node("toto"))
    l.add_head(Node(2))
    l.add_tail(Node(9))
    l.add_tail(Node(67))
    l.add_head(Node(1))
    l.add_tail(Node("tail"))
    print(l.head().get_next())
