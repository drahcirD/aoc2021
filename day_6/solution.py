#! /usr/bin/env python
from operator import itemgetter
import pathlib
from typing import Counter
import fire

def get_result():
    def parse():
        return [int(x) for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().strip().split(',')]
        
    def solve(data):
        for day in range(1, 81):
            new_fish = []
            for i, time in enumerate(data):
                if time == 0:
                    new_fish.append(8)
                    data[i] = 6
                else:
                    data[i]-=1
            data.extend(new_fish)
        return len(data)
    
    return solve(parse())

def get_result2():
    def parse():
        return [int(x) for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().strip().split(',')]
        
    def solve(data):
        res = Counter(data)
        for day in range(1, 257):
            for k, v in res.copy().items():
                res[k-1] += v
                res[k] -= v
            res[8] += res[-1]
            res[6] += res[-1]
            del res[-1]
        return sum([v for v in res.values()])
    
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()
    