from typing import List, Tuple
from copy import deepcopy

created = 0
developed = 0

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
            for student in a_list:
                if student == '#':
                    continue
                if student[1] in my_dict.keys():
                    my_dict[student[1]] += 1
                else:
                    my_dict[student[1]] = 1
            max_v = 0
            sum_v = 0
            for k, v in my_dict.items():
                sum_v += v
                if v > max_v:
                    max_v = v
            result += sum_v - max_v
        return result


class Node:

    def __init__(self, board: Board, G):
        self.board = board
        self.nexts: List[Node] = []
        self.visited = False
        self.heuristic = board.count_displacement()
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
        developed+=1
        if current_node.is_goal():
            path: List[Node] = [current_node]
            while current_node.parent:
                path.insert(0, current_node.parent)
                current_node = current_node.parent
            return path
        else:
            frontier.remove(current_node)
            explored.append(current_node)
            current_node.produce_nexts()
            for child in current_node.nexts:
                global created
                created+=1
                flag = False
                if not is_in_explored(a_node=child, explored=explored):
                    for front in frontier:
                        if child.board.inputs != front.board.inputs or child.heuristic + child.G < front.heuristic + front.G:
                            flag = True
                            break
                    if flag:
                        frontier.append(child)


if __name__ == '__main__':
    row, col = map(int, input().split())
    qu = []
    sqr = ()
    for i in range(row):
        q1 = list(input().split())
        nq1 = []
        for j in range(col):
            if q1[j] != '#':
                nq1.append((int(q1[j][:3]), q1[j][3:]))
            else:
                sqr = (i, j)
                nq1.append(q1[j])
        qu.append(nq1)

    my_node = Node(Board(qu, square_pos=sqr), 0)
    frontier = a_star(my_node)
    print(len(frontier) - 2)
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
    for i in dirs:
        print(i)
    print("created nodes : ", created)
    print("developed nodes : ", developed)
