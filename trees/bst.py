class Node():
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.__red = True

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
    red-black bst
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
        new_root.setleft(curr)

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

    def insert(self, node):
        # find initial insert position
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
                    self.rotateleft(curr)

                # case 3
                curr.parent.__red = False
                curr.parent.parent.__red = True
                curr = curr.parent.parent
                self.rotateright(curr)

            # on right of grandparent (reflection)
            else:

                # uncle is red, case 1
                if curr.parent.parent.left.__red:
                    uncle = curr.parent.parent.left
                    curr.parent.__red = False
                    uncle.__red = False
                    curr.parent.parent.__red = True
                    curr = curr.parent.parent

                # on left of parent, case 2
                elif curr == curr.parent.left:
                    curr = curr.parent
                    self.rotateright(curr)

                # case 3
                curr.parent.__red = False
                curr.parent.parent.__red = True
                curr = curr.parent.parent
                self.rotateleft(curr)

        # after inserting root or color violation reaching the top
        self.head.__red = False