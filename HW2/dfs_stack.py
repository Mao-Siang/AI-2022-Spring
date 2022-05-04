import csv
from collections import deque
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    # raise NotImplementedError("To be implemented")
    '''
    First open edgeFile by using open() and read data by csv.reader()
    Create two dictionaries, the "edges" one stores edges as adjacency list and the "information" one
    stores the corresponding distance and speed with two endpoints ID of the edge as the key.

    Then, we use list as stack to implement dfs. 
    While doing dfs, we store the parent node of the current one and calculate the number of visited nodes.
    After finishing dfs by finding a path from start to end, we iterate the "parent" dictionary and get the route.
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
        # if (first, second) not in information:
        #     information[(first, second)] = []
        information[(first, second)] = [distance, speed]
      
      num_visited = 0
      dist = 0
      route = deque()
      
      parent = {}
      stack = []
      stack.append(start)
      visited = {}
      
      while len(stack) != 0:
        
        back = stack[-1]
        stack.pop(-1)

        visited[back] = True
        num_visited += 1
        if back == end:
          break
        else:
        
            for i in edges.get(back,[]):
                if i not in visited:
                  parent[i] = back
                  stack.append(i)
      cur = end
      while cur != start:
          route.appendleft(cur)
          cur = parent[cur]
      route.appendleft(start)

      for i in range(len(route)-1):
          dist += information[(route[i], route[i+1])][0]

    return list(route), dist, num_visited
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
