import operator
import re
from typing import List, Tuple
from copy import deepcopy
from itertools import permutations

counter = 0
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
    return list(permutations(my_list))


def give_places_in_dict(a_input):
    permutation = {}
    for i in range(row):
        for j in range(col):
            permutation[a_input[i][j]] = (i, j)
    return permutation


def displacements_in_height(arr):
    def merge_sort(arr):
        global counter
        n = len(arr)
        if n > 1:
            middle = n // 2
            arr1 = arr[:middle]
            arr2 = arr[middle:]
            merge_sort(arr1)
            merge_sort(arr2)
            i = j = k = 0
            while i < len(arr1) and j < len(arr2):
                if arr1[i] > arr2[j]:
                    arr[k] = arr1[i]
                    i += 1
                    k += 1
                else:
                    arr[k] = arr2[j]
                    j += 1
                    k += 1
                    counter += (len(arr1) - i)
            while j < len(arr2):
                arr[k] = arr2[j]
                j += 1
                k += 1
            while i < len(arr1):
                arr[k] = arr1[i]
                i += 1
                k += 1

    merge_sort(arr)
    return counter


class Board:
    def __init__(self, inputs: list, square_pos):
        self.row = len(inputs)
        self.col = len(inputs[0])
        self.inputs = inputs
        self.square_pos = square_pos

    def count_displacement(self):
        result = 0
        for a_list in self.inputs:
            my_dict = {}
            my_arr = []
            for student in a_list:
                if student == '#':
                    continue
                my_arr.append(student[0])
                if student[1] in my_dict.keys():
                    my_dict[student[1]] += 1
                else:
                    my_dict[student[1]] = 1
            max_v = 0
            sum_v = 0
            max_k = None
            for k, v in my_dict.items():
                sum_v += v
                if v > max_v:
                    max_v = v
                    max_k = k
            last_h = 0
            last_h_c = -1
            for s in a_list:
                if s == '#':
                    continue
                if s[1] == max_k:
                    if s[0] > last_h:
                        last_h_c += 1
                    last_h = s[0]
            global counter
            counter = 0
            a = displacements_in_height(my_arr)
            print(a)
            print(my_arr)
            result += sum_v - max_v + last_h_c + a
            # print("kir : ", a_list)
            # print("innnnnnnn : ", result, sum_v, max_v, last_h_c)
        # print_list("asl : ", self.inputs)
        # print(f'{result}')
        return result

    def count_distance_from_goal(self):
        all_results = []
        my_ords = give_places_in_dict(self.inputs)
        for a_goal in all_goals:
            res = 0
            target_ord = give_places_in_dict(a_goal)
            for k in my_ords.keys():
                res += (abs(my_ords[k][1] - target_ord[k][1]) + abs(my_ords[k][0] - target_ord[k][0]))
            all_results.append(res)
        return min(all_results)

    def count_it_better(self):
        permutation = {}
        for i in range(row):
            for j in range(col):
                if self.inputs[i][j] == "#":
                    continue
                if not self.inputs[i][j][1] in permutation.keys():
                    permutation[self.inputs[i][j][1]] = []
                permutation[self.inputs[i][j][1]].append((i, j))
        dist = 0
        # print(permutation)
        for k, v in permutation.items():
            my_dict = {}
            for v1 in v:
                if not v1[0] in my_dict.keys():
                    my_dict[v1[0]] = 0
                my_dict[v1[0]] += 1
            max_rep = max(my_dict.items(), key=operator.itemgetter(1))[0]
            # print_list(str(max_rep),self.inputs)
            empty = []
            for cc in range(col):
                empty.append(cc)
            for v1 in v:
                for c in range(self.col):
                    if v1[0] == max_rep and v1[1] == c and c in empty:
                        empty.remove(c)
            min_dis = 100
            min_dict = {}
            for v1 in v:
                print(v1)
                min_dict[v1] = 0
                if v1[0] != max_rep:
                    for e in empty:
                        print(e)
                        temp = abs(v1[1] - e)
                        if temp < min_dis:
                            min_dis = temp
                        min_dict[v1] = min_dis
            print(min_dict)

            for v1 in v:
                dist += (abs(v1[0] - max_rep) + min_dict[v1])

        print(dist)
        return dist


def print_list(quide, al):
    print(quide)
    for a in al:
        print(a)


class Node:

    def __init__(self, board: Board, G):
        self.board = board
        self.nexts: List[Node] = []
        self.visited = False
        self.heuristic = board.count_distance_from_goal()
        self.G = G
        self.parent = None

    def is_goal(self):
        for q in self.board.inputs:
            nq = deepcopy(q)
            if '#' in nq:
                if nq[0] != '#':
                    return False
                else:
                    nq.pop(0)
            last_student = deepcopy(nq[0])
            for student in nq:
                # print(student)
                if student[1] != last_student[1] or student[0] > last_student[0]:
                    return False
                last_student = deepcopy(student)
        return True

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
                next_node = Node(Board(new_input, next_node_sq), self.G + 1)
                next_node.parent = self
                self.nexts.append(next_node)


def is_in_explored(a_node: Node, explored: List[Node]):
    for exp in explored:
        if a_node.board.inputs == exp.board.inputs:
            return True
    return False


def a_star(node: Node):
    frontier: List[Node] = []
    explored: List[Node] = []
    frontier.append(node)
    current_node: Node = min(frontier, key=lambda x: x.heuristic + x.G)
    while frontier:
        global developed
        developed += 1
        if current_node.board.inputs in all_goals:
            path: List[Node] = [current_node]
            while current_node.parent:
                path.insert(0, current_node.parent)
                current_node = current_node.parent
            return path

        frontier.remove(current_node)
        explored.append(current_node)
        current_node.produce_nexts()
        for child in current_node.nexts:
            global created
            created += 1
            flag = False
            if not is_in_explored(child,explored):
                for front in frontier:
                    if child.board.inputs == front.board.inputs:
                        if child.heuristic + child.G >= front.heuristic+front.G:
                            flag = True
                        # else:
                            # temp = front
                        break
                if not flag:
                    frontier.append(child)
                # if temp:
                #     frontier.remove(temp)
        current_node = min(frontier, key=lambda x: x.heuristic + x.G)


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
                str_c=0
                for c in range(len(q1[j])):
                    if q1[j][c].isalpha():
                        str_c = c
                        break
                nq1.append((int(q1[j][:str_c]), q1[j][str_c:]))

        qu.append(nq1)

    all_goals = make_goals(qu)
    # Board(qu, sqr).count_distance_from_goal()
    for ii in range(len(all_goals)):
        all_goals[ii] = list(all_goals[ii])
    my_node = Node(Board(qu, square_pos=sqr), 0)
    frontier1 = a_star(my_node)
    print(len(frontier1) - 1)
    last_sq = frontier1[0].board.square_pos
    dirs = []
    for i in range(len(frontier1)):
        direction = (frontier1[i].board.square_pos[0] - last_sq[0], frontier1[i].board.square_pos[1] - last_sq[1])
        if direction == (0, 1):
            dirs.append('RIGHT')
        elif direction == (0, -1):
            dirs.append('LEFT')
        elif direction == (1, 0):
            dirs.append('DOWN')
        elif direction == (-1, 0):
            dirs.append("UP")
        last_sq = (frontier1[i].board.square_pos[0], frontier1[i].board.square_pos[1])
    for i in dirs:
        print(i)
    print("created nodes : ", created)
    print("developed nodes : ", developed)
