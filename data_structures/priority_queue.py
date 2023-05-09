class QueueNode:
    def __init__(self, priority, information):
        self.priority = priority
        self.information = information if information is not None else priority


class MinPriorityQueue:
    def __init__(self):
        self.queue = []

    def insert(self, priority, information=None):
        if not isinstance(priority, (int, float)):
            raise ValueError('Priority value must be an Integer or Float.')

        new_node = QueueNode(priority, information)

        self.queue.append(new_node)
        i = len(self.queue) - 1
        while i > 0 and self.queue[i].priority <= self.queue[(i - 1) // 2].priority:
            self.queue[i], self.queue[(i - 1) // 2] = self.queue[(i - 1) // 2], self.queue[i]
            i = (i - 1) // 2
        return self

    def change_priority(self, priority, information):
        for i, node in enumerate(self.queue):
            if node.information == information:
                node.priority = priority
                self.heapify(i, len(self.queue))
                return self
        return None

    # TODO:  Cite "https://www.programiz.com/dsa/heap-data-structure#heapify"
    def heapify(self, i, n):
        smallest = i
        left = (2 * i) + 1
        right = (2 * i) + 2

        if left < n and self.queue[left].priority < self.queue[smallest].priority:
            smallest = left
        if right < n and self.queue[right].priority < self.queue[smallest].priority:
            smallest = right

        if smallest != i:
            self.queue[i], self.queue[smallest] = self.queue[smallest], self.queue[i]
            self.heapify(smallest, n)

    def get(self):
        if not self.queue:
            return None

        root = self.queue[0]
        if len(self.queue) == 1:
            return self.queue.pop().information
        # Swap root with last element
        n = len(self.queue)
        self.queue[0], self.queue[n - 1] = self.queue[n - 1], self.queue[0]
        self.queue.pop()
        self.heapify(0, n - 1)
        return root.information

    def peek(self):
        return self.queue[0].information

    def is_empty(self):
        return len(self.queue) == 0


class MaxPriorityQueue:
    def __init__(self):
        self.queue = []

    def insert(self, priority, information=None):
        if not isinstance(priority, (int, float)):
            raise ValueError('Priority value must be an Integer or Float.')

        new_node = QueueNode(priority, information)

        self.queue.append(new_node)
        i = len(self.queue) - 1
        while i > 0 and self.queue[i].priority >= self.queue[(i - 1) // 2].priority:
            self.queue[i], self.queue[(i - 1) // 2] = self.queue[(i - 1) // 2], self.queue[i]
            i = (i - 1) // 2
        return self

    def change_priority(self, priority, information):
        for i, node in enumerate(self.queue):
            if node.information == information:
                node.priority = priority
                self.heapify(i, len(self.queue))
                return self
        return None

    def heapify(self, i, n):
        largest = i
        left = (2 * i) + 1
        right = (2 * i) + 2

        if left < n and self.queue[left].priority > self.queue[largest].priority:
            largest = left
        if right < n and self.queue[right].priority > self.queue[largest].priority:
            largest = right

        if largest != i:
            self.queue[i], self.queue[largest] = self.queue[largest], self.queue[i]
            self.heapify(largest, n)

    def get(self):
        if not self.queue:
            return None

        root = self.queue[0]
        if len(self.queue) == 1:
            return self.queue.pop().information
        # Swap root with last element
        n = len(self.queue)
        self.queue[0], self.queue[n - 1] = self.queue[n - 1], self.queue[0]
        self.queue.pop()
        self.heapify(0, n - 1)
        return root.information

    def peek(self):
        return self.queue[0].information

    def is_empty(self):
        return len(self.queue) == 0
