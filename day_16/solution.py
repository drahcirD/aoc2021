#! /usr/bin/env python
import pathlib
import fire

HEX2BIT = {"0": "0000",
"1": "0001",
"2": "0010",
"3": "0011",
"4": "0100",
"5": "0101",
"6": "0110",
"7": "0111",
"8": "1000",
"9": "1001",
"A": "1010",
"B": "1011",
"C": "1100",
"D": "1101",
"E": "1110",
"F": "1111"}

BIT2HEX= {v:k for k,v in HEX2BIT.items()}

def _read_literal(data, cur, is_sub):
    pre =6
    start = cur
    values = []
    while data[cur] == '1':
        values.append(data[cur+1:cur+1+4])
        cur+=5
    assert data[cur] == '0'
    values.append(data[cur+1:cur+1+4])
    cur += 5
    if not is_sub:
        while (cur-start+pre) % 4 > 0:
            assert data[cur] == "0"
            cur+=1
    literal = int(f"0b{''.join(values)}",2)
    return cur,literal

def _read(data, cur, versions, is_sub):
    version = int(BIT2HEX[f"0{data[cur:cur+3]}"])
    versions.append(version)
    pid = int(BIT2HEX[f"0{data[cur+3:cur+6]}"])
    if pid == 4:
        cur, literal =_read_literal(data, cur+6, is_sub)
    else:
        cur+=6
        length_id = data[cur]
        if length_id == '0':
            length = int(f"0b{data[cur+1:cur+1+15]}",2)
            cur+=16
            stop = cur + length
            while cur < stop:
                cur, res = _read(data, cur, versions, True)
            return cur, res
        elif length_id =='1':
            n_subpp = int(f"0b{data[cur+1:cur+1+11]}",2)
            cur+=12
            for i in range(n_subpp):
                cur, res = _read(data, cur, versions, True)
            return cur, res
        else:
            assert False
    return cur, None

def _read2(data, cur, versions, is_sub):
    def _operate(pid, old, new):
        match pid:
            case 0:
                old += new
            case 1:
                old *= new
            case 2:
                old = min(old, new)
            case 3:
                old = max(old, new)
            case 5:
                old = new if not old else int(old > new)
            case 6:
                old = new if not old else int(old < new)
            case 7:
                old = new if not old else int(old == new)
        return old

    version = int(BIT2HEX[f"0{data[cur:cur+3]}"])
    versions.append(version)
    pid = int(BIT2HEX[f"0{data[cur+3:cur+6]}"])
    if pid == 4:
        cur, literal =_read_literal(data, cur+6, is_sub)
        return cur, literal
    else:
        cur+=6
        length_id = data[cur]
        match pid:
            case 0:
                res = 0
            case 1:
                res = 1
            case 2:
                res = float('inf')
            case 3:
                res = float('-inf')
            case 5:
                res = None
            case 6:
                res = None
            case 7:
                res = None

        if length_id == '0':
            length = int(f"0b{data[cur+1:cur+1+15]}",2)
            cur+=16
            stop = cur + length
        
            while cur < stop:
                cur, sub_res = _read2(data, cur, versions, True)
                res = _operate(pid, res, sub_res)
            return cur, res
        elif length_id =='1':
            n_subpp = int(f"0b{data[cur+1:cur+1+11]}",2)
            cur+=12
            for _ in range(n_subpp):
                cur, sub_res = _read2(data, cur, versions, True)
                res = _operate(pid, res, sub_res)
            return cur, res
        else:
            assert False

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return ''.join([HEX2BIT[x] for x in path.read_text()])
        
    def solve(data):
        cur = 0
        versions = []
        cur, res = _read(data, cur, versions, False)
        return sum(versions)
    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return ''.join([HEX2BIT[x] for x in path.read_text()])
        
    def solve(data):
        cur = 0
        versions = []
        cur, res = _read2(data, cur, versions, False)
        return res

    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    