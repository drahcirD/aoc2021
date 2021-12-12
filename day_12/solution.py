#! /usr/bin/env python
import pathlib
from collections import defaultdict, Counter
import fire

def get_result(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        input_ = [x.split('-') for x in path.read_text().split('\n')]
        graph = defaultdict(set)
        for entry in input_:
            first, second = entry
            graph[first].add(second)
            graph[second].add(first)
        return graph

        
    def solve(data):
        def dfs(visited, graph, node, end, path, paths):
            if node == end:
                path.append(end)
                paths.append(path)
                return
            if visited[node] == 0 or node.isupper():
                visited[node] += 1
                path.append(node)
                for neighbour in graph[node]:
                    dfs(visited, graph, neighbour, end, path, paths)
                path.pop()
                visited[node] -=1
        visited = Counter()
        path = []
        paths =  []
        dfs(visited, data, 'start', 'end', path, paths)
        return len(paths)

    
    return solve(parse())

def get_result2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        input_ = [x.split('-') for x in path.read_text().split('\n')]
        graph = defaultdict(set)
        for entry in input_:
            first, second = entry
            if first != 'end' and second != 'start':
                graph[first].add(second)
            if first != 'start' and second != 'end':
                graph[second].add(first)
        return graph

        
    def solve(data):
        def dfs(visited, graph, node, end, path, paths):
            if node == end:
                path.append(end)
                paths.append(path)
                return
            small_caves_twice = [k for k,v in visited.items() if v == 2 and k.islower()]
            if not small_caves_twice or visited[node] == 0 or node.isupper():
                visited[node] += 1
                path.append(node)
                for neighbour in graph[node]:
                    dfs(visited, graph, neighbour, end, path, paths)
                path.pop()
                visited[node] -=1
        visited = Counter()
        path = []
        paths =  []
        dfs(visited, data, 'start', 'end', path, paths)
        return len(paths)
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    example2 = pathlib.Path(__file__).resolve().parent / "slightly_larger_example.txt"
    example3 = pathlib.Path(__file__).resolve().parent / "even_larger_example.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example": get_result2(example), "example2": get_result2(example2),"example3": get_result2(example3), "input": get_result2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    