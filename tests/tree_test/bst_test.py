import unittest
from trees.bst import BST
import random

def black_height(curr):
    if curr is None:
        return 1
    left_bh = black_height(curr.left)
    right_bh = black_height(curr.right)
    if left_bh == -1 or right_bh == -1 or left_bh != right_bh:
        return -1
    return left_bh + int(not curr.__red)

class TestRedBlack(unittest.TestCase):
    def setUp(self):
        random.seed(1957)

        self.insert_trees = []
        for n in range(1, 50, 3):
            bst = BST()
            for _ in range(n):
                bst.insert(random.randint(0,1000))
            self.insert_trees.append(bst)

        # TODO: delete random items from each tree
        self.delete_trees = self.insert_trees.copy()
        for dbst in self.delete_trees:
            dels = 0
            while dels < random.randint(0,bst.len()):
                dels += int(dbst.delete(random.randint(0,1000)))


    def test_black_heights_insertion(self):
        bh_rule = True
        trees = self.insert_trees
        for bst in trees:
            if black_height(bst.root) == -1:
                bh_rule = False
        self.assertTrue(bh_rule)

    def test_black_heights_deletion(self):
        bh_rule = True
        trees = self.delete_trees
        for bst in trees:
            if black_height(bst.root) == -1:
                bh_rule = False
        self.assertTrue(bh_rule)