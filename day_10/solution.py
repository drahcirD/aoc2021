#! /usr/bin/env python
from os import chdir
import pathlib
from collections import deque
import fire
import statistics

_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
_MATCHES = {
     ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}
_MATCHES_INV = {v:k for k,v in _MATCHES.items()}
def get_result():
    def parse():
        return [x for x in (pathlib.Path(__file__).resolve().parent / "input1.txt").read_text().split('\n')]
        
    def solve(data):
        res = 0
        for line in data:
            stack = list()
            for c in line:
                if c not in _MATCHES.values():
                    if stack[-1] != _MATCHES[c]:
                        res += _POINTS[c]
                        break
                    else:
                        stack.pop()
                else:
                    stack.append(c)
        return res

    
    return solve(parse())

_POINTS2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}
def get_result2():
    def parse():
        return [x for x in (pathlib.Path(__file__).resolve().parent / "input2.txt").read_text().split('\n')]
        
    def solve(data):
        scores = []
        for line in data:
            stack = list()
            corrupt = False
            for c in line:
                if c not in _MATCHES.values():
                    if stack[-1] != _MATCHES[c]:
                        corrupt = True
                        break
                    else:
                        stack.pop()
                else:
                    stack.append(c)

            if corrupt:
                continue
            score = 0
            missing_chars = []
            for c in stack[::-1]:
                if c not in _MATCHES.values():
                    continue
                score*=5
                score += _POINTS2[_MATCHES_INV[c]]
                missing_chars.append(c)

            scores.append(score)

        
        return statistics.median(sorted(scores))

    
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()
    