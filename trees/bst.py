class Node():
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.__red = True

    def setright(self, node):
        node.parent = self
        self.right = node

    def setleft(self, node):
        node.parent = self
        self.left = node

class BST():
    """
    red-black bst with comparable values
    """

    def __init__(self):
        self.head = None

    def insert(self, val):

        # find initial insert position
        node = Node(val)
        curr = self.head
        while curr.left and curr.right:
            if node.val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        if node.val < curr.val:
            curr.setleft(node)
        else:
            curr.setright(node)

        curr = node
        # RB correction
        while curr.parent.__red:
            # on left of grandparent
            if curr.parent == curr.parent.parent.left:
                # uncle is red, case 1
                if curr.parent.parent.right.__red:
                    uncle = curr.parent.parent.right
                    curr.parent.__red = False
                    uncle.__red = False
                    curr.parent.parent.__red = True
                    curr = curr.parent.parent
                # on right of parent, case 2
                elif curr == curr.parent.right:
                    curr = curr.parent
                    # ...
            # on right of grandparent (reflection)
            else:
                # ...
                continue
