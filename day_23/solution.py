#! /usr/bin/env python
import pathlib
import fire
import sys
from frozendict import frozendict
from queue import PriorityQueue

COST = {"A": 1, "B": 10, "C": 100, "D": 1000}
AMPHIPODS = {k for k in COST}
AMPH2ROOMCOL = {"A": 3, "B": 5, "C": 7, "D": 9}
GOAL = frozendict(
    {
        (2, 9): "D",
        (3, 3): "A",
        (3, 7): "C",
        (2, 3): "A",
        (2, 5): "B",
        (3, 5): "B",
        (2, 7): "C",
        (3, 9): "D",
    }
)

from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def manhattan(first, second):
    return sum(abs(x - y) for x, y in zip(first, second))


def get_result(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return {
            (i, j): c
            for i, row in enumerate(path.read_text().split("\n"))
            for j, c in enumerate(row)
        }

    def solve(data):
        def print_map(cur, walls, rooms, hallway):
            for i in range(-2, 7):
                for j in range(-2, 16):
                    try:
                        print(cur[(i, j)], end="")
                    except KeyError:
                        if (i, j) in walls:
                            print("#", end="")
                        elif (i, j) in rooms or (i, j) in hallway:
                            print(".", end="")
                        else:
                            print(" ", end="")

                print()

        def is_room_available(cur, room, amph_pos, amph_val):
            if room in cur:
                return False

            if room[1] != AMPH2ROOMCOL[amph_val] and amph_pos not in {
                (2, room[1]),
                (3, room[1]),
            }:
                return False

            if room[0] == 2:
                other = (3, room[1])
            elif room[0] == 3:
                other = (2, room[1])
            else:
                assert False

            if other not in cur:
                if room[0] == 2:
                    return False
                else:
                    return True
            else:
                return cur[other] == amph_val

            assert False

        def dijkstra_lengths(start_vertex):
            distances = {}
            distances[start_vertex] = 0

            visited = set()
            pq = PriorityQueue()
            pq.put((0, start_vertex))

            while not pq.empty():
                (cur_dist, cur) = pq.get()
                visited.add(cur)
                r, c = cur
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for neighbor in neighbors:
                    if data[neighbor] == "#":
                        continue

                    neighbor_dist = 1
                    if neighbor not in visited:
                        old_path_cost = distances.get(neighbor, sys.maxsize)
                        new_path_cost = cur_dist + neighbor_dist
                        if new_path_cost < old_path_cost:
                            pq.put((new_path_cost, neighbor))
                            distances[neighbor] = new_path_cost
            return distances

        def reachable_positions(visited, cur, node, walls):
            if node not in visited:
                visited.add(node)
                r, c = node
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for neighbor in neighbors:
                    if neighbor in walls or neighbor in cur:
                        continue
                    reachable_positions(visited, cur, neighbor, walls)

        def dijkstra(start_vertex, hallway, rooms, bad_hallway, dists, walls):
            distances = {}
            distances[start_vertex] = 0

            visited = set()
            pq = PriorityQueue()
            pq.put(PrioritizedItem(0, start_vertex))

            while not pq.empty():
                # breakpoint()
                item = pq.get()
                (cur_dist, cur) = item.priority, item.item
                visited.add(cur)
                print(pq.qsize())
                neighbors = {}
                # print_map(cur, walls, rooms, hallway)
                for amph_pos, amph_val in cur.items():
                    if amph_pos in rooms and amph_pos == (3, AMPH2ROOMCOL[amph_val]):
                        # breakpoint()
                        continue

                    possible_rooms = [
                        room
                        for room in rooms
                        if is_room_available(cur, room, amph_pos, amph_val)
                    ]
                    # print("="*50)
                    # print("cur pos:")
                    # print_map(cur, walls, rooms, hallway)
                    # print(f"Reachable from {amph_pos}")
                    reachable = set()
                    reachable_positions(reachable, cur, amph_pos, walls)
                    for room in possible_rooms:
                        if not room in reachable:
                            # print(f"room {room} is not reachable")
                            continue
                        # print(f"room {room} is reachable")
                        new = dict(cur)
                        new.pop(amph_pos)
                        new[room] = amph_val
                        new = frozendict(new)
                        assert len(new) == 8
                        neighbors[new] = dists[amph_pos][room] * COST[amph_val]

                    possible_hallway = []
                    if amph_pos not in hallway:
                        possible_hallway = [
                            x for x in hallway if x not in cur and x not in bad_hallway
                        ]
                        for pos in possible_hallway:
                            if not pos in reachable:
                                # print(f"pos {pos} is not reachable")
                                continue
                            # print(f"pos {pos} is reachable")
                            new = dict(cur)
                            new.pop(amph_pos)
                            new[pos] = amph_val
                            new = frozendict(new)
                            assert len(new) == 8
                            neighbors[new] = dists[amph_pos][pos] * COST[amph_val]
                    # breakpoint()
                    # print("="*50)
                for neighbor, neighbor_dist in neighbors.items():
                    if neighbor not in visited:
                        old_path_cost = distances.get(neighbor, sys.maxsize)
                        new_path_cost = cur_dist + neighbor_dist
                        if new_path_cost < old_path_cost:
                            pq.put(PrioritizedItem(new_path_cost, neighbor))
                            distances[neighbor] = new_path_cost
            return distances

        amph = frozendict({pos: val for pos, val in data.items() if val in AMPHIPODS})
        rooms = {pos for pos, val in data.items() if val in AMPHIPODS}
        hallway = {pos for pos, val in data.items() if val == "."}
        walls = {pos for pos, val in data.items() if val == "#"}
        bad_hallway = {
            pos for pos in hallway if any([manhattan(pos, room) == 1 for room in rooms])
        }
        all_positions = rooms | hallway
        dists = {}
        for pos in all_positions:
            dists[pos] = dijkstra_lengths(pos)

        res = dijkstra(amph, hallway, rooms, bad_hallway, dists, walls)
        correct = []
        for cur, entry in res.items():
            cost = entry
            for amph_pos, amph_val in cur.items():
                if not (amph_pos in rooms and amph_pos[1] == AMPH2ROOMCOL[amph_val]):
                    break
            else:
                correct.append(cost)
        return min(correct)

    return solve(parse())


def get_result2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return {
            (i, j): c
            for i, row in enumerate(path.read_text().split("\n"))
            for j, c in enumerate(row)
        }

    def solve(data):
        def print_map(cur, walls, rooms, hallway):
            for i in range(-2, 7):
                for j in range(-2, 16):
                    try:
                        print(cur[(i, j)], end="")
                    except KeyError:
                        if (i, j) in walls:
                            print("#", end="")
                        elif (i, j) in rooms or (i, j) in hallway:
                            print(".", end="")
                        else:
                            print(" ", end="")

                print()

        def is_room_available(cur, room, amph_pos, amph_val):
            if room in cur:
                return False

            if room[1] != AMPH2ROOMCOL[amph_val] and amph_pos not in {
                (x, room[1]) for x in range(room[0]+1, 5 + 1)
            }:
                return False
            
            if room[1] != AMPH2ROOMCOL[amph_val] and amph_pos in {
                (x, room[1]) for x in range(room[0]+1, 5 + 1)
            }:
                return True

            assert room[1] == AMPH2ROOMCOL[amph_val]
            rooms_level = sorted([(x, room[1]) for x in range(2, 5 + 1)])
            room_index = rooms_level.index(room)         
            return all((room in cur and cur[room] == amph_val for room in rooms_level[room_index+1: 6]))

            

        def dijkstra_lengths(start_vertex):
            distances = {}
            distances[start_vertex] = 0

            visited = set()
            pq = PriorityQueue()
            pq.put((0, start_vertex))

            while not pq.empty():
                (cur_dist, cur) = pq.get()
                visited.add(cur)
                r, c = cur
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for neighbor in neighbors:
                    if data[neighbor] == "#":
                        continue

                    neighbor_dist = 1
                    if neighbor not in visited:
                        old_path_cost = distances.get(neighbor, sys.maxsize)
                        new_path_cost = cur_dist + neighbor_dist
                        if new_path_cost < old_path_cost:
                            pq.put((new_path_cost, neighbor))
                            distances[neighbor] = new_path_cost
            return distances

        def reachable_positions(visited, cur, node, walls):
            if node not in visited:
                visited.add(node)
                r, c = node
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for neighbor in neighbors:
                    if neighbor in walls or neighbor in cur:
                        continue
                    reachable_positions(visited, cur, neighbor, walls)

        def dijkstra(start_vertex, hallway, rooms, bad_hallway, dists, walls):
            distances = {}
            distances[start_vertex] = 0

            visited = set()
            pq = PriorityQueue()
            pq.put(PrioritizedItem(0, start_vertex))

            while not pq.empty():
                # breakpoint()
                item = pq.get()
                (cur_dist, cur) = item.priority, item.item
                visited.add(cur)
                print(pq.qsize())
                neighbors = {}
                # print_map(cur, walls, rooms, hallway)
                for amph_pos, amph_val in cur.items():
                    if amph_pos in {(x, AMPH2ROOMCOL[amph_val]) for x in range(2,6)}:
                        if all(
                            [
                                room_pos in cur and cur[room_pos] == amph_val
                                for room_pos in range(amph_pos[0] + 1, 5 + 1)
                            ]
                        ):
                            continue

                    possible_rooms = [
                        room
                        for room in rooms
                        if is_room_available(cur, room, amph_pos, amph_val)
                    ]
                    reachable = set()
                    reachable_positions(reachable, cur, amph_pos, walls)
                    for room in possible_rooms:
                        if not room in reachable:
                            continue
                        new = dict(cur)
                        new.pop(amph_pos)
                        new[room] = amph_val
                        new = frozendict(new)
                        assert len(new) == 16
                        neighbors[new] = dists[amph_pos][room] * COST[amph_val]

                    possible_hallway = []
                    if amph_pos not in hallway:
                        possible_hallway = [
                            x for x in hallway if x not in cur and x not in bad_hallway
                        ]
                        for pos in possible_hallway:
                            if not pos in reachable:
                                continue
                            new = dict(cur)
                            new.pop(amph_pos)
                            new[pos] = amph_val
                            new = frozendict(new)
                            assert len(new) == 16
                            neighbors[new] = dists[amph_pos][pos] * COST[amph_val]

                for neighbor, neighbor_dist in neighbors.items():
                    if neighbor not in visited:
                        old_path_cost = distances.get(neighbor, sys.maxsize)
                        new_path_cost = cur_dist + neighbor_dist
                        if new_path_cost < old_path_cost:
                            pq.put(PrioritizedItem(new_path_cost, neighbor))
                            distances[neighbor] = new_path_cost
            return distances

        amph = frozendict({pos: val for pos, val in data.items() if val in AMPHIPODS})
        rooms = {pos for pos, val in data.items() if val in AMPHIPODS}
        hallway = {pos for pos, val in data.items() if val == "."}
        walls = {pos for pos, val in data.items() if val == "#"}
        bad_hallway = {
            pos for pos in hallway if any([manhattan(pos, room) == 1 for room in rooms])
        }
        all_positions = rooms | hallway
        dists = {}
        for pos in all_positions:
            dists[pos] = dijkstra_lengths(pos)

        res = dijkstra(amph, hallway, rooms, bad_hallway, dists, walls)
        correct = []
        for cur, entry in res.items():
            cost = entry
            for amph_pos, amph_val in cur.items():
                if not (amph_pos in rooms and amph_pos[1] == AMPH2ROOMCOL[amph_val]):
                    break
            else:
                correct.append(cost)
        return min(correct)

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    example2 = pathlib.Path(__file__).resolve().parent / "example2.txt"
    input2 = pathlib.Path(__file__).resolve().parent / "input2.txt"
    return {
        "part1": {"example": get_result(example), "input": get_result()},
        "part2": {"example2": get_result2(example2), "input2": get_result2(input2)},
    }


if __name__ == "__main__":
    fire.Fire()
