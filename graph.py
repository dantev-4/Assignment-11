"""
Student information for this assignment:

Replace <FULL NAME> with your name.
On my/our honor, <Dante Villarreal> and <FULL NAME>, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1:djv797
UT EID 2:
"""

import sys

# -----------------------PRINTING LOGIC, DON'T WORRY ABOUT THIS PART----------------------------
RESET_CHAR = "\u001b[0m"  # Code to reset the terminal color
COLOR_DICT = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
}
BLOCK_CHAR = "\u2588"  # Character code for a block


def colored(text, color):
    """Wrap the string with the color code."""
    color = color.strip().lower()
    if color not in COLOR_DICT:
        raise ValueError(color + " is not a valid color!")
    return COLOR_DICT[color] + text


def print_block(color):
    """Print a block in the specified color."""
    print(colored(BLOCK_CHAR, color) * 2, end="")

# -----------------------PRINTING LOGIC, DON'T WORRY ABOUT THIS PART----------------------------


class Node:
    """
    Represents a node in a singly linked list.
    """
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class StackError(Exception):
    pass


class Stack:
    def __init__(self):
        self._top = None
        self._size = 0

    def peek(self):
        if self.is_empty():
            raise StackError("Peek from empty stack.")
        return self._top.data

    def push(self, item):
        new_node = Node(item)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise StackError("Pop from empty stack.")
        removed_data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return removed_data

    def is_empty(self):
        return self._top is None

    def size(self):
        return self._size


class QueueError(Exception):
    pass


class Queue:
    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0

    def peek(self):
        if self.is_empty():
            raise QueueError("Peek from empty queue.")
        return self._front.data

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self._front = new_node
        else:
            self._rear.next = new_node
        self._rear = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise QueueError("Dequeue from empty queue.")
        front_data = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return front_data

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size


class ColoredVertex:
    def __init__(self, index, x, y, color):
        self.index = index
        self.color = color
        self.prev_color = color
        self.x = x
        self.y = y
        self.edges = []
        self.visited = False

    def add_edge(self, vertex_index):
        self.edges.append(vertex_index)

    def visit_and_set_color(self, color):
        self.visited = True
        self.prev_color = self.color
        self.color = color

    def __str__(self):
        return f"index: {self.index}, color: {self.color}, x: {self.x}, y: {self.y}"


class ImageGraph:
    def __init__(self, image_size):
        self.vertices = []
        self.image_size = image_size

    def print_image(self):
        img = [["black" for _ in range(self.image_size)] for _ in range(self.image_size)]
        for vertex in self.vertices:
            img[vertex.y][vertex.x] = vertex.color
        for line in img:
            for pixel in line:
                print_block(pixel)
            print()
        print(RESET_CHAR)

    def reset_visited(self):
        for vertex in self.vertices:
            vertex.visited = False

    def create_adjacency_matrix(self):
        size = len(self.vertices)
        matrix = [[0] * size for _ in range(size)]
        for vertex in self.vertices:
            for neighbor in vertex.edges:
                matrix[vertex.index][neighbor] = 1
        return matrix

    def bfs(self, start_index, color):
        self.reset_visited()
        print("Starting BFS; initial state:")
        self.print_image()

        queue = Queue()
        queue.enqueue(start_index)
        start_vertex = self.vertices[start_index]
        target_color = start_vertex.color

        while not queue.is_empty():
            current = queue.dequeue()
            vertex = self.vertices[current]

            if not vertex.visited and vertex.color == target_color:
                vertex.visit_and_set_color(color)
                for neighbor in vertex.edges:
                    queue.enqueue(neighbor)

        print("Final BFS state:")
        self.print_image()

    def dfs(self, start_index, color):
        self.reset_visited()
        print("Starting DFS; initial state:")
        self.print_image()

        stack = Stack()
        stack.push(start_index)
        start_vertex = self.vertices[start_index]
        target_color = start_vertex.color

        while not stack.is_empty():
            current = stack.pop()
            vertex = self.vertices[current]

            if not vertex.visited and vertex.color == target_color:
                vertex.visit_and_set_color(color)
                for neighbor in reversed(vertex.edges):
                    stack.push(neighbor)

        print("Final DFS state:")
        self.print_image()


def create_graph(data):
    lines = data.strip().split("\n")
    image_size = int(lines[0])
    num_vertices = int(lines[1])
    graph = ImageGraph(image_size)

    for i in range(2, 2 + num_vertices):
        x, y, color = lines[i].split(", ")
        graph.vertices.append(ColoredVertex(i - 2, int(x), int(y), color))

    num_edges = int(lines[2 + num_vertices])

    for i in range(3 + num_vertices, 3 + num_vertices + num_edges):
        v1, v2 = map(int, lines[i].split(", "))
        graph.vertices[v1].add_edge(v2)
        graph.vertices[v2].add_edge(v1)

    start_index, color = lines[3 + num_vertices + num_edges].split(", ")
    return graph, int(start_index), color


def main():
    data = sys.stdin.read()
    graph, start_index, color = create_graph(data)

    print("Adjacency Matrix:")
    adjacency_matrix = graph.create_adjacency_matrix()
    for row in adjacency_matrix:
        print(" ".join(map(str, row)))

    print("\nRunning BFS:")
    graph.bfs(start_index, color)

    print("\nResetting graph and running DFS:")
    graph, start_index, color = create_graph(data)
    graph.dfs(start_index, color)


if __name__ == "__main__":
    main()
