from hash.hash import HashTable
import bisect


class Graph:
    def __init__(self):
        self.edges = HashTable(700)

    def add_vertex(self, node):
        self.edges.add(node.get_key(), [])

    def add_weighted_edge(self, source, target, weight):
        # print(f'source key: {source.get_key()} ~ (target, weight): {(target, weight)}')
        # self.edges.insert(source.get_key(), (target, weight))
        # self.edges.insert(target.get_key(), (source, weight))

        source_node = self.edges.get_node(source.get_key())
        print(f'source node = {source_node}')
        # target_node = self.edges.get_node(target.get_key())

        # print(f'BEFORE:   source node: {source_node} ~~ target node: {target_node}')

        source_tuple = (target, weight)
        print(f'source tuple = {source_tuple}')
        # target_tuple = (source, weight)

        bisect.insort(source_node.value, source_tuple, key=lambda x: x[1])
        # bisect.insort(target_node.value, target_tuple, key=lambda x: x[1])

        # source_node.value.append((target, weight))
        # target_node.value.append((source, weight))

        # print(f'AFTER:   source node: {source_node} ~~ target node: {target_node}')

        return self.edges

    def show_all_connections(self):
        print('\n***SHOW ALL CONNECTIONS CALLED***')
        # FIXME:  Below shows failures in adjacencies hash table

        # for x in self.edges.get_all():
        #     print(x)

        # for vertex in self.vertices:
        #     print(f'current vertex = {vertex}')
        #     node = self.edges.lookup(vertex.get_key())
        #     count = 0
        #     while node:
        #         print(node)
        #         node = node.next
        #         count += 1
        #     print(f'count === {count}')

        # for x in self.edges.get_all():
        #     print(x)
        print('*****************************')
        count = 0
        for key, value in self.edges.items():
            print(f'current = {key}')
            for val in value:
                print(val)
            print(f'total == {len(value)}')
            count += 1
        print(f'TOTAL = {count}')

            # edges = self.edges.get_node(vertex.get_key())
            # while edges:
            #     print(edges)
            #     edges = edges.next
        return
