class Queue:
    """
    A basic FIFO (First-In-First-Out) queue implementation using a list.
    """

    def __init__(self, startValues=None):
        """
        Initialize the queue with optional starting values.
        :param startValues: Optional list of initial values.
        """
        if startValues is None:
            startValues = []
        if not isinstance(startValues, list):
            raise TypeError("startValues must be a list")
        self.data = startValues

    def dequeue(self):
        """
        Remove and return the first item from the queue.
        :return: The dequeued value.
        :raises IndexError: If the queue is empty.
        """
        if len(self.data) > 0:
            return self.data.pop(0)
        raise IndexError("dequeue from empty queue")

    def enqueue(self, value):
        """
        Add a value to the end of the queue.
        :param value: The value to add.
        :return: The value added.
        """
        self.data.append(value)
        return value

    def enqueue_list(self, values):
        """
        Add a list of values to the end of the queue.
        :param values: List of values to add.
        :return: The list of values added.
        :raises TypeError: If values is not a list.
        """
        if not isinstance(values, list):
            raise TypeError("values must be a list")
        self.data.extend(values)
        return values

    def length(self):
        """
        Return the number of items in the queue.
        :return: Length of the queue.
        """
        return len(self.data)


class Stack:
    """
    A basic LIFO (Last-In-First-Out) stack implementation using a list.
    """

    def __init__(self, startValues=None):
        """
        Initialize the stack with optional starting values.
        :param startValues: Optional list of values (not added to stack).
        """
        if startValues is None:
            startValues = []
        if not isinstance(startValues, list):
            raise TypeError("startValues must be a list")
        self.data = []

    def push(self, value):
        """
        Push a value onto the stack.
        :param value: The value to add.
        """
        self.data.append(value)

    def pop(self):
        """
        Remove and return the top item from the stack.
        :return: The popped value.
        :raises IndexError: If the stack is empty.
        """
        if len(self.data) > 0:
            return self.data.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        """
        Return the top value without removing it.
        :return: The top value.
        :raises IndexError: If the stack is empty.
        """
        if len(self.data) > 0:
            return self.data[-1]
        raise IndexError("peek from empty stack")

    def length(self):
        """
        Return the number of items in the stack.
        :return: Length of the stack.
        """
        return len(self.data)


class TreeNode:
    """
    A node in a binary search tree.
    """

    def __init__(self, value):
        """
        Create a new tree node.
        :param value: The value of the node.
        """
        self.left = None
        self.right = None
        self.value = value

    def insert(self, value):
        """
        Insert a new value into the binary search tree.
        :param value: The value to insert.
        """
        if value < self.value:
            if self.left is None:
                self.left = TreeNode(value)
            else:
                self.left.insert(value)
        if value > self.value:
            if self.right is None:
                self.right = TreeNode(value)
            else:
                self.right.insert(value)

    def inorder_traversal(self):
        """
        Print the tree values in in-order traversal.
        """
        if self.left:
            self.left.inorder_traversal()
        print(self.value)
        if self.right:
            self.right.inorder_traversal()

    def preorder_traversal(self):
        """
        Print the tree values in pre-order traversal.
        """
        print(self.value)
        if self.left:
            self.left.preorder_traversal()
        if self.right:
            self.right.preorder_traversal()

    def find(self, value):
        """
        Search for a value in the tree.
        :param value: The value to search.
        :return: Tuple (True, node) if found, else False.
        """
        if value < self.value:
            if self.left is None:
                return False
            else:
                return self.left.find(value)
        elif value > self.value:
            if self.right is None:
                return False
            else:
                return self.right.find(value)

        if value == self.value:
            return True, self


class Node:
    """
    A node in a singly linked list.
    """

    def __init__(self, value):
        """
        Create a new node.
        :param value: Value to store.
        """
        self.value = value
        self.next = None


class LinkedList:
    """
    A basic singly linked list.
    """

    def __init__(self):
        """
        Create an empty linked list.
        """
        self.head = None

    def __repr__(self):
        """
        String representation of the list.
        """
        if self.head is None:
            return "[]"
        last = self.head
        return_string = f"[{last.value}"
        while last.next:
            last = last.next
            return_string += f", {last.value}"
        return_string += "]"
        return return_string

    def __contains__(self, item):
        """
        Check if an item is in the list.
        :param item: The value to search.
        :return: True if found, else False.
        """
        last = self.head
        while last is not None:
            if last.value == item:
                return True
            last = last.next
        return False

    def __len__(self):
        """
        Return the length of the list.
        """
        last = self.head
        counter = 0
        while last is not None:
            counter += 1
            last = last.next
        return counter

    def append(self, value):
        """
        Add a value to the end of the list.
        :param value: Value to add.
        """
        if self.head is None:
            self.head = Node(value)
        else:
            last = self.head
            while last.next:
                last = last.next
            last.next = Node(value)

    def prepend(self, value):
        """
        Add a value to the start of the list.
        :param value: Value to add.
        """
        first_node = Node(value)
        first_node.next = self.head
        self.head = first_node

    def insert(self, value, index):
        """
        Insert a value at a specific index.
        :param value: Value to insert.
        :param index: Position to insert at.
        :raises ValueError: If index is out of bounds.
        """
        if index == 0:
            self.prepend(value)
        else:
            if self.head is None:
                raise ValueError("Index out of bounds")
            last = self.head
            for i in range(index - 1):
                if last.next is None:
                    raise ValueError("Index out of bounds")
                last = last.next
            new_node = Node(value)
            new_node.next = last.next
            last.next = new_node

    def delete(self, value):
        """
        Delete the first occurrence of a value from the list.
        :param value: Value to delete.
        """
        last = self.head
        if last is not None:
            if last.value == value:
                self.head = last.next
            else:
                while last.next:
                    if last.next.value == value:
                        last.next = last.next.next
                        break
                    last = last.next

    def pop(self, index):
        """
        Remove the node at a specific index.
        :param index: Index to remove.
        :raises ValueError: If index is out of bounds.
        """
        if self.head is None:
            raise ValueError("Index out of bounds")
        if index == 0:
            self.head = self.head.next
            return
        last = self.head
        for i in range(index - 1):
            if last.next is None:
                raise ValueError("Index out of bounds")
            last = last.next
        if last.next is None:
            raise ValueError("Index out of bounds")
        last.next = last.next.next

    def get(self, index):
        """
        Get the value at a specific index.
        :param index: Index to access.
        :return: Value at the index.
        :raises ValueError: If index is out of bounds.
        """
        if self.head is None:
            raise ValueError("Index out of bounds")
        last = self.head
        for i in range(index):
            if last is None:
                raise ValueError("Index out of bounds")
            last = last.next
        return last.value
