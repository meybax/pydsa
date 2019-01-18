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

def copy_helper(source):
    if source is None:
        return None
    dest = Node(source.val, _Node__isred=source._Node__red)
    dest.setleft(copy_helper(source.left))
    dest.setright(copy_helper(source.right))
    return dest

class BST():
    """
    red-black bst with comparable values
    """

    def __init__(self):
        self.root = None
        self.size = 0

    def rotateright(self, curr):
        new_root = curr.left
        curr.setleft(new_root.right)
        if not curr.parent:
            self.root = new_root
            new_root.parent = None
        elif curr == curr.parent.left:
            curr.parent.setleft(new_root)
        else:
            curr.parent.setright(new_root)
        new_root.setright(curr)
        return new_root

    def rotateleft(self, curr):
        new_root = curr.right
        curr.setright(new_root.left)
        if not curr.parent:
            self.root = new_root
            new_root.parent = None
        elif curr == curr.parent.left:
            curr.parent.setleft(new_root)
        else:
            curr.parent.setright(new_root)
        new_root.setleft(curr)
        return new_root

    def insert(self, val):
        self.size += 1
        # find initial insert position
        node = Node(val)
        if self.root is None:
            node.__isred = False
            self.root = node
            return

        curr = self.root
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
        while curr.parent and curr.parent.parent and curr.parent._Node__red:
            # on left of grandparent
            if curr.parent == curr.parent.parent.left:
                uncle = curr.parent.parent.right
                onLeft = True
                rotate = self.rotateright
            # on right of grandparent
            else:
                uncle = curr.parent.parent.left
                onLeft = False
                rotate = self.rotateleft

            # uncle is red, case 1
            if uncle._Node__red:
                curr.parent._Node__red = False
                uncle._Node__red = False
                curr.parent.parent._Node__red = True
                curr = curr.parent.parent
            else:
                # on right/left of parent, case 2
                if curr == curr.parent.right and onLeft:
                    curr = self.rotateleft(curr.parent).left
                elif curr == curr.parent.left and not onLeft:
                    curr = self.rotateright(curr.parent).right

                # case 3
                curr.parent._Node__red = False
                curr.parent.parent._Node__red = True
                curr = curr.parent.parent
                curr = rotate(curr)
                break

        # after inserting root or color violation reaching root
        self.root._Node__red = False

    def delete(self, node):
        # standard BTS delete, keeping track of color of deleted and replacement Node
        del_isRed = node._Node__red
        curr = node
        if not curr.left and not curr.right:
            replace = None
            if curr == curr.parent.right:
                curr.parent.right = None
            else:
                curr.parent.left = None
            curr = curr.parent
        elif not curr.left or not curr.right:
            replace = curr.right or curr.left
            curr.val = replace.val
            curr.left = replace.left
            curr.right = replace.right
        else:
            replace = curr.right
            while replace.left:
                replace = replace.left
            Node.val = replace.val
            self.delete(replace)

        # simple case
        if del_isRed or replace._Node__red:
            curr._Node__red == False
        else:
            # ...
            pass

    def insert_no_rebalance(self, val):
        node = Node(val)
        if self.root is None:
            node.__isred = False
            self.root = node
            return

        curr = self.root
        while curr.left and curr.right:
            if node.val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        if node.val < curr.val:
            curr.setleft(node)
        else:
            curr.setright(node)

    def copy(self):
        new_tree = BST()
        new_root = copy_helper(self.root)
        new_tree.root = new_root
        new_tree.size = self.size
        return new_tree