class _HashNode:
    """
    Represents nodes used in hash table.
    """
    def __init__(self, key, value):
        """
        Initializes a new instance of the _HashNode class.
        :param key: The key associated with the node.
        :param value: The value associated with the node.
        """
        self._key = key
        self._value = value
        self._next = None

    def __repr__(self):
        """
        Returns the string representation of the _HashNode object.
        :return: The string representation of the _HashNode object.
        """
        return f'HashNode(key={self.key} | value={self.value})'

    @property
    def key(self):
        """
        Returns the key associated with the node.
        :return: The key associated with the node.
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key associated with the node.
        :param key: The new key associated with the node.
        """
        self._key = key

    @property
    def value(self):
        """
        Returns the value associated with the node.
        :return: The value associated with the node.
        """
        return self._value

    @value.setter
    def value(self, val):
        """
        Sets the value associated with the node.
        :param val: The new value associated with the node.
        """
        self._value = val

    @property
    def next(self):
        """
        Returns the value of the next pointer associated with the node.
        :return: The value of the next pointer associated with the node.
        """
        return self._next

    @next.setter
    def next(self, next):
        """
        Sets the value of the next pointer associated with the node.
        :param next: The next pointer value associated with the node.
        """
        self._next = next


class HashTable:
    """
    A class representing a hash function that provides a Python dictionary-like implementation. This implementation
    includes a rehash() function that will resize the table to better distribute nodes once its load factor is
    exceeded. Standard methods for getting nodes, setting nodes, changing nodes, etc. are provided.
    """
    def __init__(self, table_size: int = 37, load_factor: float = 0.75):
        """
        Initializes a new instance of the HashNode class.
        :param table_size: The desired size of the table.
        :param load_factor: The threshold value which triggers rehashing if exceeded.
        """
        self._table_size = table_size
        self._table = [None] * self._table_size
        self._num_nodes = 0
        self._load_factor = load_factor

    def __getitem__(self, unhashed_key):
        """
        Returns the node associated with the unhashed key.
        :param unhashed_key: Key associated with node before hashing.
        :return:
        """
        return self._get_node(unhashed_key)

    def __setitem__(self, unhashed_key, value):
        """
        Adds node with provided key and value.
        :param unhashed_key: Key to be associated with node prior to hashing.
        :param value: Value to be associated with node.
        :return:
        """
        self._add_node(unhashed_key, value)

    def _get_node(self, unhashed_key):
        """
        Hashes the provided key, then finds and returns the corresponding node.
        Implements the move-to-front strategy for increased efficiency.
        :param unhashed_key: Key associated with node before hashing.
        :return: The corresponding node if it exists, otherwise None.
        """
        hashed_key = self._generate_hash(str(unhashed_key))
        if self._table[hashed_key] is None:
            return None
        curr_node = self._table[hashed_key]
        prev_node = None

        while curr_node:
            if curr_node.key == unhashed_key:
                if prev_node:
                    prev_node.next = curr_node.next
                    curr_node.next = self._table[hashed_key]
                    self._table[hashed_key] = curr_node
                return curr_node
            curr_node = curr_node.next
        return None

    def _add_node(self, unhashed_key, value):
        """
        Adds a node to the hash table after hashing the provided key.
        :param unhashed_key: Key to be associated with node prior to hashing.
        :param value: Value to be associated with node.
        :return:
        """
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

    def _generate_hash(self, unhashed_key):
        """
        The primary logic of the hash data structure. Takes the sum of each character's integer value representing its
        Unicode character, then takes that value with respect to the size of the table to determine its position.
        :param unhashed_key: Key to be hashed.
        :return: The calculated index after determining the key's hash value.
        """
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
