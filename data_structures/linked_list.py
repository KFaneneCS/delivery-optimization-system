class Node:

    def __init__(self, value, **kwargs):
        self.value = value
        self.next = None
        self.prev = None
        for k, v in kwargs.items():
            setattr(self, k, v)


class LinkedList:

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __iter__(self):
        current = self._head
        while current is not None:
            yield current
            current = current.next

    def __reversed__(self):
        current = self._tail
        while current is not None:
            yield current
            current = current.prev

    def add_link(self, value, **kwargs):
        new_node = Node(value, **kwargs)
        if self._head is None:
            self._head = self._tail = new_node
            self._size += 1
            return
        self._tail.next = new_node
        new_node.prev = self._tail
        self._tail = new_node
        self._size += 1

    def prepend_link(self, value):
        new_node = Node(value)
        self._head.prev = new_node
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def insert_link(self, index, value):
        if index < 0:
            raise IndexError("Index out of bounds")
        if index == 0:
            self.prepend_link(value)
            return
        if index >= self._size:
            self.add_link(value)
            return

        new_node = Node(value)
        prev_node = self.link_at(index - 1)
        following_node = prev_node.next
        new_node.prev = prev_node
        new_node.next = following_node
        prev_node.next = new_node
        following_node.prev = new_node
        self._size += 1

    def remove_link(self, index):
        if (index > self._size - 1) or (index < 0):
            raise IndexError("Index out of bounds")
        if index == 0:
            self._head = self._head.next
            self._head.prev = None
            return
        node = self.link_at(index)
        node.prev.next, node.next.prev = node.next, node.prev
        self._size -= 1

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    @property
    def size(self):
        return self._size

    def link_at(self, index):
        if (index > self._size - 1) or (index < 0):
            raise IndexError("Index out of bounds")
        if index < self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next
        else:
            current = self._tail
            for _ in reversed(range(self._size - index - 1)):
                current = current.prev
        return current

    def contains(self, value):
        return any(node.value == value for node in self)

    def print_all(self):
        print([node.value for node in self])
