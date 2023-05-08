class _HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self):
        return f'HashNode(key={self.key} | value={self.value})'


class HashTable:
    def __init__(self, table_size: int = 37, load_factor: float = 0.75):
        self.table_size = table_size
        self.table = [None] * self.table_size
        self.num_nodes = 0
        self.load_factor = load_factor

    def items(self):
        for node in self.get_all():
            yield node.key, node.value

    def _generate_hash(self, unhashed_key):
        h = 0
        for char in str(unhashed_key):
            h += ord(char)
        return h % self.table_size

    def add_node(self, unhashed_key, value):
        hashed_key = self._generate_hash(unhashed_key)
        curr_node = self.table[hashed_key]
        new_node = _HashNode(unhashed_key, value)

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
                    self.add_node(node.key, node.value)
                    node = node.next

    def delete(self, unhashed_key):
        hashed_key = self._generate_hash(str(unhashed_key))
        curr_node = self.table[hashed_key]
        prev_node = None

        if curr_node is None:
            raise KeyError(f'Key {unhashed_key} not found.')
        while curr_node:
            if curr_node.key == unhashed_key:
                if not prev_node:
                    self.table[hashed_key] = curr_node.next
                else:
                    prev_node.next = curr_node.next
                self.num_nodes -= 1
                return curr_node
        return None

    def get_node(self, unhashed_key):
        hashed_key = self._generate_hash(str(unhashed_key))
        if self.table[hashed_key] is None:
            return None
        curr_node = self.table[hashed_key]
        while curr_node:
            if curr_node.key == unhashed_key:
                return curr_node
            curr_node = curr_node.next
        return None

    def has_node(self, unhashed_key):
        hashed_key = self._generate_hash(str(unhashed_key))
        curr_node = self.table[hashed_key]
        while curr_node:
            if curr_node.key == unhashed_key:
                return True
            curr_node = curr_node.next
        return False

    def change_node(self, unhashed_key, new_value):
        node = self.get_node(unhashed_key)
        if node is not None:
            node.value = new_value
        else:
            self.add_node(unhashed_key, new_value)

    def get_all(self):
        for node in self.table:
            if not node:
                pass
            while node:
                yield node
                node = node.next

    def print_all(self):
        print([node for node in self.get_all()])
