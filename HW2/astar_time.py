import csv
import heapq as pq
from collections import deque
from math import inf

edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)

    '''
    First, open the edgeFile by open() and read the file by csv.reader()
    create three dictionaries 
    "edges" : stores the edges as adjacency list
    "rd_time" : stores the time (distance/speedlimit) (with two endpoint ID as key)
    "distance" : stores the distance between edges    (with two endpoint ID as key)
    Then, find the max speed limit and store it in "max_speed"

    Second, open the heuristicFile by using open() and read the file by csv.reader()
    The least time is the distance to the endpoint divided by the max speed limit.

    While doing astar_time algorithm, we calculate the number of visited nodes and 
	store the parent of the current node.

	create a dictionary minTime to store the smallest time cost from start node.
	For every neighbor of current node, check if the cost from start is the smallest.
    if it is smaller than the current smallest one, we update its parent and
	the smallest distance. Also, if it is not in the heap, we push into it.

    After finishing A* time by finding a path from start to end, 
	we iterate the "parent" dictionary and get the route.
    Finally, calculate the distance by the "route" list and "information" dictionary.
    Then return the results.
    '''
    f = open(edgeFile, 'r')
    edge_csv = csv.reader(f)
    header = f.readline()
      
    edges = {}
    rd_time = {}
    distance = {}
    max_speed = -1.0
    for row in edge_csv:
        first = int(row[0])
        second = int(row[1])
        distance[(first, second)] = float(row[2])
        rd_time[(first, second)] = float(row[2]) / float(row[3]) * 3.6
        max_speed = max(max_speed, float(row[3]))
        if first not in edges:
            edges[first] = []
        edges[first].append(second)
    f.close()
    

    max_speed /= 3.6

    # read heuristic file
    f = open(heuristicFile, 'r')
    heuristic_csv = csv.reader(f)
    
    timeToDest = {}
    for i, row in enumerate(heuristic_csv):
      if i == 0: 
        a = int(row[1])
        b = int(row[2])
        c = int(row[3])
      else :
        timeToDest[int(row[0])] = {a : float(row[1])/max_speed, b :float(row[2])/max_speed, c : float(row[3])/max_speed}
    
    f.close()

    # astar algorithm
    route = deque()
    time = 0
    num_visited = 0

    parent = {}
    queue = []
    minTime = {start: 0}
   
    pq.heappush(queue, (timeToDest[start][end], 0, start))
    openset = {start:1}

    while len(queue) > 0:
        _, dis, idx = pq.heappop(queue) 
        num_visited += 1
        openset[idx] -= 1

        if idx == end:
            break
        
        for i in edges.get(idx, []):
            g_score = minTime.get(idx,inf) + rd_time[(idx, i)]
            if g_score < minTime.get(i, inf):
                parent[i] = idx
                minTime[i] = g_score
                h_score = g_score + timeToDest[i][end]
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
        time += rd_time[(route[i], route[i+1])]

    return list(route), time, num_visited
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
