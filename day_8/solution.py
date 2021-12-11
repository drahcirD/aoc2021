#! /usr/bin/env python
from os import remove
import pathlib
import fire
from collections import Counter, defaultdict
import itertools

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

_WIRES= {0: ["a","b", "c", 'e', 'f', 'g'], 1: ['c', 'f'], 2: ['a', 'c', 'd', 'e', 'g'], 3: ['a', 'c', 'd', 'f', 'g'], 4: ['b', 'c', 'd', 'f'],
 5: ['a', 'b', 'd', 'f', 'g'], 6: ['a', 'b', 'd', 'e', 'f', 'g'], 7: ['a', 'c', 'f'], 8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'], 9: ['a', 'b', 'c', 'd', 'f', 'g']}
_SUMS = {len(v): k for k,v in _WIRES.items()}

def get_result():
    def parse():
        data = [x for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().split('\n')]
        res = []
        for line in data:
            d = line.split(' ')
            pipe = d.index('|')
            res.append([d[:pipe], d[pipe+1:]])
        return res

    def solve(data):
        cnt = Counter()
        for d in data:
            output_ = d[1]
            for o in output_:
                cnt[_SUMS[len(o)]] += 1
        return cnt[1] + cnt[4] + cnt[7] + cnt[8]
    
    return solve(parse())

def get_result2():
    def parse():
        data = [x for x in (pathlib.Path(__file__).resolve().parent / "input.txt").read_text().split('\n')]
        res = []
        for line in data:
            d = line.split(' ')
            pipe = d.index('|')
            res.append([d[:pipe], d[pipe+1:]])
        return res

    def solve(data):
        res = 0
        for d in data:
            input_ = d[0]
            output_ = d[1]
            nbr_mapping = {}
            # Find with unique length
            for o in input_:
                candidates = [k for k,v in _WIRES.items() if len(o) == len(v)]
                s_o = set(o)
                if len(candidates) == 1:
                    candidate = candidates[0]
                    nbr_mapping[candidate] = tuple(sorted(o))

            # Find rest by using similarities
            for o in input_:
                s_o = set(o)
                if len(s_o) == 6:
                    if len(s_o & set(nbr_mapping[4])) == 4:
                        nbr_mapping[9] = tuple(sorted(o))
                    elif len(s_o & set(nbr_mapping[7])) == 3:
                        nbr_mapping[0] = tuple(sorted(o))
                    else:
                        nbr_mapping[6] = tuple(sorted(o))
                elif len(s_o) == 5:
                    if len(s_o & set(nbr_mapping[7])) == 3:
                        nbr_mapping[3] = tuple(sorted(o))
                    elif len(s_o & set(nbr_mapping[4])) == 3:
                        nbr_mapping[5] = tuple(sorted(o))
                    else:
                        nbr_mapping[2] = tuple(sorted(o))
            inv_mapping = {v:k for k,v in nbr_mapping.items()}
            res += int(''.join([str(inv_mapping[tuple(sorted(o))]) for o in output_]))
        return res
    return solve(parse())

if __name__ == '__main__':
  fire.Fire()
    