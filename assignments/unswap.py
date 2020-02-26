#!/usr/bin/python3

import sys

__infile__ = sys.argv[1]
__outfile__ = sys.argv[2]

class Board:
    state: list
    cliques = [
        [0,1,2,3,4,5,6,7,8],
        [9,10,11,12,13,14,15,16,17],
        [18,19,20,21,22,23,24,25,26],
        [27,28,29,30,31,32,33,34,35],
        [36,37,38,39,40,41,42,43,44],
        [45,46,47,48,49,50,51,52,53],
        [54,55,56,57,58,59,60,61,62],
        [63,64,65,66,67,68,69,70,71],
        [72,73,74,75,76,77,78,79,80],
        [0,9,18,27,36,45,54,63,72],
        [1,10,19,28,37,46,55,64,73],
        [2,11,20,29,38,47,56,65,74],
        [3,12,21,30,39,48,57,66,75],
        [4,13,22,31,40,49,58,67,76],
        [5,14,23,32,41,50,59,68,77],
        [6,15,24,33,42,51,60,69,78],
        [7,16,25,34,43,52,61,70,79],
        [8,17,26,35,44,53,62,71,80],
        [0,1,2,9,10,11,18,19,20],
        [3,4,5,12,13,14,21,22,23],
        [6,7,8,15,16,17,24,25,26],
        [27,28,29,36,37,38,45,46,47],
        [30,31,32,39,40,41,48,49,50],
        [33,34,35,42,43,44,51,52,53],
        [54,55,56,63,64,65,72,73,74],
        [57,58,59,66,67,68,75,76,77],
        [60,61,62,69,70,71,78,79,80]
    ]
    
    def __init__(self, state): # state is a list of lists
        self.state = []
        for row in state:
            for cell in row:
                self.state.append(cell)
        print('\n'.join('|'.join(str(cell) for cell in row) for row in state))

    def validate(self): # returns list of inconsistent pairs
        fails = set([])
        for clique in Board.cliques:
            for first in range(8):
                for second in range(first + 1, 9):
                    if self.state[clique[first]] == self.state[clique[second]]:
                        fails.add((clique[first], clique[second]))
        return fails

    def single_swap(self):
        fails = set([])
        for clique in Board.cliques:
            for first in range(8):
                for second in range(first + 1, 9):
                    if self.state[clique[first]] == self.state[clique[second]]:
                        return (clique[first], clique[second])

with open(__infile__, 'r') as infile:
    boards = [Board(line.split(',') for line in board.split('\n')[1:]) for board in infile.read().split('\n\n')]
    swaps = [board.single_swap() for board in boards]

with open(outfile, 'w') as outfile:
    outfile.write('\n'.join(','.join(swap) for swap in swaps))