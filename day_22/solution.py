#! /usr/bin/env python
from collections import defaultdict
import pathlib
from typing import List, Set
import fire
import functools
import operator
import itertools


def get_result(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        data = [x.split(" ") for x in path.read_text().split("\n")]
        new_data = []

        for d in data:
            coords = [x.split("..") for x in d[1].split(",")]
            for i, c in enumerate(["x", "y", "z"]):
                coords[i][0] = int(coords[i][0].replace(f"{c}=", ""))
                coords[i][1] = int(coords[i][1])
            new_data.append((d[0], [tuple(x) for x in coords]))
        return new_data

    def solve(data):

        cube = {}
        print("=" * 50)
        for d in data:
            for x in range(-50, 51):
                if not (d[1][0][0] <= x <= d[1][0][1]):
                    continue
                for y in range(-50, 51):
                    if not (d[1][1][0] <= y <= d[1][1][1]):
                        continue
                    for z in range(-50, 51):
                        if not (d[1][2][0] <= z <= d[1][2][1]):
                            continue
                        if d[0] == "on":
                            cube[(x, y, z)] = 1
                        else:
                            try:
                                del cube[(x, y, z)]
                            except KeyError:
                                pass
        return len(cube)

    return solve(parse())


class Cuboid:
    def intersect(self, other):
        x1 = max(self.x1, other.x1)
        y1 = max(self.y1, other.y1)
        z1 = max(self.z1, other.z1)
        x2 = min(self.x2, other.x2)
        y2 = min(self.y2, other.y2)
        z2 = min(self.z2, other.z2)

        if x1 < x2 and y1 < y2 and z1 < z2:
            return Cuboid(x1, y1, z1, x2, y2, z2, status=not self.status)
 

    def volume(self):
        return (self.x2 - self.x1+1) * (self.y2 - self.y1+1) * (self.z2 - self.z1+1)

    def __init__(self, x1, y1, z1, x2, y2, z2, status=True):
        if x1 > x2 or y1 > y2 or z1 > z2:
            raise ValueError
        self.x1, self.y1, self.z1 = x1, y1, z1
        self.x2, self.y2, self.z2 = x2, y2, z2
        self.status = status


def get_result2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        data = [x.split(" ") for x in path.read_text().split("\n")]
        new_data = []

        for d in data:
            coords = [x.split("..") for x in d[1].split(",")]
            for i, c in enumerate(["x", "y", "z"]):
                coords[i][0] = int(coords[i][0].replace(f"{c}=", ""))
                coords[i][1] = int(coords[i][1])
            new_data.append((d[0], [tuple(x) for x in coords]))
        return new_data
    
    def solve(data):

        cubes = []

        for d in data:
            start = tuple([x[0] for x in d[1]])
            end = tuple([x[1] for x in d[1]])
            new_cubes = []
            cuboid_a = Cuboid(*start, *end, d[0]=='on')
            for cuboid_b in cubes:
                new_cubes.append(cuboid_b)
                if intersection := cuboid_b.intersect(cuboid_a):
                    new_cubes.append(intersection)

            if cuboid_a.status:
                new_cubes.append(cuboid_a)

            cubes = new_cubes
        return sum((c.volume() for c in cubes if c.status)) - sum((c.volume() for c in cubes if not c.status))
    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    example2 = pathlib.Path(__file__).resolve().parent / "example2.txt"
    example3 = pathlib.Path(__file__).resolve().parent / "example3.txt"
    return {
        "part1": {"example": get_result(example), "example2": get_result(example2), "input": get_result()},
        "part2": {"example3": get_result2(example3), "input": get_result2()},
    }


if __name__ == "__main__":
    fire.Fire()
