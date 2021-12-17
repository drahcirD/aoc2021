#! /usr/bin/env python
import pathlib
import fire
import itertools
import random

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        data = [x.split('..') for x in path.read_text().strip().replace('target area: ','').split(', ')]

        data[0][0]=data[0][0].replace('x=', '')
        data[1][0]=data[1][0].replace('y=', '')
        return data

        
    def solve(data):
        x, y = data
        x0, x1 = [int(i) for i in x]
        y0, y1 = [int(i) for i in y]
        
        def _simulate(v0):
            p = (0, 0)
            v = v0
            max_y = float('-inf')
            while (p[0] < x1 and v[0]>0 or v[0] == 0 and x0<= p[0] <=x1) and not (p[1] < y0 and v[1]<0) :
                p = (p[0]+v[0], p[1]+v[1])
                v_sign = v[0]/abs(v[0]) if v[0] != 0 else 0
                v = (v[0]+-1*v_sign, v[1]-1)

                if p[1] > max_y:
                    max_y = p[1]

                if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                    return True, max_y
            
            
            if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                return True, max_y
            return False, -1
            
        velocities = list(itertools.product(range(0,500),repeat=2))
        negative_y = [(x[0], -1*x[1]) for x in velocities]
        velocities = list(itertools.chain(velocities, negative_y))
        random.shuffle(velocities)
        y_list = []
  
        for vel in velocities:
            res, max_y =  _simulate(vel)
            if res:
                y_list.append(max_y)
        
        return max(y_list)
    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        data = [x.split('..') for x in path.read_text().strip().replace('target area: ','').split(', ')]

        data[0][0]=data[0][0].replace('x=', '')
        data[1][0]=data[1][0].replace('y=', '')
        return data

        
    def solve(data):
        x, y = data
        x0, x1 = [int(i) for i in x]
        y0, y1 = [int(i) for i in y]
        
        def _simulate(v0):
            p = (0, 0)
            v = v0
            max_y = float('-inf')
            while (p[0] < x1 and v[0]>0 or v[0] == 0 and x0<= p[0] <=x1) and not (p[1] < y0 and v[1]<0) :
                p = (p[0]+v[0], p[1]+v[1])
                v_sign = v[0]/abs(v[0]) if v[0] != 0 else 0
                v = (v[0]+-1*v_sign, v[1]-1)

                if p[1] > max_y:
                    max_y = p[1]

                if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                    return True, max_y
            
            
            if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                return True, max_y
            return False, -1
            
        velocities = list(itertools.product(range(0,500),repeat=2))
        negative_y = [(x[0], -1*x[1]) for x in velocities]
        velocities = list(itertools.chain(velocities, negative_y))
        random.shuffle(velocities)
        vels = set()
  
        for vel in velocities:
            res, _ =  _simulate(vel)
            if res:
                vels.add(vel)
        return len(vels)
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    