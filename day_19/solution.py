#! /usr/bin/env python
import collections
import pathlib
import fire
import itertools
from collections import Counter, defaultdict
import numpy as np

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        data = [x for x in path.read_text().split('\n\n')]
        scanners = {}
        for i, scanner in enumerate(data):
            scanners[i] = [tuple([int(y) for y in x.split(',')]) for x in scanner.split('\n')[1:]]
        return scanners

    def solve(data):
        ind_start = list(itertools.permutations(range(3), 3))
        indexing = set()
        for index in ind_start:
            for i in {-1, 1}:
                for j in {-1, 1}:
                    for k in {-1, 1}:
                        indexing.add((index,(i,j,k)))

        scanner_positions = {0: (0,0,0)}
        known_scanners = {0: data[0]}
        
        tried_and_failed = defaultdict(set)
        old_found = 0
        while len(known_scanners) < len(data):
            found_new = False
            for known_scanner, known_beacons in known_scanners.items():
                for scanner, beacons in data.items():
                    if scanner in scanner_positions or scanner in tried_and_failed[known_scanner]:
                        continue
                    for ind in indexing:
                        diffs = Counter()
                        rotated_beacons = [tuple([beacon[i]*sign for i, sign in zip(ind[0], ind[1])]) for beacon in beacons]
                        diffs = Counter(tuple((x-y for x,y in zip(b1,b2))) for b1 in known_beacons for b2 in rotated_beacons)
                        more_than_12 = [diff for diff, times in diffs.items() if times >=12]
                        if more_than_12:
                            assert len(more_than_12) == 1
                            scanner_pos = more_than_12.pop()
                            scanner_positions[scanner] = scanner_pos
                            known_scanners[scanner] = [tuple([i+j for i,j in zip(scanner_pos, beacon)]) for beacon in rotated_beacons]
                            found_new = True
                            break

                    if not found_new:
                        tried_and_failed[known_scanner].add(scanner)
                    
                if found_new:
                    break
            if old_found == len(known_scanners):
                tried_and_failed = defaultdict(set)
            old_found = len(known_scanners)
        unique_beacons = set()
        for known_scanner, known_beacons in known_scanners.items():
            unique_beacons.update(known_beacons)

        return len(unique_beacons)
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        data = [x for x in path.read_text().split('\n\n')]
        scanners = {}
        for i, scanner in enumerate(data):
            scanners[i] = [tuple([int(y) for y in x.split(',')]) for x in scanner.split('\n')[1:]]
        return scanners

    def solve(data):
        ind_start = list(itertools.permutations(range(3), 3))
        indexing = set()
        for index in ind_start:
            for i in {-1, 1}:
                for j in {-1, 1}:
                    for k in {-1, 1}:
                        indexing.add((index,(i,j,k)))

        scanner_positions = {0: (0,0,0)}
        known_scanners = {0: data[0]}
        
        tried_and_failed = defaultdict(set)
        old_found = 0
        while len(known_scanners) < len(data):
            found_new = False
            for known_scanner, known_beacons in known_scanners.items():
                for scanner, beacons in data.items():
                    if scanner in scanner_positions or scanner in tried_and_failed[known_scanner]:
                        continue
                    for ind in indexing:
                        diffs = Counter()
                        rotated_beacons = [tuple([beacon[i]*sign for i, sign in zip(ind[0], ind[1])]) for beacon in beacons]
                        diffs = Counter(tuple((x-y for x,y in zip(b1,b2))) for b1 in known_beacons for b2 in rotated_beacons)
                        more_than_12 = [diff for diff, times in diffs.items() if times >=12]
                        if more_than_12:
                            assert len(more_than_12) == 1
                            scanner_pos = more_than_12.pop()
                            scanner_positions[scanner] = scanner_pos
                            known_scanners[scanner] = [tuple([i+j for i,j in zip(scanner_pos, beacon)]) for beacon in rotated_beacons]
                            found_new = True
                            break

                    if not found_new:
                        tried_and_failed[known_scanner].add(scanner)
                    
                if found_new:
                    break
            if old_found == len(known_scanners):
                tried_and_failed = defaultdict(set)
            old_found = len(known_scanners)
        
        def manhattan(first, second):
            return sum(abs(x -y) for x,y in zip(first, second))
        return max((manhattan(x,y) for x,y in itertools.product(scanner_positions.values(), repeat=2)))
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    