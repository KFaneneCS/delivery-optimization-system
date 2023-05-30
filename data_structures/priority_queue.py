class _QueueNode:
    """
    A class representing nodes used in the priority queue.
    """

    def __init__(self, priority, information, is_max: bool = False):
        """
        Initializes a new instance of the _QueueNode class.
        :param priority: The priority value of the node.
        :param information: The data that will be prioritized.
        :param is_max: A boolean which accounts for both max and min priority queues for proper priority value
        comparisons.
        """
        self.priority = priority
        self.information = information if information is not None else priority
        self.is_max = is_max

    def __lt__(self, other):
        """
        Method which allows for proper priority value comparisons depending on whether the user intends for a max-
        or min-priority queue.
        :param other: The general other object to compare against.
        :return: True if the current object has a priority that is higher than the other object's for a max queue, or
        True if the current object has a priority that is lower than the other object's for a min queue.
        """
        if self.is_max:
            return self.priority > other.priority
        else:
            return self.priority < other.priority


class PriorityQueue:
    """
    A class that implements a priority queue (both min- and max-heap).

    This implementation contains many standard methods for inserting into the queue, changing a node's priority,
    getting and peeking at the node at the front of the queue, and others.  It also has the necessary heapify()
    function which maintains each node's priority relative to each other, with the root node containing the highest
    priority value.
    """

    def __init__(self, is_max: bool = False):
        """
        Initializes a new instance of the PriorityQueue class.
        :param is_max: Boolean that indicates max priority queue if true, otherwise min priority queue.
        """
        self._queue = []
        self.is_max = is_max

    def __iter__(self):
        """
        Returns an iterator that yields the information for each node in the queue.
        :return: Node information for each node in the queue.
        """
        for node in self._queue:
            yield node.information

    def insert(self, priority, information=None):
        """
        Insertion method to add new node to the priority queue performing a heap-up operation.
        :param priority: The priority value of the new node.
        :param information: The information/data associated with the new node.
        """
        new_node = _QueueNode(priority, information)

        self._queue.append(new_node)
        i = len(self._queue) - 1
        while i > 0 and self._queue[i].priority <= self._queue[(i - 1) // 2].priority:
            self._queue[i], self._queue[(i - 1) // 2] = self._queue[(i - 1) // 2], self._queue[i]
            i = (i - 1) // 2

    def change_priority(self, priority, information):
        """
        Changes the priority value of an existing node in the queue.
        :param priority: The new priority value of an existing node.
        :param information: The current information associated with the existing node. Used to find the node in queue.
        :return:
        """
        for i, node in enumerate(self._queue):
            if node.information == information:
                node.priority = priority
                self.heapify(i, len(self._queue))
                return self
        return None

    def heapify(self, i, n):
        """
        Method which contains the heap logic to maintain the tree's heap property.

        Compares the left and right child of the node at index i and performs a swap if the current node's priority
        value is less than either child.  This is performed recursively until the all nodes are in their proper place.
        This method is called to restore the heap property after changes are made, such as removing nodes.
        :param i:
        :param n:
        :return:
        """
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
        """
        Pops and returns the next node at the front of the queue, then calls the heapify() method to maintain the
        tree's heap property.
        :return: The next node at the front of the queue, otherwise None.
        """
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

    def peek(self):
        """
        Returns the information/data for the node at the front of the queue without removing it from the queue.
        :return: The information/data for the node at the front of the queue.
        :raises IndexError: Returns None if there are no nodes.
        """
        try:
            return self._queue[0].information
        except IndexError:
            return None

    def peek_last(self):
        """
        Returns the information/data for the node at the back of the queue without removing it from the queue.
        :return: The information/data for the node at the back of the queue.
        :raises IndexError: Returns None if there are no nodes.
        """
        try:
            return self._queue[-1].information
        except IndexError:
            return None

    def contains(self, information):
        """
        A boolean function that returns True if a node exists with the provided information passed as a parameter,
        otherwise False.
        :param information: The node's information/data in the queue if it exists.
        :return: True if a node exists with the provided information/data, otherwise False.
        """
        for i, node in enumerate(self._queue):
            if node.information == information:
                return True
        return False

    def is_empty(self):
        """
        A boolean function that returns True if there are no nodes in the queue, otherwise False.
        :return: True if there are no nodes in the queue, otherwise False.
        """
        return len(self._queue) == 0

    def get_size(self):
        """
        Returns the number of nodes in the priority queue.
        :return: Number of nodes in the priority queue.
        """
        return len(self._queue)
