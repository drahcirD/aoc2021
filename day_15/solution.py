#! /usr/bin/env python
import pathlib
import fire
import numpy as np
import sys
from queue import PriorityQueue

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return np.array([np.asarray([int(nbr) for nbr in row]) for row in path.read_text().split('\n')])
        
    def solve(data):
        for i in range(1, data.shape[0]):
            data[i,0] += data[i - 1,0]
    
        for j in range(1, data.shape[1]):
            data[0,j] += data[0,j - 1]

        for i in range(1, data.shape[0]):
            for j in range(1, data.shape[1]):
                data[i][j] += (min(data[i - 1][j],
                                data[i][j - 1]))
        
        return data[data.shape[0] - 1][data.shape[1] - 1] - data[0,0]
        
    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        data = np.array([np.asarray([int(nbr) for nbr in row]) for row in path.read_text().split('\n')])
        row,col=data.shape
        new_data = np.zeros((row*5, col*5))
        for i in range(5):
            for j in range(5):
                ins = data + i+j
                ins[np.where(ins > 9)] -= 9
                new_data[row*i:row*(i+1), col*j:col*(j+1)] = ins
        return new_data
        
    def solve(data):
        def dijkstra(start_vertex):
            distances = np.full_like(data, sys.maxsize)
            distances[start_vertex] = 0

            visited = set()
            pq = PriorityQueue()
            pq.put((0, start_vertex))

            while not pq.empty():
                (cur_dist, cur) = pq.get()
                visited.add(cur)
                r,c = cur
                neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                for neighbor in neighbors:
                    if neighbor[0] >= data.shape[0] or neighbor[0] < 0 or neighbor[1] >= data.shape[1] or neighbor[1] < 0:
                        continue

                    neighbor_dist = data[neighbor]
                    if neighbor not in visited:
                        old_path_cost = distances[neighbor]
                        new_path_cost = cur_dist + neighbor_dist
                        if new_path_cost < old_path_cost:
                            pq.put((new_path_cost, neighbor))
                            distances[neighbor] = new_path_cost
            return distances
        return dijkstra((0,0))[data.shape[0] - 1][data.shape[1] - 1]
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    