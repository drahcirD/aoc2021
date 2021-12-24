#! /usr/bin/env python
import pathlib
import fire
import functools
import numba

@functools.cache
@numba.njit
def get_z(cur, reg_z, i15, i4, i5):
    z1 = int(reg_z // i4)
    x0 = (reg_z % 26) + i5
    x1 = int(int(x0 == cur) == 0)
    y0 = 25*x1 + 1
    z2 = z1*y0
    y1 = (cur + i15)*x1
    z3 = z2 + y1
    return z3

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        splits = path.read_text().split('inp w\n')
        data = [split.split('\n') for split in splits[1:]]
        return data

    def solve(data):
        prev_states = {0: []}
        for digit in range(14):
            instr = ['inp w'] + data[digit][:-1]
            states = {}
            i15, i4, i5 = int(instr[15].split(' ')[2]), int(instr[4].split(' ')[2]), int(instr[5].split(' ')[2])
            for state in prev_states:
                for i in reversed(range(1,10)):
                    new_state = get_z(i, state, i15, i4, i5)
                    try:
                        old = states[new_state].pop()
                        states[new_state].append(max(old, i))
                    except KeyError:
                        states[new_state] = prev_states[state].copy()
                        states[new_state].append(i)
            prev_states = states
            print(digit, len(states))
        return ''.join((str(n) for n in states[0]))

    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        splits = path.read_text().split('inp w\n')
        data = [split.split('\n') for split in splits[1:]]
        return data

    def solve(data):
        prev_states = {0: []}
        for digit in range(14):
            instr = ['inp w'] + data[digit][:-1]
            states = {}
            i15, i4, i5 = int(instr[15].split(' ')[2]), int(instr[4].split(' ')[2]), int(instr[5].split(' ')[2])
            for state in prev_states:
                for i in range(1,10):
                    new_state = get_z(i, state, i15, i4, i5)
                    try:
                        old = states[new_state].pop()
                        states[new_state].append(min(old, i))
                    except KeyError:
                        states[new_state] = prev_states[state].copy()
                        states[new_state].append(i)
            prev_states = states
            print(digit, len(states))
        return ''.join((str(n) for n in states[0]))

    return solve(parse())

def main():
    return {
        "part1": {"input": get_result()},
        "part2": {"input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
