#! /usr/bin/env python
import pathlib
import fire
import numpy as np
import operator

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        indices, folds = [x for x in path.read_text().split('\n\n')]
        inds = [(int(x.split(',')[0]), int(x.split(',')[1].strip())) for x in indices.split('\n')]
        folds = [fold.replace("fold along ", "").strip() for fold in folds.split('\n')]
        max_y = max(inds, key=operator.itemgetter(1))[1]
        max_x = max(inds, key=operator.itemgetter(0))[0]
        matrix = np.zeros((max_y+1, max_x+1))
        for ind in inds:
            y,x = ind
            matrix[x,y] = 1
        return matrix, folds
        
    def solve(matrix, folds):
        for fold in folds:
            direction, pos = fold.split('=')
            pos = int(pos)
            if direction == 'y':
                matrix = matrix[:pos,:] + np.flipud(matrix[pos+1:,:])
            elif direction == 'x':
                matrix = matrix[:, :pos] + np.fliplr(matrix[:,pos+1:])
            break
    
        return len(np.where(matrix >=1)[0])

    
    return solve(*parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        indices, folds = [x for x in path.read_text().split('\n\n')]
        inds = [(int(x.split(',')[0]), int(x.split(',')[1].strip())) for x in indices.split('\n')]
        folds = [fold.replace("fold along ", "").strip() for fold in folds.split('\n')]
        max_y = max(inds, key=operator.itemgetter(1))[1]
        max_x = max(inds, key=operator.itemgetter(0))[0]
        matrix = np.zeros((max_y+1, max_x+1))
        for ind in inds:
            y,x = ind
            matrix[x,y] = 1
        return matrix, folds
        
    def solve(matrix, folds):
        for fold in folds:
            direction, pos = fold.split('=')
            pos = int(pos)
            if direction == 'y':
                matrix = matrix[:pos,:] + np.flipud(matrix[pos+1:,:])
            elif direction == 'x':
                matrix = matrix[:, :pos] + np.fliplr(matrix[:,pos+1:])
    
        matrix[np.where(matrix >=1)] = 1
        with np.printoptions(precision=4, suppress=True, formatter={'int': '{%d}'.format}, linewidth=1000):
            print(matrix)
        return len(np.where(matrix >=1)[0])

    return solve(*parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    