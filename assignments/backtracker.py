#!/usr/bin/python3

import sys

__infile__ = sys.argv[1]
__outfile__ = sys.argv[2]

class Board:
	cliques = [[0,1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15,16,17],[18,19,20,21,22,23,24,25,26],[27,28,29,30,31,32,33,34,35],[36,37,38,39,40,41,42,43,44],[45,46,47,48,49,50,51,52,53],[54,55,56,57,58,59,60,61,62],[63,64,65,66,67,68,69,70,71],[72,73,74,75,76,77,78,79,80],[0,9,18,27,36,45,54,63,72],[1,10,19,28,37,46,55,64,73],[2,11,20,29,38,47,56,65,74],[3,12,21,30,39,48,57,66,75],[4,13,22,31,40,49,58,67,76],[5,14,23,32,41,50,59,68,77],[6,15,24,33,42,51,60,69,78],[7,16,25,34,43,52,61,70,79],[8,17,26,35,44,53,62,71,80],[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],[6,7,8,15,16,17,24,25,26],[27,28,29,36,37,38,45,46,47],[30,31,32,39,40,41,48,49,50],[33,34,35,42,43,44,51,52,53],[54,55,56,63,64,65,72,73,74],[57,58,59,66,67,68,75,76,77],[60,61,62,69,70,71,78,79,80]]
	# clique_sets = [set(clique) for clique in cliques]

	def __init__(self, state):
		self.state = [int(c) for c in state]

	def __str__(self):
		aslist = []
		for i in range(9):
			aslist.append(self.state[9*i:9*(i + 1)])
		return '\n'.join('|'.join(str(cell) for cell in line) for line in aslist)

	def __repr__(self):
		return str(self)
	
	def valid_n(self, cell):
		numbers = range(1,10)
		for clique in Board.cliques:
			if self.state[cell] in clique:
				for cell in clique:
					try:
						numbers.remove(self.state[cell])
		return numbers

def parse_boards(file, status):
	boards = []
	line = file.readline()
	while line:
		buffer = ''
		if status in line:
			for i in range(9):
				buffer += file.readline()
			buffer = buffer.replace(',','')
			buffer = buffer.replace('\n','')
			boards.append(buffer)
		line = file.readline()
	return boards

def main():
	with open(__infile__) as infile:
		boards = parse_boards(infile, 'incomplete')
	