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


class Node:
    def __init__(self, board: Board):
        self.board = board
        self.nexts: List[Node] = []
        self.visited = False

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
                for a_q in self.board.inputs:
                    my_q = a_q.copy()
                    new_input.append(my_q)
                new_input[temp_sq[0]][temp_sq[1]] = new_input[next_node_sq[0]][next_node_sq[1]]
                new_input[next_node_sq[0]][next_node_sq[1]] = '#'
                next_node = Node(Board(new_input, next_node_sq))
                self.nexts.append(next_node)


def dls_rec(node: Node, limit, my_path: List[Node]):
    if node.is_goal():
        my_path.append(node)
        return my_path
    if limit <= 0:
        return None
    global developed
    global created
    developed += 1
    node.produce_nexts()
    for a_nn in node.nexts:
        created += 1
        result = dls_rec(a_nn, limit - 1, my_path=my_path)
        if result is not None:
            my_path.insert(0, a_nn)
            return my_path


def ids(start_node: Node):
    for l in range(20):
        front: List[Node] = []
        result = dls_rec(deepcopy(start_node), l, front)
        if result is not None and result is not False:
            result.insert(0, start_node)
            return result
        print(f'No answer was found in {l}')


def print_list(quide, al):
    print(quide)
    for a in al:
        print(a)


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

    my_node = Node(Board(qu, square_pos=sqr))
    frontier = ids(my_node)
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
