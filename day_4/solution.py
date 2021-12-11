#! /usr/bin/env python
import pathlib
import fire
import numpy as np

class Board():
    def __init__(self, board):
        self.board = np.array([np.asarray([int(nbr) for nbr in row.split()]) for row in board.split('\n')])
        self.marked = np.zeros(self.board.shape)
    
    def mark(self, value):
        self.marked[np.where(self.board == value)] = 1
    
    def won(self):
        return np.any([row.all() for row in self.marked]) or np.any([row.all() for row in self.marked.T])

    def score(self):
        return np.sum(self.board[np.where(self.marked != 1)])

def get_result():
    def parse():
        data = [x for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().split('\n\n')]
        nbrs = [int(x) for x in data[0].split(',')]
        boards = [Board(d) for d in data[1:]]
        return nbrs, boards
        
    def solve(nbrs, boards):
        for n in nbrs:
            for board in boards:
                board.mark(n)
                if board.won():
                    return board.score() * n

    
    return solve(*parse())

def get_result2():
    def parse():
        data = [x for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().split('\n\n')]
        nbrs = [int(x) for x in data[0].split(',')]
        boards = [Board(d) for d in data[1:]]
        return nbrs, boards
        
    def solve(nbrs, boards):
        last_board = -1
        for n in nbrs:
            for board in boards:
                if board.won():
                    continue
                board.mark(n)
                if board.won():
                    last_board = board.score() * n
        return last_board
    return solve(*parse())

if __name__ == '__main__':
  fire.Fire()
    