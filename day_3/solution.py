#! /usr/bin/env python
import pathlib
import fire
from collections import Counter
import operator

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [tuple(x) for x in path.read_text().split('\n')]
        
    def solve(data):
        counters = [Counter() for x in data[0]]
        for d in data:
            for i, bit in enumerate(d):
                counters[i][bit] += 1
        gamma = f"0b{''.join(['1' if cnt['1'] > cnt['0'] else '0' for cnt in counters])}"
        epsilon = f"0b{''.join(['0' if cnt['1'] > cnt['0'] else '1' for cnt in counters])}"
        return int(gamma,2) * int(epsilon, 2)
    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [tuple(x) for x in path.read_text().split('\n')]
        
    def solve(data):
        def _sub_solve(data, most=True):
            for i in range(len(data[0])):
                cnt = Counter([d[i] for d in data])
                most_common = max(cnt, key=cnt.get)
                least_common = min(cnt, key=cnt.get)
                if most_common == least_common:
                    data = [d for d in data if d[i] == '1' and most or d[i] == '0' and not most]
                elif most:
                    data = [d for d in data if d[i] == most_common]
                else:
                    data = [d for d in data if d[i] == least_common]
                
                if len(data) == 1:
                    return f"0b{''.join(data.pop())}"
        
        return int(_sub_solve(data.copy(), True), 2) * int(_sub_solve(data.copy(), False), 2)



    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    