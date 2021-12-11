#! /usr/bin/env python
import pathlib
import fire
from collections import Counter

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [int(x) for x in path.read_text().strip().split(',')]
        
    def solve(data):
        cnt = Counter()
        positions = set(data)
        for p in positions:
            cnt[p] = sum([abs(x -p) for x in data])
        return min(cnt.values())

    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [int(x) for x in path.read_text().strip().split(',')]
        
    def solve(data):
        cnt = Counter()
        positions = range(min(data), max(data))
        for p in positions:
            cnt[p] = sum([abs(x -p)/2*(x+1-(x-abs(x -p))) for x in data])
        return min(cnt.values())
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    