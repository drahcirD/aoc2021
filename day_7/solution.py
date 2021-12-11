#! /usr/bin/env python
import pathlib
import fire
from collections import Counter

def get_result():
    def parse():
        return [int(x) for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().strip().split(',')]
        
    def solve(data):
        cnt = Counter()
        positions = set(data)
        for p in positions:
            cnt[p] = sum([abs(x -p) for x in data])
        return min(cnt.values())

    
    return solve(parse())

def get_result2():
    def parse():
        return [int(x) for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().strip().split(',')]
        
    def solve(data):
        cnt = Counter()
        positions = range(min(data), max(data))
        for p in positions:
            cnt[p] = sum([abs(x -p)/2*(x+1-(x-abs(x -p))) for x in data])
        return min(cnt.values())
    
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()
    