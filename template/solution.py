#! /usr/bin/env python
import pathlib
import fire

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [int(x) for x in path.read_text().split('\n')]
        
    def solve(data):
        pass
    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [int(x) for x in path.read_text().split('\n')]
        
    def solve(data):
        pass
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    