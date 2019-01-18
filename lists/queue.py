class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def setnext(self, node):
        node.prev = self
        self.next = node

class Queue():
    def __init__(self, head=None):
        self.head = head
        curr = self.head
        prev = None
        self.length = 0
        while curr:
            self.length += 1
            prev = curr
            curr = curr.next
        self.tail = prev

    def enqueue(self, data):
        self.length += 1
        node = QueueNode(data)
        if not self.head:
            self.head = node
            self.tail = node
            return
        self.tail.setnext(node)
        self.tail = self.tail.next



    def dequeue(self):
        if not self.head:
            return None
        self.length -= 1
        ret = self.head.data
        if self.tail == self.head:
            self.head = self.tail = None
            return ret
        self.head = self.head.next
        return ret

    def top(self):
        if not self.head:
            return None
        return self.head.data

    def __len__(self):
        return self.length