import operator
import re
from typing import List, Tuple
from copy import deepcopy
from itertools import permutations

created = 0
developed = 0


def make_goals(my_input: List[List[Tuple[int, str]]]):
    my_dict = {}
    for all_lists in my_input:
        for student in all_lists:
            if student == '#':
                continue
            if student[1] not in my_dict.keys():
                my_dict[student[1]] = []
            my_dict[student[1]].append(student)
    my_list = []
    for c in my_dict.keys():
        my_dict[c].sort(reverse=True)
        if len(my_dict[c]) != col:
            my_dict[c].insert(0, '#')
        my_list.append(my_dict[c])
    my_list = list(permutations(my_list))
    for a in range(len(my_list)):
        my_list[a] = list(my_list[a])
    return my_list


def give_places_in_dict(a_input):
    permutation = {}
    for i in range(row):
        for j in range(col):
            permutation[a_input[i][j]] = (i, j)
    return permutation


class Board:
    def __init__(self, inputs: list, square_pos):
        self.row = len(inputs)
        self.col = len(inputs[0])
        self.inputs = inputs
        self.square_pos = square_pos


def print_list(quide, al):
    print(quide)
    for a in al:
        print(a)


class Node:

    def __init__(self, board: Board):
        self.board = board
        self.nexts: List[Node] = []
        self.parent = None

    def produce_nexts(self):
        temp_sq = (self.board.square_pos[0], self.board.square_pos[1])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for adir in directions:
            next_node_sq = (temp_sq[0] + adir[0], temp_sq[1] + adir[1])
            if self.board.row > next_node_sq[0] >= 0 and self.board.col > next_node_sq[1] >= 0:
                new_input = []
                # print_list("original board : ",self.board.inputs)
                # new_input = list(self.board.inputs)
                for a_q in self.board.inputs:
                    my_q = a_q.copy()
                    new_input.append(my_q)
                # print_list("new input : ",new_input)
                new_input[temp_sq[0]][temp_sq[1]] = new_input[next_node_sq[0]][next_node_sq[1]]
                new_input[next_node_sq[0]][next_node_sq[1]] = '#'
                next_node = Node(Board(new_input, next_node_sq))
                next_node.parent = self
                self.nexts.append(next_node)


def is_in_explored(a_node: Node, explored: List[Node]):
    for exp in explored:
        if a_node.board.inputs == exp.board.inputs:
            return exp
    return False


def bidirectional(start_node: Node):
    global created
    global developed
    s_frontier: List[Node] = [start_node]
    g_frontier: List[Node] = []
    for g in all_goals:
        sqr_g = ()
        for r in range(row):
            if g[r][0] == '#':
                sqr_g = (r, 0)
                break
        g_frontier.append(Node(Board(g, sqr_g)))
    explored: List[Node] = []
    while s_frontier and g_frontier:
        current_node = s_frontier.pop(0)
        developed += 1
        same_node = is_in_explored(current_node, g_frontier)
        if same_node:
            path: List[Node] = [current_node]
            while current_node.parent:
                path.insert(0, current_node.parent)
                current_node = current_node.parent
                path.append(same_node)
                while same_node.parent:
                    path.append(same_node.parent)
                    same_node = same_node.parent
            return path

        current_node.produce_nexts()
        explored.append(current_node)
        for child in current_node.nexts:
            if not is_in_explored(child, explored):
                created += 1
                s_frontier.append(child)
        current_node = g_frontier.pop(0)
        developed += 1
        same_node = is_in_explored(current_node, s_frontier)
        if same_node:
            path: List[Node] = [current_node]
            while current_node.parent:
                path.append(current_node.parent)
                current_node = current_node.parent
            while same_node.parent:
                path.insert(0, same_node.parent)
                same_node = same_node.parent
            return path

        current_node.produce_nexts()
        explored.append(current_node)
        for child in current_node.nexts:
            if not is_in_explored(child, explored):
                created += 1
                g_frontier.append(child)


if __name__ == '__main__':
    row, col = map(int, input().split())
    qu = []
    sqr = ()
    for i in range(row):
        q1 = list(input().split())
        nq1 = []
        for j in range(col):
            if q1[j] == '#':
                sqr = (i, j)
                nq1.append(q1[j])
            else:
                str_c = 0
                for c in range(len(q1[j])):
                    if q1[j][c].isalpha():
                        str_c = c
                        break
                nq1.append((int(q1[j][:str_c]), q1[j][str_c:]))

        qu.append(nq1)

    all_goals = make_goals(qu)

    my_node = Node(Board(qu, square_pos=sqr))
    frontier = bidirectional(my_node)
    last_sq = frontier[0].board.square_pos
    dirs = []
    for i in range(len(frontier)):
        direction = (frontier[i].board.square_pos[0] - last_sq[0], frontier[i].board.square_pos[1] - last_sq[1])
        if direction == (0, 1):
            dirs.append('RIGHT')
        elif direction == (0, -1):
            dirs.append('LEFT')
        elif direction == (1, 0):
            dirs.append('DOWN')
        elif direction == (-1, 0):
            dirs.append("UP")
        last_sq = (frontier[i].board.square_pos[0], frontier[i].board.square_pos[1])
    print(len(dirs))
    for i in dirs:
        print(i)
    print("created nodes : ", created)
    print("developed nodes : ", developed)
