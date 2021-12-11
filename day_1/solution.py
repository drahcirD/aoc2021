#! /usr/bin/env python
import pathlib
import fire
import itertools
from collections import Counter


def get_result():
    def parse():
        return [int(x) for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().split()]
        
    def solve(data):
        return sum([1 for prev, next in itertools.pairwise(data) if next > prev])

    
    return solve(parse())

def get_result2():
    def parse():
        return [int(x) for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().split()]
        
    def solve(data):
        temp = [sum([one, two, three]) for one, two, three in zip(data, data[1:], data[2:])]
        return sum([1 for prev, next in itertools.pairwise(temp)  if next > prev])
        
    
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()
    