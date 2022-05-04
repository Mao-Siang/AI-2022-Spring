import csv
from collections import deque
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    '''
    First, open the edgeFile by using open() and read the file by using csv.reader()
    Create two dictionaries, the "edges" one stores edges as adjacency list and the "information" one
    stores the corresponding distance and speed with two endpoints ID of the edge as the key.

    Then, we do bfs from the start point and store the parent of the node on the current path simutaneously.
    Also, we caculate the number of the visited nodes.
    After finishing bfs by finding a path from start to end, we iterate the "parent" dictionary and get the route.
    Finally, we calculate the distance by the "route" list and "information" dictionary.
    Then return the results.
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

        parent = {}
        visited = {}
        queue = deque()
        queue.append(start)

        while len(queue)>0:
            front = queue[0]
            queue.popleft()
            if front == end:
                break
            
            num_visited += 1

            for i in edges.get(front,[]):
                if i not in visited:
                    visited[i] = True
                    queue.append(i)
                    parent[i] = front
        cur = end
        while cur != start:
            route.appendleft(cur)
            cur = parent[cur]
        route.appendleft(start)

        for i in range(len(route)-1):
            dist += information[(route[i], route[i+1])][0]

    return list(route), dist, num_visited
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
