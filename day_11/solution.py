#! /usr/bin/env python
import pathlib
import fire
import numpy as np

def get_result():
    def parse():
        return np.array([np.asarray([int(nbr) for nbr in row]) for row in (pathlib.Path(__file__).resolve().parent / "input1.txt").read_text().split('\n')])
        
    def solve(data):
        flashes = 0
        def _add_to_neighbors(data, index):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    neighbor = (index[0]+i, index[1]+j)
                    if neighbor[0] >= data.shape[0] or neighbor[0] < 0 or neighbor[1] >= data.shape[1] or neighbor[1] < 0:
                        continue
                    data[neighbor] += 1


        for _ in range(100):
            data += 1
            already_flashed = set()
            running = True
            while running:
                new_flashes = set()
                for i, j in zip(*np.where(data > 9)):
                    index = (i, j)
                    if index in already_flashed:
                        continue
                    _add_to_neighbors(data, index, already_flashed)
                    new_flashes.add(index)
                running = len(new_flashes - already_flashed) > 0
                already_flashed.update(new_flashes)
            for index in already_flashed:
                data[index] = 0
            flashes += len(already_flashed)
        
        return flashes
    
    return solve(parse())

def get_result2():
    def parse():
        return np.array([np.asarray([int(nbr) for nbr in row]) for row in (pathlib.Path(__file__).resolve().parent / "input2.txt").read_text().split('\n')])
        
    def solve(data):
        flashes = 0
        def _add_to_neighbors(data, index):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    neighbor = (index[0]+i, index[1]+j)
                    if neighbor[0] >= data.shape[0] or neighbor[0] < 0 or neighbor[1] >= data.shape[1] or neighbor[1] < 0:
                        continue
                    data[neighbor] += 1

        step = 0
        while True:
            step+=1
            data += 1
            already_flashed = set()
            running = True
            while running:
                new_flashes = set()
                for i, j in zip(*np.where(data > 9)):
                    index = (i, j)
                    if index in already_flashed:
                        continue
                    _add_to_neighbors(data, index, already_flashed)
                    new_flashes.add(index)
                running = len(new_flashes - already_flashed) > 0
                already_flashed.update(new_flashes)
            if len(already_flashed) == data.size:
                break
            for index in already_flashed:
                data[index] = 0
            flashes += len(already_flashed)
        return step
    
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()
    