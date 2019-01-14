class Node():
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.__red = False

class BST():
    """
    red-black bst
    """

    def __init__(self):
        self.head = None

    def insert(self):
