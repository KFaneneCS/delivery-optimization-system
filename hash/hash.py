class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        return f'HashNode(key={self.key} | value={self.value})'


class HashTable:
    def __init__(self, table_size: int = 30, load_factor: float = 0.75):
        self.table_size = table_size
        self.table = [None] * self.table_size
        self.num_nodes = 0
        self.load_factor = load_factor

    def _generate_hash(self, key):
        h = 0
        for char in str(key):
            h += ord(char)
        return h % self.table_size

    def insert(self, key, value):
        hashed_key = self._generate_hash(str(key))
        curr_node = self.table[hashed_key]
        new_node = HashNode(key, value)

        if curr_node is None:
            self.table[hashed_key] = new_node
        else:
            while curr_node.next:
                curr_node = curr_node.next
            curr_node.next = new_node
        self.num_nodes += 1

        if self.num_nodes / self.table_size >= self.load_factor:
            self.rehash()

        return new_node

    def rehash(self):
        temp_table = self.table

        self.table_size *= 2
        self.table = [None] * self.table_size
        self.num_nodes = 0

        for node in temp_table:
            if node is None:
                pass
            else:
                while node:
                    key = node.key
                    hashed_key = self._generate_hash(key)
                    self.insert(hashed_key, node)
                    node = node.next

    def delete(self, key):
        hashed_key = self._generate_hash(str(key))
        curr_node = self.table[hashed_key]

        while curr_node:
            if curr_node.key == key:
                return curr_node
        return None

    def lookup(self, key):
        hashed_key = self._generate_hash(str(key))
        if self.table[hashed_key] is None:
            return None

        curr_node = self.table[hashed_key]
        while curr_node:
            if curr_node.key == key:
                return curr_node
            curr_node = curr_node.next
        return None

    def get_all(self):
        for node in self.table:
            if not node:
                pass
            while node:
                yield node
                node = node.next
