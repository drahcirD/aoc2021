#! /usr/bin/env python
import itertools
import pathlib
import fire
from itertools import pairwise
from collections import Counter
from functools import lru_cache

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        template, adj = [x for x in path.read_text().split('\n\n')]
        adj = {x.split(" -> ")[0]:x.split(" -> ")[1] for x in adj.split('\n')}
        return template, adj       
    def solve(template, adj):
        for step in range(10):
            res = list(template)
            offset = 0
            for i in range(len(template)-1):
                s = template[i]+template[i+1]
                ins = adj[s]
                res.insert(i+1+offset, ins)
                offset +=1
            template = ''.join(res)
        cnt = Counter(template)
        most_common = max(cnt, key=cnt.get)
        least_common = min(cnt, key=cnt.get)
        return cnt[most_common] - cnt[least_common]


    
    return solve(*parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        template, adj = [x for x in path.read_text().split('\n\n')]
        adj = {tuple(x.split(" -> ")[0]):x.split(" -> ")[1] for x in adj.split('\n')}
        return template, adj       
    def solve(template, adj):
        pairs = Counter(pairwise(template))
        cnt = Counter(template)
        for step in range(1,41):
            new_pairs = Counter()
            for pair, nbr in pairs.items():
                ins = adj[pair]
                new_pairs[(pair[0], ins)]+=nbr
                new_pairs[(ins, pair[1])]+=nbr
                cnt[ins] += nbr
            pairs = new_pairs
        most_common = max(cnt, key=cnt.get)
        least_common = min(cnt, key=cnt.get)
        return cnt[most_common] - cnt[least_common]
    
    return solve(*parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    