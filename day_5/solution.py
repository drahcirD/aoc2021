#! /usr/bin/env python
import pathlib
from collections import Counter
import fire

def _print_board(cnt):
    for y in  range(10):
        for x in range(10):
            if (x,y) in cnt:
                print(cnt[(x,y)], end='')
            else:
                print('.', end='')
        print()

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [x.split(" -> ") for x in path.read_text().split('\n')]
        
    def solve(data):
        cnt = Counter()
        for d in data:
            p1, p2 = d
            x1, y1 = [int(x) for x in p1.split(',')]
            x2, y2 = [int(x) for x in p2.split(',')]
            points = set()
            if not( x1 == x2 or y1==y2):
                continue
            x_start, x_end = min(x1, x2), max(x1, x2)
            for x in range(x_start, x_end+1):
                p = (x, y1)
                points.add(p)
            y_start, y_end = min(y1, y2), max(y1, y2)
            for y in range(y_start, y_end+1):
                p = (x1, y)
                points.add(p)
            for p in points:
                cnt[p] += 1
        return sum([1 for x, c in cnt.items() if c >= 2])
            
    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [x.split(" -> ") for x in path.read_text().split('\n')]
        
    def solve(data):
        cnt = Counter()
        for d in data:
            p1, p2 = d
            x1, y1 = [int(x) for x in p1.split(',')]
            x2, y2 = [int(x) for x in p2.split(',')]
            points = set()
            x_sign = (x2 - x1)/abs(x2-x1) if x1 != x2 else 0
            y_sign = (y2 - y1)/abs(y2-y1) if y1 != y2 else 0
            p = (x1, y1)
            points.add(p)
            while p != (x2, y2):
                p = (p[0] +1*x_sign, p[1]+1*y_sign)
                points.add(p)
            for p in points:
                cnt[p] += 1
        return sum([1 for x, c in cnt.items() if c >= 2])
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }

if __name__ == '__main__':
  fire.Fire()
    
    