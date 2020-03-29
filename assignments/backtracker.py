#!/usr/bin/python3

import sys
import time
import copy

class Stack:

	def __init__(self, start):
		self.storage = []
		self.filled = 0
		for item in start:
			self.push(item)

	def __str__(self):
		tostr = ''
		for i in range(self.filled):
			item  = self.storage[i]
			tabbed = str(i) + ' ' * ( 4 - len(str(i)) ) + str(item).replace('\n','\n    ')
			tostr = tabbed + '\n' + tostr
		return tostr

	def __repr__(self):
		return str(self)

	def push(self, item):
		if len(self.storage) <= self.filled:
			self.storage.append(item)
		else:
			self.storage[self.filled] = item
		self.filled += 1

	def pop(self):
		self.filled -= 1
		temp = self.storage[self.filled]
		self.storage[self.filled] = None
		return temp

class Board:
	cliques = [[0,1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15,16,17],[18,19,20,21,22,23,24,25,26],[27,28,29,30,31,32,33,34,35],[36,37,38,39,40,41,42,43,44],[45,46,47,48,49,50,51,52,53],[54,55,56,57,58,59,60,61,62],[63,64,65,66,67,68,69,70,71],[72,73,74,75,76,77,78,79,80],[0,9,18,27,36,45,54,63,72],[1,10,19,28,37,46,55,64,73],[2,11,20,29,38,47,56,65,74],[3,12,21,30,39,48,57,66,75],[4,13,22,31,40,49,58,67,76],[5,14,23,32,41,50,59,68,77],[6,15,24,33,42,51,60,69,78],[7,16,25,34,43,52,61,70,79],[8,17,26,35,44,53,62,71,80],[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],[6,7,8,15,16,17,24,25,26],[27,28,29,36,37,38,45,46,47],[30,31,32,39,40,41,48,49,50],[33,34,35,42,43,44,51,52,53],[54,55,56,63,64,65,72,73,74],[57,58,59,66,67,68,75,76,77],[60,61,62,69,70,71,78,79,80]]

	def __init__(self, state):
		try_int = lambda c: int(c) if c.isdigit() else 0
		self.state = [try_int(c) for c in state]
		self.first_empty = -1
		self.nexts = []

	def __str__(self):
		aslist = []
		for i in range(9):
			aslist.append(self.state[9*i:9*(i + 1)])
		return '\n'.join(','.join(str(cell) for cell in line) for line in aslist)

	def __repr__(self):
		return str(self)

	def valid_n(self, cell):
		numbers = list(range(1,10))
		for clique in Board.cliques:
			if cell in clique:
				for other in clique:
					try:
						numbers.remove(self.state[other])
					except:
						pass
		return numbers

	def get_nexts(self):
		for cell in range(81):
			if self.state[cell] == 0:
				self.first_empty = cell
				self.nexts = self.valid_n(cell)
				return

	def validate(self): # returns list of inconsistent pairs
		fails = set([])
		for clique in Board.cliques:
			for first in range(8):
				for second in range(first + 1, 9):
					if self.state[clique[first]] == self.state[clique[second]]:
						fails.add((clique[first], clique[second]))
		return list(fails)

	def copy(self):
		return Board(''.join(str(c) for c in self.state))

def solve(stack):
	board = stack.pop()
	backtracks = 0
	while board:

		board.get_nexts()
		if board.first_empty == -1:
			print(backtracks)
			return board

		for option in board.nexts[::-1]:
			new = board.copy()
			new.state[board.first_empty] = option
			stack.push(new)
		board = stack.pop()
		backtracks += 1

def parse_boards(file, flag):
	boards = []
	line = file.readline()

	while line:
		buffer = ''
		if flag in line:
			for i in range(9):
				buffer += file.readline()

			buffer = buffer.replace(',','')
			buffer = buffer.replace('\n','')
			boards.append(buffer)

		line = file.readline()
	return boards

def main(argv = None):
	if not argv:
		try:
			__infile__ = sys.argv[1]
			__outfile__ = sys.argv[2]
			__board_flag__ = sys.argv[3]
		except Exception as ex:
			print('Expected 3 arguments')

	with open(__infile__, 'r') as infile:
		stacks = [Stack( [Board(board)] ) for board in parse_boards(infile, __board_flag__)]

	board = solve(stacks[0])
	with open(__outfile__, 'w') as outfile:
		outfile.write(str(board))
main()