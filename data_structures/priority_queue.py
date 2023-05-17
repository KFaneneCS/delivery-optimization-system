class QueueNode:
    def __init__(self, priority, information):
        self.priority = priority
        self.information = information if information is not None else priority


class MinPriorityQueue:
    def __init__(self):
        self._queue = []

    def __iter__(self):
        for node in self._queue:
            yield node.information

    def insert(self, priority, information=None):
        new_node = QueueNode(priority, information)

        self._queue.append(new_node)
        i = len(self._queue) - 1
        while i > 0 and self._queue[i].priority <= self._queue[(i - 1) // 2].priority:
            self._queue[i], self._queue[(i - 1) // 2] = self._queue[(i - 1) // 2], self._queue[i]
            i = (i - 1) // 2
        return self

    def change_priority(self, priority, information):
        for i, node in enumerate(self._queue):
            if node.information == information:
                node.priority = priority
                self.heapify(i, len(self._queue))
                return self
        return None

    # TODO:  Cite "https://www.programiz.com/dsa/heap-data-structure#heapify"
    def heapify(self, i, n):
        smallest = i
        left = (2 * i) + 1
        right = (2 * i) + 2

        if left < n and self._queue[left].priority < self._queue[smallest].priority:
            smallest = left
        if right < n and self._queue[right].priority < self._queue[smallest].priority:
            smallest = right

        if smallest != i:
            self._queue[i], self._queue[smallest] = self._queue[smallest], self._queue[i]
            self.heapify(smallest, n)

    def get(self):
        if not self._queue:
            return None

        root = self._queue[0]
        if len(self._queue) == 1:
            return self._queue.pop().information
        # Swap root with last element
        n = len(self._queue)
        self._queue[0], self._queue[n - 1] = self._queue[n - 1], self._queue[0]
        self._queue.pop()
        self.heapify(0, n - 1)
        return root.information

    def get_by_information(self, info):
        for i, node in enumerate(self._queue):
            if node.information == info:
                node = self._queue.pop(i)
                return node.information
        return None

    def peek(self):
        try:
            return self._queue[0].information
        except IndexError:
            return None

    def contains(self, information):
        for i, node in enumerate(self._queue):
            if node.information == information:
                return True
        return False

    def is_empty(self):
        return len(self._queue) == 0

    def get_size(self):
        return len(self._queue)


class MaxPriorityQueue:
    def __init__(self):
        self._queue = []

    def insert(self, priority, information=None):
        if not isinstance(priority, (int, float)):
            raise ValueError('Invalid "priority" value.')

        new_node = QueueNode(priority, information)

        self._queue.append(new_node)
        i = len(self._queue) - 1
        while i > 0 and self._queue[i].priority >= self._queue[(i - 1) // 2].priority:
            self._queue[i], self._queue[(i - 1) // 2] = self._queue[(i - 1) // 2], self._queue[i]
            i = (i - 1) // 2
        return self

    def change_priority(self, priority, information):
        for i, node in enumerate(self._queue):
            if node.information == information:
                node.priority = priority
                self.heapify(i, len(self._queue))
                return self
        return None

    def heapify(self, i, n):
        largest = i
        left = (2 * i) + 1
        right = (2 * i) + 2

        if left < n and self._queue[left].priority > self._queue[largest].priority:
            largest = left
        if right < n and self._queue[right].priority > self._queue[largest].priority:
            largest = right

        if largest != i:
            self._queue[i], self._queue[largest] = self._queue[largest], self._queue[i]
            self.heapify(largest, n)

    def get(self):
        if not self._queue:
            return None

        root = self._queue[0]
        if len(self._queue) == 1:
            return self._queue.pop().information
        # Swap root with last element
        n = len(self._queue)
        self._queue[0], self._queue[n - 1] = self._queue[n - 1], self._queue[0]
        self._queue.pop()
        self.heapify(0, n - 1)
        return root.information

    def get_by_information(self, info):
        for i, node in enumerate(self._queue):
            if node.information == info:
                node = self._queue.pop(i)
                return node.information
        return None

    def peek(self):
        try:
            return self._queue[0].information
        except IndexError:
            return None

    def contains(self, information):
        for i, node in enumerate(self._queue):
            if node.information == information:
                return True
        return False

    def is_empty(self):
        return len(self._queue) == 0

    def get_size(self):
        return len(self._queue)
