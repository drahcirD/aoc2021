#! /usr/bin/env python
from functools import cache
import pathlib
import fire
import itertools
def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [int([y for y in x.split(': ')][1]) for x in path.read_text().split('\n')]
        
    def solve(data):
        
        won = False
        die = itertools.cycle(range(1, 101))
        scores = {i+1:0 for i, x in enumerate(data)}
        rolls = 0
        while not won:
            for player, place in enumerate(data):
                pos = place
                for _ in range(3):
                    roll = next(die)
                    pos += roll
                    rolls +=1
                pos = 1 + (pos - 1) % (11 - 1)
                data[player] = pos
                scores[player+1] += pos
                if scores[player+1] >=1000:
                    won = True
                    break
        return scores[min(scores, key=scores.get)]*rolls


    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [int([y for y in x.split(': ')][1]) for x in path.read_text().split('\n')]
        
    def solve(data):        
        @cache
        def play(roll, n_rolls, turn, pos1, pos2, score1, score2):
            if turn == 1:
                pos1 += roll
                pos1 = 1 + (pos1 - 1) % (11 - 1)              
            elif turn == 2:
                pos2 += roll
                pos2 = 1 + (pos2 - 1) % (11 - 1)

            n_rolls = 1 + (n_rolls - 1) % (4 - 1)
            if n_rolls == 3 and turn == 1:
                score1 += pos1
                if score1 >= 21:
                    return 1, 0
                turn = 2
            elif n_rolls == 3 and turn == 2:
                score2 += pos2
                if score2 >= 21:
                    return 0, 1
                turn = 1
    
            wins = zip(play(1, n_rolls+1, turn, pos1, pos2, score1, score2), 
                        play(2, n_rolls+1, turn, pos1, pos2, score1, score2),
                        play(3, n_rolls+1, turn, pos1, pos2, score1, score2))
            return [sum(x) for x in wins]

        wins = zip(play(1, 1, 1, data[0], data[1], 0, 0),
            play(2, 1, 1, data[0], data[1], 0, 0),
            play(3, 1, 1, data[0], data[1], 0, 0))
        return max((sum(x) for x in wins))
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    