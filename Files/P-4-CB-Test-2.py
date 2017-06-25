"""Running with Bunnies
====================

You and your rescued bunny prisoners need to get out of this collapsing death trap of a space station - and fast! Unfortunately, some of the bunnies have been weakened by their long imprisonment and can't run very fast. Their friends are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can and get through the bulkheads before they close. 

The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ..., last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave - you can move to and from the bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact with the space station's security checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is traversed, the same amount of time is used or added.

Write a function of the form answer(times, time_limit) to calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest prisoner IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by prisoner ID, with the first bunny being 0. There are at most 5 bunnies, and time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best combination for this space station hallway, so the answer is [1, 2].

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) times = [[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]]
    (int) time_limit = 3
Output:
    (int list) [0, 1]

Inputs:
    (int) times = [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]]
    (int) time_limit = 1
Output:
    (int list) [1, 2]

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
"""

import queue

def answer(times, time_limit):
    exit_node = len(times) - 1
    num_bunnies = len(times) - 2
    best_bunnies_possible = list(map(lambda x: x, range(0, num_bunnies)))
    best_bunnies_checker = list(map(lambda x: x, range(num_bunnies+2)))
    possible_sets = []
    b_f_times = generate_b_f(times)
    if infinite_check(times, b_f_times[0]):
        return best_bunnies_possible

    ## Check if it is possible to get from node zero to exit node in time.
    ## If the last element in the first row is greater than the time limit
    ## it is impossible to get to the exit in time at all.
    if b_f_times[0][-1] > time_limit:
        return []
    ## Check if it is possible to make it through each node and still make
    ## it to the exit in time.
    bad_nodes = set()
    for temp_node, temp_edges in enumerate(b_f_times):
        ## b_f_times[0][temp_node] is the shortest path from start to node.
        ## temp_edge[exit_node] is shortest path from node to exit.
        temp_sum = b_f_times[0][temp_node] + temp_edges[exit_node]
        if temp_sum > time_limit:
            bad_nodes.add(temp_node)
    ## For each pair, if the paths directly between them are larger than
    ## the time limit it is safe to ignore travel between the pair.
    bad_pairs = {}

    for temp_node_1, temp_edges_1 in enumerate(b_f_times):
        for temp_node_2, temp_edges_2 in enumerate(b_f_times):
            if (temp_edges_1[temp_node_2] > time_limit
                    and temp_edges_2[temp_node_1] > time_limit):
                try:
                    bad_pairs[temp_node_1].add(temp_node_2)
                except KeyError:
                    bad_pairs[temp_node_1] = {temp_node_2}
                try:
                    bad_pairs[temp_node_2].add(temp_node_1)
                except KeyError:
                    bad_pairs[temp_node_2] = {temp_node_1}

    ## Set up the node keepers.
    node_keepers = []
    for temp_node in range(len(times)):
        node_keepers.append(NodeKeeper())

    ## Place all of the nodes that are not bad nodes or part of a bad pair
    ## into a queue to start the search.
    path_queue = queue.Queue()
    for temp_node in range(1, len(times)):
        if temp_node not in bad_nodes:
            try:
                if temp_node not in bad_pairs[0]:
                    path_queue.put(Path(time_limit,
                                        {0, temp_node},
                                        times[0][temp_node],
                                        temp_node, 0, [0]))
            except KeyError:
                path_queue.put(Path(time_limit,
                                    {0, temp_node},
                                    times[0][temp_node],
                                    temp_node, 0, [0]))

    ## While there is anything in the queue pop the first one.
    while not path_queue.empty():
        temp_path = path_queue.get()
        ## Check to see if we have all the bunnies and can exit.
        if (best_bunnies_checker == sorted(temp_path.bunnies_gotten)
                and temp_path.current_row is exit_node
                and temp_path.current_time >= 0):
            return best_bunnies_possible

        ## Loop through the edges extending from the paths current node.
        for node_key, edge in enumerate(times[temp_path.current_row]):
            temp_bunnies = temp_path.bunnies_gotten.copy()
            temp_bunnies.add(node_key)
            new_path = Path(temp_path.current_time,
                            temp_bunnies,
                            edge, node_key,
                            temp_path.path_length,
                            temp_path.path_so_far)

            ## Add the current list of bunnies collected if we are at the
            ## exit node and we still have time.
            temp_set = check_for_exit_bunnies(new_path, exit_node)
            if temp_set is not None:
                if temp_set not in possible_sets:
                    possible_sets.append(temp_set)

            ## Decide whether to put the node back on the queue.
            process_new_node(times, temp_path,
                             node_key, node_keepers,
                             new_path, bad_nodes,
                             bad_pairs, path_queue)

    ## This is the final check.
    try:
        max_len = len(max(possible_sets, key=len))
        ## Find the largest number of bunnies with the lowest identifiers.
        final_list = None
        for item in possible_sets:
            if len(item) == max_len:
                if final_list is not None:
                    if item < final_list:
                        final_list = item
                else:
                    final_list = item
    except ValueError:
        final_list = []

    ## Returns final list of bunnies collected.
    return final_list

def process_new_node(times, temp_path,
                     node_key, node_keepers,
                     new_path, bad_nodes,
                     bad_pairs, path_queue):
    """Checks to see if the new node should be put back on the queue."""
    if (times[temp_path.current_row][node_key] != 0
            or temp_path.current_row is not node_key):
        ## Check to make sure that we haven't done this set of nodes before in
        ## a better time.
        if node_keepers[node_key].check_for_better_path(new_path.bunnies_gotten,
                                                        new_path.path_length,
                                                        new_path.current_time):
            ## If we are in here it means we have a possibly better path to
            ## look at.
            ## Check if the new node key is bad. If it is, skip.
            if node_key not in bad_nodes:
                ## Check if the pair is a bad one.
                try:
                    if node_key not in bad_pairs[temp_path.current_row]:
                        path_queue.put(new_path)
                except KeyError:
                    path_queue.put(new_path)

def check_for_exit_bunnies(new_path, exit_node):
    """Performs checks to see if the current path is useable and Returns
        a list of the nodes visited in the path."""
    if new_path.current_row is exit_node:
        if new_path.current_time >= 0:
            temp_set = new_path.bunnies_gotten.copy()
            temp_set.discard(0)
            temp_set.discard(exit_node)
            temp_set_2 = []
            for item in temp_set:
                temp_set_2.append(item - 1)
            temp_set_2.sort()
            if len(temp_set_2) > 0:
                return temp_set_2

def generate_b_f(times):
    """Simple container to make the Bellman-Ford generation a one liner."""
    b_f_times = []
    for key, _ in enumerate(times):
        b_f_times.append(b_f_general(times, key))
    return b_f_times

def b_f_general(graph_array, current_node):
    """Runs the Bellman-Ford algorithm to find shortest paths."""
    distance = []
    predecessor = []
    ## Step 1: Initialize graph:
    for _ in range(len(graph_array)):
        distance.append(float('inf'))
        predecessor.append(None)

    distance[current_node] = 0

    ## Step 2: Relax edges repeatedly:
    for _ in range(1, len(graph_array)):
        ## For each node_1:
        for node_1, edges in enumerate(graph_array):
            ## For each node_2:
            for node_2, edge in enumerate(edges):
                if distance[node_1] + edge < distance[node_2]:
                    distance[node_2] = distance[node_1] + edge
                    predecessor[node_2] = node_1
    return distance

def infinite_check(graph_array, distance):
    """Runs the Bellman-Ford algorithm to look for infinite loops."""

    ## Check for negative-weight cycles:
    ## For each node_1:
    for node_1, edges in enumerate(graph_array):
        ## For each node_2:
        for node_2, edge in enumerate(edges):
            ## If distance[node_1] + graph_array[node_1][node_2]
            ##      < distance[node_2]:
            if distance[node_1] + edge < distance[node_2]:
                return True
    return False

class NodeKeeper:
    """Used to make sure extra loops are not performed when it is possible
        to run through a loop multiple times without hitting the time limit.
        Check the node keepers when you pull a path off the queue."""
    def __init__(self):
        self.paths = {}

    def check_for_better_path(self, path, path_length, path_time):
        """If this is true, use the path as a seed."""
        temp_tuple = tuple(sorted(path))
        if temp_tuple in self.paths:
            if path_length < self.paths[temp_tuple]['path_length']:
                self.paths[temp_tuple]['path_length'] = path_length
                return True
            if path_time > self.paths[temp_tuple]['path_time']:
                self.paths[temp_tuple]['path_time'] = path_time
                return True
            else:
                return False
        else:
            self.paths[temp_tuple] = {}
            self.paths[temp_tuple]['path_length'] = path_length
            self.paths[temp_tuple]['path_time'] = path_time
            return True

class Path:
    """Contains the information needed to keep track of which nodes a
        particular path has passed through and the current length of
        that path."""
    def __init__(self, start_time,
                 bunnies_gotten, time_delta,
                 current_row, previous_length, previous_path):
        self.current_time = start_time - time_delta
        self.bunnies_gotten = bunnies_gotten
        self.path_so_far = list(previous_path)
        self.path_so_far.append(current_row)
        self.current_row = current_row
        self.path_length = previous_length + 1

if __name__ == "__main__":
    TEST_VALS = [[[0, 1, 1, 1, 1],
                  [1, 0, 1, 1, 1],
                  [1, 1, 0, 1, 1],
                  [1, 1, 1, 0, 1],
                  [1, 1, 1, 1, 0]],
                 [[0, 1, 1, 1, 1, 1, 1],
                  [1, 0, 1, 1, 1, 1, 1],
                  [1, 1, 0, 1, 1, 1, 1],
                  [1, 1, 1, 0, 1, 1, 1],
                  [1, 1, 1, 1, 0, 1, 1],
                  [1, 1, 1, 1, 1, 0, 1],
                  [1, 1, 1, 1, 1, 1, 0]],
                 [[0, 1, 1, 1, -1],
                  [1, 0, 1, 1, 1],
                  [1, 1, 0, 1, 1],
                  [1, 1, 1, 0, 1],
                  [-1, 1, 1, 1, 0]],
                 [[0, 2, 2, 2, -1],
                  [9, 0, 2, 2, -1],
                  [9, 3, 0, 2, -1],
                  [9, 3, 2, 0, -1],
                  [9, 3, 2, 2, 0]],
                 [[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]],
                 [[0, 9, 9],
                  [9, 0, 9],
                  [9, 9, 0]],
                 [[0, 1, 8, 9, 9, 9, 9],
                  [8, 0, 8, 1, 8, 8, 8],
                  [8, 8, 0, 8, 8, 8, 8],
                  [8, 8, 8, 0, 1, 8, 8],
                  [8, 8, 8, 8, 0, 1, 8],
                  [8, 8, 8, 8, 8, 0, 1],
                  [8, 8, 8, 8, 8, 8, 0]]]

    TEST_TIMES = [3, 999, 3, 1, 3, 9, 5]
    TEST_ANSWERS = [[0, 1], ##Right
                    [0, 1, 2, 3, 4], ##Right
                    [0, 1, 2], ##Right
                    [1, 2], ##Wrong
                    [0, 1, 2], ##Right
                    [], ##Right
                    [0, 2, 3, 4]] ##Right
    for i in range(len(TEST_VALS)):
        print(answer(TEST_VALS[i], TEST_TIMES[i]))
    ##print(answer(TEST_VALS[3], TEST_TIMES[3]))
