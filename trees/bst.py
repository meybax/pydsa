class Node():
    def __init__(self, val, left=None, right=None, parent=None, __isred=True):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.__red = __isred

    def setright(self, node):
        if node:
            node.parent = self
        self.right = node

    def setleft(self, node):
        if node:
            node.parent = self
        self.left = node

class BST():
    """
    red-black bst with comparable values
    """

    def __init__(self):
        self.head = None

    def rotateright(self, curr):
        new_root = curr.left
        curr.setleft(new_root.right)
        if not curr.parent:
            self.head = new_root
            new_root.parent = None
        elif curr == curr.parent.left:
            curr.parent.setleft(new_root)
        else:
            curr.parent.setright(new_root)
        new_root.setright(curr)

    def rotateleft(self, curr):
        new_root = curr.right
        curr.setright(new_root.left)
        if not curr.parent:
            self.head = new_root
            new_root.parent = None
        elif curr == curr.parent.left:
            curr.parent.setleft(new_root)
        else:
            curr.parent.setright(new_root)
        new_root.setleft(curr)

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
                uncle = curr.parent.parent.right
                onLeft = True
                rotate = self.rotateright()
            # on right of grandparent
            else:
                uncle = curr.parent.parent.left
                onLeft = False
                rotate = self.rotateleft()

            # uncle is red, case 1
            if uncle.__red:
                curr.parent.__red = False
                uncle.__red = False
                curr.parent.parent.__red = True
                curr = curr.parent.parent

            # on right/left of parent, case 2
            elif curr == curr.parent.right and onLeft:
                curr = curr.parent
                self.rotateleft(curr)
            elif curr == curr.parent.left and not onLeft:
                curr = curr.parent
                self.rotateright(curr)

            # case 3
            curr.parent.__red = False
            curr.parent.parent.__red = True
            curr = curr.parent.parent
            rotate(curr)

        # after inserting root or color violation reaching the top
        self.head.__red = False
