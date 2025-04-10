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

class Node:
    def __init__(self,value):
        self.value = value
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None
    def __repr__(self):
        if self.head is None: return "[]"
        else: last = self.head
        return_string = f"[{last.value}"

        while last.next:
            last = last.next
            return_string += f", {last.value}"
        return_string += "]"
        return return_string
    def __contains__(self, item):
        last = self.head
        while last is not None:
            if last.value == item: return True
            last = last.next
        return False
    def __len__(self):
        last = self.head
        counter = 0
        while last is not None:
            counter += 1
            last = last.next
        return counter
    def append(self,value):
        if self.head is None:
            self.head = Node(value)
        else:
            last = self.head
            while last.next:
                last = last.next
            last.next = Node(value)
    def prepend(self,value):
        first_node = Node(value)
        first_node.next = self.head
        self.head = first_node
    def insert(self,value,index):
        if index == 0: self.prepend(value)
        else:
            if self.head is None:
                raise ValueError("Index out of bounds")
            else:
                last = self.head
                for i in range(index-1):
                    if last.next is None: raise ValueError("Index out of bounds")
                    last = last.next
                new_node = Node(value)
                new_node.next = last.next
                last.next = new_node

    def delete(self,value):
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

    def pop(self,index):
        if self.head is None:
            raise ValueError("Index out of bounds")
        else:
            last = self.head
            for i in range(index-1):
                if last.next is None: raise ValueError("Index out of bounds")
                last = last.next

            if last.next is None:
                raise ValueError("Index out of bounds")
            else:
                last.next = last.next.next
    def get(self,index):
        if self.head is None: raise ValueError("Index out of bounds")
        else:
            last = self.head
            for i in range(index):
                if last is None: raise ValueError("Index out of bounds")
                last = last.next
            return last.value

