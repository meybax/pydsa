from lists.queue import Queue
from collections import namedtuple
from sty import fg

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

    def __init__(self, node=None):
        self.root = node
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
        # case with no children
        if not curr.left and not curr.right:
            replace = None
            if curr == curr.parent.right:
                curr.parent.right = None
            else:
                curr.parent.left = None
            curr = curr.parent
        # case with 1 child
        elif not curr.left or not curr.right:
            replace = curr.right or curr.left
            curr.val = replace.val
            curr.left = replace.left
            curr.right = replace.right
        # case with 2 children
        else:
            replace = curr.right
            while replace.left:
                replace = replace.left
            Node.val = replace.val
            self.delete(replace)

        # simple case
        if del_isRed or replace._Node__red:
            curr._Node__red == False
        # both delete and replace are black
        else:
            while curr != self.root:
                sibling = curr.parent.left if curr == curr.parent.right else curr.parent.right
                # case where sibling has red child
                if not sibling._Node__red and (sibling.left._Node__red or sibling.right._Node__red):
                    niece = sibling.left if sibling.left._Node__red else sibling.right
                    if sibling == curr.parent.left:
                        # left left
                        if niece == sibling.left:
                            self.rotateright(curr.parent)
                        # left right
                        else:
                            niece._Node__red = False
                            sibling = self.rotateleft(sibling)
                            self.rotateright(sibling.parent)
                    else:
                        # right right
                        if niece == sibling.right:
                            self.rotateleft(curr.parent)
                        # right left
                        else:
                            niece._Node__red = False
                            sibling = self.rotateright(sibling)
                            self.rotateleft(sibling.parent)
                    break
                # sibling and children are black
                elif not sibling._Node__red:
                    sibling._Node__red = True
                    curr = curr.parent
                # sibling is red
                else:
                    sibling._Node__red = False
                    # right case
                    if sibling == sibling.parent.right:
                        sibling.left._Node__red = True
                        self.rotateleft(curr.parent)
                    # left case
                    else:
                        sibling.right._Node__red = True
                        self.rotateright(curr.parent)
                    break
            else:
                self.root._Node__red = False
        return self.root

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

    def visualize(self):
        ldict = level_order_dict(self.root)
        levels = sorted(ldict.keys())[-1] + 1
        currs = 1
        spaces_betw = [currs]
        for _ in range(levels - 1):
            currs *= 2
            currs += 1
            spaces_betw.append(currs)
        spaces_betw = list(reversed(spaces_betw))
        spaces_betw.append(0)

        for l in range(levels):
            print(' ' * (spaces_betw[l + 1]), end='')
            curr_level = ldict[l]
            for node in curr_level:
                if not node:
                    p = ' '
                elif node._Node__red:
                    p = fg.red + str(node.val) + fg.rs
                else:
                    p = str(node.val)
                print(p, end=' ' * spaces_betw[l])
            print()

def level_order_dict(root):
    level = 0
    q = Queue()
    LevelNode = namedtuple('LevelNode', ['node', 'level'])
    q.enqueue(LevelNode(root, level))
    ldict = {0:[]}
    all_null = True
    while q:
        curr = q.dequeue()
        if curr.level != level:
            if all_null:
                del ldict[level]
                break
            all_null = True
            level = curr.level
            ldict[level] = [curr.node]
        else:
            ldict[level].append(curr.node)

        if curr.node is None:
            left = None
            right = None
        else:
            all_null = False
            left = curr.node.left
            right = curr.node.right
        q.enqueue(LevelNode(left, level + 1))
        q.enqueue(LevelNode(right, level + 1))

    return ldict

def rb_bst_from_level_order(level_ord):
    """
    :return:
    """
    level_ord = level_ord.split()
    val, color = level_ord[0].split('.')
    level_ord[0] = Node(val, _Node__isred=color=='R')

    for i in range(len(level_ord)):
        curr = level_ord[i]
        i = i + 1
        if curr is not None and type(curr) != str:
            li = (i * 2) - 1
            ri = (i * 2)
            if li < len(level_ord) and level_ord[li] != 'null':
                left_val, left_color = level_ord[li].split('.')
                curr.setleft(Node(left_val, _Node__isred=left_color=="R"))
                level_ord[li] = curr.left
            if ri < len(level_ord)  and level_ord[ri] != 'null':
                right_val, right_color = level_ord[ri].split('.')
                curr.setright(Node(right_val, _Node__isred=right_color=="R"))
                level_ord[ri] = curr.right
    return level_ord[0]

def copy_helper(source):
    if source is None:
        return None
    dest = Node(source.val, _Node__isred=source._Node__red)
    dest.setleft(copy_helper(source.left))
    dest.setright(copy_helper(source.right))
    return dest

bst = BST(rb_bst_from_level_order('1.B 2.B 3.B null 5.R 6.B null null null 7.B'))
bst.visualize()