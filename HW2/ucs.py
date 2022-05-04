import csv
from collections import deque
import heapq as pq
from math import inf
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    '''
    First open edgeFile by using open() and read data by csv.reader()
    Create two dictionaries, the "edges" one stores edges as adjacency list and the "information" one
    stores the corresponding distance and speed with two endpoints ID of the edge as the key.

    Then, we create a min-heap by using heapq, which is sorted by walked distance from start node.
    While doing uniform cost search, we calculate the number of visited nodes and store the parent of current node on certain path.
    After finishing ucs, we get the route by iterating the "parent" dictionary from the end.
    The distance of the route is exactly the first element of the tuple which we last pop from the heap before reaching end.
    Finally, return the results.
    '''
    with open (edgeFile) as f:
        csvreader = csv.reader(f)
        header = f.readline()
      
        edges = {}
        information = {}
        for row in csvreader:
            first = int(row[0])
            second = int(row[1])
            distance = float(row[2])
            speed = float(row[3])
            if first not in edges:
                edges[first] = []
            edges[first].append(second)
            information[(first, second)] = [distance, speed]
    
        dist = 0
        num_visited = 0
        route = deque()
        
        visited = {start: True}
        parent = {}
        queue = []
        pq.heappush(queue, (0, start))

        minDist = {start:0}
        openset = {start:1}
        while queue:
            d, idx = pq.heappop(queue)
            
            num_visited += 1
            
            if idx == end:
                break
        
            for i in edges.get(idx,[]):
                score = minDist.get(idx,inf) + information[(idx, i)][0]
                if score < minDist.get(i, inf):
                    parent[i] = idx
                    minDist[i] = score
                    if openset.get(i, 0) == 0:
                        pq.heappush(queue, (score, i))
                        if i in openset : openset[i] += 1
                        else : openset[i] = 1
                    
        cur = end
        while cur != start:
            route.appendleft(cur)
            cur = parent[cur]
        route.appendleft(start)

        for i in range(len(route)-1):
            dist += information[(route[i], route[i+1])][0]

    return list(route), dist, num_visited
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
