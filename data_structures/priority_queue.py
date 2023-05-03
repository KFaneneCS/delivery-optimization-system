class QueueNode:
    def __init__(self, priority, information):
        self.pr = priority
        self.info = information if information is not None else priority


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def insert(self, priority, information=None):
        if not isinstance(priority, (int, float)):
            raise ValueError('Priority value must be an Integer or Float.')

        new_node = QueueNode(priority, information)

        self.queue.append(new_node)
        i = len(self.queue) - 1
        while i > 0 and self.queue[i].pr <= self.queue[(i - 1) // 2].pr:
            self.queue[i], self.queue[(i - 1) // 2] = self.queue[(i - 1) // 2], self.queue[i]
            i = (i - 1) // 2
        return self

    def change_priority(self, priority, information):
        for i, node in enumerate(self.queue):
            if node.info == information:
                node.pr = priority
                self.heapify(i, len(self.queue))
                return self
        return None

    # TODO:  Cite "https://www.programiz.com/dsa/heap-data-structure#heapify"
    def heapify(self, i, n):
        smallest = i
        left = (2 * i) + 1
        right = (2 * i) + 2

        if left < n and self.queue[left].pr < self.queue[smallest].pr:
            smallest = left
        if right < n and self.queue[right].pr < self.queue[smallest].pr:
            smallest = right

        if smallest != i:
            self.queue[i], self.queue[smallest] = self.queue[smallest], self.queue[i]
            self.heapify(smallest, n)

    def get(self):
        if not self.queue:
            return None

        root = self.queue[0]
        if len(self.queue) == 1:
            return self.queue.pop().info
        # Swap root with last element
        n = len(self.queue)
        self.queue[0], self.queue[n - 1] = self.queue[n - 1], self.queue[0]
        self.queue.pop()
        self.heapify(0, n - 1)
        return root.info

    def peek(self):
        return self.queue[0].info

    def is_empty(self):
        return len(self.queue) == 0

    def print_queue(self):
        print([(node.pr, node.info) for node in self.queue])
