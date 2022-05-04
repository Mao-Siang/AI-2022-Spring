from collections import deque
import csv
import heapq as pq


from math import inf

edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    '''
    First, open the edgeFile by open() and read the file by csv.reader()
    Create two dictionaries, 
	the "edges" one stores edges as adjacency list and 
	the "information" one stores the corresponding distance and speed 
	with two endpoints ID of the edge as the key.

    Second, open the heuristicFile by using open() and read the file by csv.reader()
    Create dictionary "DistToEnd", 
	which stores the distance to corresponding endpoint.
    
	During astar algorithm, we calculate the number of visited nodes and 
	store the parent of the current node.
		
	create a dictionary minDist to store the smallest cost from start node.
	For every neighbor of current node, check if the cost from start is the smallest.
    if it is smaller than the current smallest one, we update its parent and
	the smallest distance. Also, if it is not in the heap, we push into it.
     
    After finishing astar by finding a path from start to end, 
    we iterate the "parent" dictionary from the end and get the route.
    Finally, calculate the distance by "route" list and "information" dictionary.
    Then return the results.

    '''
    # read edgeFile
    f = open(edgeFile, 'r')
    edge_csv = csv.reader(f)
    header = f.readline()
      
    edges = {}
    information = {}
    for row in edge_csv:
        first = int(row[0])
        second = int(row[1])
        distance = float(row[2])
        speed = float(row[3])
        if first not in edges:
            edges[first] = []
        edges[first].append(second)
        information[(first, second)] = (distance, speed)
    f.close()
    
    # read heuristic file
    f = open(heuristicFile, 'r')
    heuristic_csv = csv.reader(f)
    
    DistToEnd = {}
    for i, row in enumerate(heuristic_csv):
      if i == 0: 
        a = int(row[1])
        b = int(row[2])
        c = int(row[3])
      else :
        DistToEnd[int(row[0])] = {a : float(row[1]), b : float(row[2]), c : float(row[3])}
    
    f.close()

    # astar algorithm
    route = deque()
    dist = 0
    num_visited = 0

    parent = {}
    queue = []
    minDist = {start: 0}
   
    pq.heappush(queue, (DistToEnd[start][end], 0, start))
    openset = {start:1}

    while len(queue) > 0:
        _, dis, idx = pq.heappop(queue) 
        num_visited += 1
        openset[idx] -= 1

        if idx == end:
            break
        
        for i in edges.get(idx, []):
            g_score = minDist.get(idx,inf) + information[(idx, i)][0]
            if g_score < minDist.get(i, inf):
                parent[i] = idx
                minDist[i] = g_score
                h_score = g_score + DistToEnd[i][end]
                if openset.get(i, 0) == 0:
                    pq.heappush(queue, (h_score, g_score, i))
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
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
