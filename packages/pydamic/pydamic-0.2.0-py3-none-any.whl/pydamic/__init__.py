# pydamic/__init__.py
class Queue:
    def __init__(self, startValues=None):
        if startValues is None:
            startValues = []
        if not isinstance(startValues, list):
            raise TypeError("startValues must be a list")
        self.data = startValues

    def dequeue(self):
        if len(self.data) > 0:
            return self.data.pop(0)
        raise IndexError("dequeue from empty queue")

    def enqueue(self, value):
        self.data.append(value)
        return value

    def enqueue_list(self, values):
        if not isinstance(values, list):
            raise TypeError("values must be a list")
        self.data.extend(values)
        return values

    def length(self):
        return len(self.data)


class Stack:
    def __init__(self, startValues=None):
        if startValues is None:
            startValues = []
        if not isinstance(startValues, list):
            raise TypeError("startValues must be a list")
        self.data = []

    def push(self, value):
        self.data.append(value)

    def pop(self):
        if len(self.data) > 0:
            return self.data.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if len(self.data) > 0:
            return self.data[-1]
        raise IndexError("peek from empty stack")

    def length(self):
        return len(self.data)
class TreeNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
    def insert(self,value):
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
        if self.left:
            self.left.inorder_traversal()
        print(self.value)
        if self.right:
            self.right.inorder_traversal()
    def preorder_traversal(self):
        print(self.value)

        if self.left:
            self.left.preorder_traversal()
        if self.right:
            self.right.preorder_traversal()

    def find(self,value):
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
            return True,self

