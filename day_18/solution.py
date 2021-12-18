#! /usr/bin/env python
from copy import deepcopy
import pathlib
import fire
import math
import itertools

def _is_pair(snail):
    if isinstance(snail, list) and len(snail) == 2:
        return isinstance(snail[0], MyNumber) and isinstance(snail[1], MyNumber)
    return False


class MyNumber:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"

class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"[{self.left},{self.right}]"

def find_left_number(snail:list, pair: Pair, left:MyNumber):
    if snail == pair:
       return left
    for val in snail:
        if isinstance(val, MyNumber):
            left = val
        elif isinstance(val, Pair) and val != pair:
            left = val.right
        elif isinstance(val, list):
           left, res = find_left_number(val, pair, left)
           if res:
               return left, True
        elif val == pair:
            return left, True
    return left, False

def find_right_number(snail:list, pair: Pair, pair_found:bool):
    if snail == pair:
        return True
    for val in snail:
        if isinstance(val, MyNumber) and pair_found:
           return val, True
        elif isinstance(val, Pair) and val != pair and pair_found:
            return val.left, True
        elif isinstance(val, list):
            right_value, pair_found = find_right_number(val, pair, pair_found)
            if right_value and pair_found:
                return right_value, pair_found
        elif val == pair:
            pair_found = True
    return None, pair_found

def explode(outmost_snail:list, snail:list, level):
    for i, val in enumerate(snail):
        if isinstance(val, list):
            if explode(outmost_snail, val, level+1):
                return True
        elif isinstance(val, Pair) and level == 4:
            left, _ = find_left_number(outmost_snail, val, None)
            right,_ = find_right_number(outmost_snail, val, False)
            if left:
                left.value += val.left.value
            if right:
                right.value += val.right.value
            old = snail.pop(i)
            snail.insert(i, MyNumber(0))
            return True

    return False

def convert(snail: list):
    for i, val in enumerate(snail):
        if _is_pair(val):
            snail.pop(i)
            assert isinstance(val[0], MyNumber)
            assert isinstance(val[1], MyNumber)
            snail.insert(i, Pair(val[0], val[1]))
            return True
        elif isinstance(val, list):
            if convert(val):
                return True
    return False

def unconvert(snail: list):
    for i, val in enumerate(snail):
        if isinstance(val, Pair):
            snail.pop(i)
            snail.insert(i, [val.left, val.right])
            return True
        elif isinstance(val, MyNumber):
            snail.pop(i)
            snail.insert(i, val.value)
            return True
        elif isinstance(val, list):
            if unconvert(val):
                return True
    return False

def split(snail:list):
    for i, val in enumerate(snail):
        if isinstance(val, list):
            if split(val):
                return True
        if isinstance(val, MyNumber) and val.value >= 10:
            snail.pop(i)
            snail.insert(i, Pair(MyNumber(math.floor(val.value/2)), MyNumber(math.ceil(val.value/2))))
            return True
        elif isinstance(val, Pair):
            if val.left.value >= 10:
                old_pair = snail.pop(i)
                new = [Pair(MyNumber(math.floor(old_pair.left.value/2)), MyNumber(math.ceil(old_pair.left.value/2))), MyNumber(old_pair.right.value)]
                snail.insert(i, new)
                return True
            elif val.right.value >= 10:
                old_pair = snail.pop(i)
                new = [MyNumber(old_pair.left.value), Pair(MyNumber(math.floor(old_pair.right.value/2)), MyNumber(math.ceil(old_pair.right.value/2)))]
                snail.insert(i, new)
                return True
    return False

def magnitude(snail: list):
    if isinstance(snail, Pair):
        snail.append(MyNumber(3*snail.pop(0).value+2*snail.pop(0).value))
        return True
    for i, val in enumerate(snail):
        if isinstance(val, Pair):
            snail.pop(i)
            snail.insert(i, MyNumber(3*val.left.value+2*val.right.value))
            return True
        elif isinstance(val, list):
            if magnitude(val):
                return True
    return False

def transform(cur):
    changed = True
    while changed:
        while convert(cur):
            continue
        changed = explode(cur, cur, 1)
        if changed:
            continue
        changed = split(cur)
        if changed:
            pass


def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        try:
            inp= path.read_text()
        except:
            inp = path

        return [eval(''.join([f"MyNumber(value={y})" if y.isdigit() else y for y in x])) for x in inp.split('\n')]
        
    def solve(data):
        cur = data[0]
        while convert(cur):
            continue
        for nbr in data[1:]:
            while convert(nbr):
                continue
            cur = [cur, nbr]
            while convert(cur):
                continue
            transform(cur)

        last = deepcopy(cur)

        while True:
            while convert(cur):
                continue
            if not magnitude(cur):
                break
        if len(cur) == 2:
            return last, cur[0].value*3 + cur[1].value*2
        else:
            assert False
        
        
    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return [eval(''.join([f"MyNumber(value={y})" if y.isdigit() else y for y in x])) for x in path.read_text().split('\n')]
        
    def solve(data):
        res = []
        for d in itertools.product(data, repeat=2):
            a,b = d
            a = deepcopy(a)
            b = deepcopy(b)
            while convert(a):
                continue
            while convert(b):
                continue
            cur = [a, b]
            transform(cur)


            while True:
                while convert(cur):
                    continue
                if not magnitude(cur):
                    break
            if len(cur) == 2:
                res.append(cur[0].value*3 + cur[1].value*2)
            else:
                assert False
        return max(res)
        
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    example2 = pathlib.Path(__file__).resolve().parent / "example2.txt"
    tests = [([[[[[9,8],1],2],3],4], [[[[0,9],2],3],4]),
    ([7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]]),
    ([[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3]),
    ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]),
    ([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],[[3,[2,[8,0]]],[9,[5,[7,0]]]])]

    for test in tests:
        a,b = test
        print("testing ", a, b)
        a = eval(''.join([f"MyNumber(value={y})" if y.isdigit() else y for y in str(a)]))
        while convert(a):
            continue
        explode(a, a, 1)
        while unconvert(a):
            continue
        print("result:", a)
        assert a==b
    tests = [([[1,2],[[3,4],5]], 143),
            ([[[[0,7],4],[[7,8],[6,0]]],[8,1]], 1384),
            ([[[[1,1],[2,2]],[3,3]],[4,4]], 445),
            ([[[[3,0],[5,3]],[4,4]],[5,5]], 791),
            ([[[[5,0],[7,4]],[5,5]],[6,6]], 1137),
            ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488)]
    
    for test in tests:
        a,b = test
        print("testing ", a, b)
        a = eval(''.join([f"MyNumber(value={y})" if y.isdigit() else y for y in str(a)]))
        while True:
            while convert(a):
                continue
            if not magnitude(a):
                break
        if len(a) == 2:
            assert a[0].value*3 + a[1].value*2 == b
        else:
            assert False

    # breakpoint()
    # get_result("[[[[4,3],4],4],[7,[[8,4],9]]]\n[1,1]")
    # breakpoint()
    tests = [("[1,1]\n[2,2]\n[3,3]\n[4,4]", [[[[1,1],[2,2]],[3,3]],[4,4]]),
            ("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]", [[[[3,0],[5,3]],[4,4]],[5,5]]),
            ("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]", [[[[5,0],[7,4]],[5,5]],[6,6]]),
            ("[[[[4,3],4],4],[7,[[8,4],9]]]\n[1,1]", [[[[0,7],4],[[7,8],[6,0]]],[8,1]])]

    for test in tests:
        a,b= test
        print("testing ", a, b)
        a = get_result(a)[0]
        while unconvert(a):
            continue
        print("result:", a)
        assert a == b
    example_res = get_result(example)[0]
    print(example_res)
    print([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]] == example_res)
    example2_res = get_result(example2)[0]
    print(example2_res)
    print([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] == example2_res)
    return {
        "part1": {"example2": get_result(example2)[1], "example": get_result(example)[1], "input": get_result()[1]},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    