#! /usr/bin/env python
import pathlib
import fire
import itertools
from collections import Counter


def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [int(x) for x in path.read_text().split()]
        
    def solve(data):
        return sum([1 for prev, next in itertools.pairwise(data) if next > prev])

    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [int(x) for x in path.read_text().split()]
        
    def solve(data):
        temp = [sum([one, two, three]) for one, two, three in zip(data, data[1:], data[2:])]
        return sum([1 for prev, next in itertools.pairwise(temp)  if next > prev])
        
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    