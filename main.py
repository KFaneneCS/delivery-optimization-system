# Kyle Fanene - 006246401

"""
**Complexity**:

Time Complexity:  By far, the greatest contributor to the time complexity of this program is the implementation of
Dijkstra's algorithm to find the most efficient path.  This is because it must iterate through each node (location)
and its relationship to every other node in a complete graph, and considering this is required on ALL nodes,
this amounts to a relatively substantial runtime of O(n^3).  This stems from Dijkstra's algorithm running at a time
complexity of O(n^2 * log(n)) - however, since we must run this "n" (number of nodes) times, the total cost is
O(n * (n^2 * log(n))), which simplifies to O(n^3).
Note that despite this undesirable time complexity, this process only needs to occur once, after which point each
shortest-path is stored in an easily-accessible hash table.

Space Complexity: Similar to the time complexity of this program, Dijkstra's is the largest contributor to the space
complexity.  This is because each node depends on a priority queue of each other node, and since we must perform the
operation for every node in a complete graph, the space complexity for best, average, and worst-case is O(n^2).

"""

from logistics_manager.logistics_manager import LogisticsManager
from user_interface.ui import UI

if __name__ == '__main__':
    locations_file_path = 'data/distance_table.csv'
    packages_file_path = 'data/package_file.csv'

    logistics_manager = LogisticsManager(locations_file_path, packages_file_path)
    logistics_manager.load_packages()
    logistics_manager.deliver_packages()
    packages = logistics_manager.get_packages()
    trucks = logistics_manager.get_trucks()

    ui = UI(packages, trucks)
    ui.execute()
