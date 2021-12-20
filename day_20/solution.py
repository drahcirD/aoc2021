#! /usr/bin/env python
import pathlib
import fire
import operator

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        enhancement, image = [x for x in path.read_text().split('\n\n')]
        image_dict = {}
        for j, row in enumerate(image.split('\n')):
            for i, c in enumerate(row):
                if c == '#':
                    image_dict[(j,i)] = 1
        return enhancement.strip(), image_dict
        
    def solve(enhancement, image):
        def _get_index(pixel):
            enhancement_code = []
            for offset in neighbor_offsets:
                neighbor = tuple((x+y for x,y in zip(pixel, offset)))
                enhancement_code.append(str(image.get(neighbor, 0)))

            return enhancement_code

        def draw(image):
            for i in range(min_row-5, max_row+6):
                for j in range(min_col-5, max_col+6):
                    try:
                        t = image[(i,j)]
                        assert t == 1
                        print('#', end='')
                    except KeyError:
                        print('.', end='')
                print()
        neighbor_offsets = [(x,y) for x in range(-1, 2) for y in range(-1, 2)]
        for step in range(2):
            image_copy = {}
            if enhancement[0] == '#':
                offset = 2 if step % 2 else 0
            else:
                offset = 0
            min_row = min(image, key=operator.itemgetter(0))[0]+offset
            max_row = max(image, key=operator.itemgetter(0))[0]-offset
            min_col = min(image, key=operator.itemgetter(1))[1]+offset
            max_col = max(image, key=operator.itemgetter(1))[1]-offset

            for i in range(min_row-3+offset, max_row+4-offset):
                for j in range(min_col-3+offset, max_col+4-offset):
                    pixel = (i,j)
                    code = _get_index(pixel)
                    index = int(''.join(code), 2)
                    val = enhancement[index]
                    if val == '#':
                        image_copy[pixel] = 1

            image = image_copy
            draw(image)
            print("="*50)
        
        return len(image)
                

    return solve(*parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        enhancement, image = [x for x in path.read_text().split('\n\n')]
        image_dict = {}
        for j, row in enumerate(image.split('\n')):
            for i, c in enumerate(row):
                if c == '#':
                    image_dict[(j,i)] = 1
        return enhancement.strip(), image_dict
        
    def solve(enhancement, image):
        def _get_index(pixel):
            enhancement_code = []
            for offset in neighbor_offsets:
                neighbor = tuple((x+y for x,y in zip(pixel, offset)))
                enhancement_code.append(str(image.get(neighbor, 0)))

            return enhancement_code

        neighbor_offsets = [(x,y) for x in range(-1, 2) for y in range(-1, 2)]
        for step in range(50):
            image_copy = {}
            if enhancement[0] == '#':
                offset = 2 if step % 2 else 0
            else:
                offset = 0
            min_row = min(image, key=operator.itemgetter(0))[0]+offset
            max_row = max(image, key=operator.itemgetter(0))[0]-offset
            min_col = min(image, key=operator.itemgetter(1))[1]+offset
            max_col = max(image, key=operator.itemgetter(1))[1]-offset

            for i in range(min_row-3+offset, max_row+4-offset):
                for j in range(min_col-3+offset, max_col+4-offset):
                    pixel = (i,j)
                    code = _get_index(pixel)
                    index = int(''.join(code), 2)
                    val = enhancement[index]
                    if val == '#':
                        image_copy[pixel] = 1
            
            image = image_copy
            print(step)
        
        return len(image)
    
    return solve(*parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    