#! /usr/bin/env python
import pathlib
import fire

def get_result():
    def parse():
        return [int(x) for x in (pathlib.Path(__file__).resolve().parent / "input1.txt").read_text().split('\n')]
        
    def solve(data):
        pass
    
    return solve(parse())

def get_result2():
    def parse():
        return [int(x) for x in (pathlib.Path(__file__).resolve().parent / "input1.txt").read_text().split('\n')]
        
    def solve(data):
        pass
    
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()
    