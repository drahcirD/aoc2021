#! /usr/bin/env python
import pathlib
import fire

def get_result():
    def parse():
        return [x.split(' ') for x in (pathlib.Path(__file__).resolve().parent / "input1.txt").read_text().split('\n')]
        
    def solve(data):
        depth = 0
        position = 0
        for d in data:
            direction, length = d
            match direction:
                case 'forward':
                    position += int(length)
                case 'down':
                    depth += int(length)
                case 'up':
                    depth -= int(length)
        return depth*position
    
    return solve(parse())

def get_result2():
    def parse():
        return [x.split(' ') for x in (pathlib.Path(__file__).resolve().parent / "input1.txt").read_text().split('\n')]
        
    def solve(data):
        depth = 0
        position = 0
        aim = 0
        for d in data:
            direction, length = d
            match direction:
                case 'forward':
                    position += int(length)
                    depth += int(length)*aim
                case 'down':
                    aim += int(length)
                case 'up':
                    aim -= int(length)
        return depth*position
    
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()