from typing import List, Tuple
from copy import deepcopy


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
                next_node = Node(Board(new_input, next_node_sq),self.G+1)
                next_node.parent = self
                self.nexts.append(next_node)

def is_in_explored(a_node:Node,explored:List[Node]):
    for exp in explored:
        if a_node.board.inputs==exp.board.inputs:
            return True
        return False


def is_in_frontier(a_node:Node, frontier:List[Node]):
    for front in frontier:
        if a_node.board.inputs==front.board.inputs and 


def a_star(node : Node):
    frontier : List[Node]=[]
    explored : List[Node]=[]
    frontier.append(node)
    current_node : Node = min(frontier,key=lambda x:x.heuristic + x.G)
    while frontier:
        if current_node.is_goal():
            path : List[Node] = [current_node]
            while current_node.parent:
                path.insert(0,current_node.parent)
                current_node = current_node.parent
            return path
        else:
            frontier.remove(current_node)
            explored.append(current_node)
            current_node.produce_nexts()
            for child in current_node.nexts:
                if not is_in_explored(a_node=child,explored=explored):
                    if not is_in_frontier(a_node=child,frontier=frontier)

