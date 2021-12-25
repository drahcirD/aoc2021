#! /usr/bin/env python
import pathlib
import fire
import numpy as np
import operator

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        data = {(i,j): x for j, row in enumerate(path.read_text().split('\n')) for i, x in enumerate(row) if x != '.'}
        return data
    
    def solve(data):
        step = 1
        moved = False
        max_x = max(data, key=operator.itemgetter(0))[0]+1
        max_y = max(data, key=operator.itemgetter(1))[1]+1
        while True:
            moved = False
            tmp = data.copy()
            for pos, sc in data.items():
                if sc == '>':
                    x = pos[0]+1
                    x = 0 if x >= max_x else x
                    try:
                        data[(x, pos[1])]
                    except:
                        tmp[(x, pos[1])] = '>'
                        tmp.pop(pos)
                        moved = True
            data = tmp
            tmp = data.copy()
            for pos, sc in data.items():
                if sc == 'v':
                    y = pos[1]+1
                    y = 0 if y >= max_y else y
                    try:
                        data[(pos[0], y)]
                    except:
                        tmp[(pos[0], y)] = 'v'
                        tmp.pop(pos)
                        moved = True
            data = tmp
            if not moved:
                break
            step +=1
            
        return step
    
    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()}
    }


if __name__ == '__main__':
  fire.Fire()
    
    