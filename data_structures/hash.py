class _HashNode:
    def __init__(self, key, value):
        self._key = key
        self._value = value
        self._next = None

    def __repr__(self):
        return f'HashNode(key={self.key} | value={self.value})'

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next


class HashTable:
    def __init__(self, table_size: int = 37, load_factor: float = 0.75):
        self._table_size = table_size
        self._table = [None] * self._table_size
        self._num_nodes = 0
        self._load_factor = load_factor

    def __getitem__(self, unhashed_key):
        return self._get_node(unhashed_key)

    def __setitem__(self, unhashed_key, value):
        self._add_node(unhashed_key, value)

    def _get_node(self, unhashed_key):
        hashed_key = self._generate_hash(str(unhashed_key))
        if self._table[hashed_key] is None:
            return None
        curr_node = self._table[hashed_key]
        while curr_node:
            if curr_node.key == unhashed_key:
                return curr_node
            curr_node = curr_node.next
        return None

    def _add_node(self, unhashed_key, value):
        hashed_key = self._generate_hash(unhashed_key)
        curr_node = self._table[hashed_key]
        new_node = _HashNode(unhashed_key, value)

        if curr_node is None:
            self._table[hashed_key] = new_node
        else:
            while curr_node.next:
                curr_node = curr_node.next
            curr_node.next = new_node
        self._num_nodes += 1

        if self._num_nodes / self._table_size >= self._load_factor:
            self.rehash()

        return new_node

    def _generate_hash(self, unhashed_key):
        h = 0
        for char in str(unhashed_key):
            h += ord(char)
        return h % self._table_size

    def get_size(self):
        return self._num_nodes

    def items(self):
        for node in self.get_all():
            yield node.key, node.value

    def rehash(self):
        temp_table = self._table

        self._table_size *= 2
        self._table = [None] * self._table_size
        self._num_nodes = 0

        for node in temp_table:
            if node is None:
                pass
            else:
                while node:
                    self._add_node(node.key, node.value)
                    node = node.next

    def delete(self, unhashed_key):
        hashed_key = self._generate_hash(str(unhashed_key))
        curr_node = self._table[hashed_key]
        prev_node = None

        if curr_node is None:
            raise KeyError(f'Key {unhashed_key} not found.')
        while curr_node:
            if curr_node.key == unhashed_key:
                if not prev_node:
                    self._table[hashed_key] = curr_node.next
                else:
                    prev_node.next = curr_node.next
                self._num_nodes -= 1
                return curr_node
        return None

    def has_node(self, unhashed_key):
        hashed_key = self._generate_hash(str(unhashed_key))
        curr_node = self._table[hashed_key]
        while curr_node:
            if curr_node.key == unhashed_key:
                return True
            curr_node = curr_node.next
        return False

    def change_node(self, unhashed_key, new_value):
        node = self._get_node(unhashed_key)
        if node is not None:
            node.value = new_value
        else:
            self._add_node(unhashed_key, new_value)

    def get_all(self):
        for node in self._table:
            if not node:
                pass
            while node:
                yield node
                node = node.next

    def print_all(self):
        print([node for node in self.get_all()])
