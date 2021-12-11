#! /usr/bin/env python
from collections import defaultdict
import pathlib
import fire
import numpy as np

def get_result():
    def parse():
        return np.array([np.asarray([int(nbr) for nbr in row]) for row in (pathlib.Path(__file__).resolve().parent / "input1.txt").read_text().split('\n')])
        
    def solve(data):
        array = np.pad(data, pad_width=1, mode='constant', constant_values=10)
        low_points = []
        for c in range(1, array.shape[1]-1):
            for r in range(1, array.shape[0]-1):
                up = array[r-1, c]
                down = array[r+1, c]
                left = array[r, c-1]
                right = array[r, c+1]
                cur = array[r,c]
                if cur < up and cur < down and cur < left and cur < right:
                    low_points.append(cur)
        return sum(low_points) + len(low_points)


    
    return solve(parse())

def get_result2():
    def parse():
        return np.array([np.asarray([int(nbr) for nbr in row]) for row in (pathlib.Path(__file__).resolve().parent / "input2.txt").read_text().split('\n')])
        
    def solve(data):
        array = np.pad(data, pad_width=1, mode='constant', constant_values=10)
        low_points = []
        for c in range(1, array.shape[1]-1):
            for r in range(1, array.shape[0]-1):
                up = array[r-1, c]
                down = array[r+1, c]
                left = array[r, c-1]
                right = array[r, c+1]
                cur = array[r,c]
                if cur < up and cur < down and cur < left and cur < right:
                    low_points.append((r,c))
        
        basins = {point: set() for point in low_points}
        def _explore(visited, index, result_set):
            if index in visited:
                return
            visited.add(index)
            if array[index] in {9, 10} or index[0] >= array.shape[0] or index[0] < 0 or index[1] >= array.shape[1] or index[1] < 0:
                return
            result_set.add(index)
            row, col = index
            _explore(visited, (row-1, col), result_set)
            _explore(visited, (row+1, col), result_set)
            _explore(visited, (row, col-1), result_set)
            _explore(visited, (row, col+1), result_set)


        for coord, basin in basins.items():
            _explore(set(), coord, basin)
        
        basin_sizes = sorted([len(v) for v in basins.values()])
        return basin_sizes[-1]*basin_sizes[-2]*basin_sizes[-3]

    
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()
    