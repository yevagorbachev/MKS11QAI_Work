#!/usr/bin/python3

import sys
import time
import copy

now = time.time

neighbors = {}
cliques = []

def setup():
	global neighbors, cliques
	neighbors = dict( (i,set([])) for i in range(81) )
	cliques = [[0,1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15,16,17],[18,19,20,21,22,23,24,25,26],[27,28,29,30,31,32,33,34,35],[36,37,38,39,40,41,42,43,44],[45,46,47,48,49,50,51,52,53],[54,55,56,57,58,59,60,61,62],[63,64,65,66,67,68,69,70,71],[72,73,74,75,76,77,78,79,80],[0,9,18,27,36,45,54,63,72],[1,10,19,28,37,46,55,64,73],[2,11,20,29,38,47,56,65,74],[3,12,21,30,39,48,57,66,75],[4,13,22,31,40,49,58,67,76],[5,14,23,32,41,50,59,68,77],[6,15,24,33,42,51,60,69,78],[7,16,25,34,43,52,61,70,79],[8,17,26,35,44,53,62,71,80],[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],[6,7,8,15,16,17,24,25,26],[27,28,29,36,37,38,45,46,47],[30,31,32,39,40,41,48,49,50],[33,34,35,42,43,44,51,52,53],[54,55,56,63,64,65,72,73,74],[57,58,59,66,67,68,75,76,77],[60,61,62,69,70,71,78,79,80]]
	for clique in cliques:
		for cell in clique:
			[neighbors[cell].add(neighbor) for neighbor in clique]

setup()

class Stack:

	def __init__(self, start = []):
		self.storage = {}
		self.filled = 0
		for item in start:
			self.push(item)

	def push(self, item):
		self.storage[self.filled] = item
		self.filled += 1

	def pop(self):
		if not self.filled:
			return None
		self.filled -= 1
		return self.storage[self.filled]

class Board:
	# INFRASTRUCTURE

	def __init__(self, string = ('0' * 81)):
		'''
		Makes a ``Board`` object from a string of digits.\n
		If a character is not a digit, a ``0`` is inserted.\n
		Parameters::\n
			string: str
		By default, returns a board with all positions set to ``0``.\n
		Raises::\n
			ValueError
		'''

		if len(string) != 81:
			raise ValueError(f'Expected string of length 81, got string of length {len(string)}')

		try_int = lambda c: int(c) if c.isdigit() else 0
		self.state = [try_int(c) for c in string]

	def __str__(self):
		'''renders the caller using commas to separate columns'''
		aslist = []
		for i in range(9):
			aslist.append(self.state[9*i:9*(i + 1)])
		return '\n'.join(','.join(str(cell) for cell in line) for line in aslist).replace('0','_') + '\n'

	def __repr__(self):
		'''renders the caller using commas to separate columns'''
		return str(self)

	def copy(self):
		'''returns a deep copy of the caller'''
		return copy.deepcopy(self)

	# SOLUTION ASSISTANCE
	def validate(self):
		for clique in cliques:
			for first in range(8):
				for second in range(first + 1, 9):
					if self.state[clique[first]] and self.state[clique[first]] == self.state[clique[second]]:
						return False
		return True

	def get_neighbors(self, cell):
		return neighbors[cell]

	def options(self, cell):
		'''
		Returns the list of possible numbers that can be inserted into cell
		'''
		numbers = [1 for i in range(10)]
		for neighbor in self.get_neighbors(cell):
			numbers[self.state[neighbor]] = 0
		numbers = [i for i in range(1,10) if numbers[i]]
		return set(numbers)
# SOLUTION LOGIC

def solve_naive(board):
	'''
	Solves using naive backtracking\n
	Parameters::\n
		board: Board
	Returns::\n
		{
		  'board': Board, #            Solved board
		  'time': float, # Solution time in seconds
		  'backtracks': int #  Number of backtracks
		}
	'''

	# Helpers
	def advance(board):
		for cell in range(81):
			if not board.state[cell]:
				opt = board.options(cell)
				if not opt or len(opt) > 1:
					return (cell, opt)
				if len(opt) == 1:
					board.state[cell] = opt.pop()
		return 'SOLVED'


	start = now()
	backtracks = 0
	stack = Stack()

	while board:
		# advance
		options = advance(board)
		if options == 'SOLVED':
			solved = board
			break
		for option in options[1]:
			new = board.copy()
			new.state[options[0]] = option
			stack.push(new)

		board = stack.pop()
		backtracks += 1

	return {'board': solved, 'time': now() - start, 'backtracks': backtracks}

def solve_least(board):
	'''
	Optimizes normal backtracking by calculating simple forcing states.\n
	Parameters::\n
		board: Board
	Returns::\n
		{
		  'board': Board, #            Solved board
		  'time': float, # Solution time in seconds
		  'backtracks': int #  Number of backtracks
		}
	'''

	# Helpers

	def set_options(board):
		board.all_options = {}
		for cell in range(81):
			if not board.state[cell]:
				board.all_options[cell] = board.options(cell)


	def adjust(board, cell, value):
		'''
		Sets a board's cell to a particular value, mutating neighbors' possiblities accordingly.

		Returns `True` if no contradictions (open cells with no possibilities) arose, `False` otherwise.

		`board` must have had `set_options` called, and the `all_options` entry for the cell must have been removed.
		'''
		board.state[cell] = value
		if not board.validate():
			return False
		for neighbor in board.get_neighbors(cell):
			if not board.state[neighbor]:
				board.all_options[neighbor].discard(value)

				ln = len(board.all_options[neighbor])
				if ln == 0:
					return False
				elif ln == 1:
					forced = board.all_options.pop(neighbor)
					if not adjust(board, neighbor, forced.pop()):
						return False
		return True

	start = now()
	backtracks = 0
	stack = Stack()

	set_options(board)

	while board:
		if not len(board.all_options):
			solved = board
			break

		options = [item for item in board.all_options.items()]
		options.sort(key = lambda i: len(i[1]))
		options = options[0]
		del board.all_options[options[0]]

		for option in options[1]:
			new = board.copy()
			status = adjust(new, options[0], option)
			if status:
				stack.push(new)

		backtracks += 1
		board = stack.pop()

	return {'board': solved, 'time': now() - start, 'backtracks': backtracks}

def solve_full(board):
	'''
	Optimizes normal backtracking by removing all forcing variations before guessing.\n
	Parameters::\n
		board: Board
	Returns::\n
		{
		  'board': Board, #            Solved board
		  'time': float, # Solution time in seconds
		  'backtracks': int #  Number of backtracks
		}
	'''

	start = now()
	backtracks = 0


	solved = Board()
	return {'board':solved, 'time': start - now(), 'backtracks':backtracks}

__modes__ = ['naive', 'least', 'full']

def solve(board, mode):
	'''
	Wrapper for solution methods.\n
	Parameters::\n
		board: Board
		mode: str # Takes the values \'naive\', \'least\', \'full\'
	Returns::\n
		{
		  'board': Board, #            Solved board
		  'time': float, # Solution time in seconds
		  'backtracks': int #  Number of backtracks
		}
	Raises::\n
		ValueError
	'''

	if mode == 'naive':
		solved = solve_naive(board)
	elif mode == 'least':
		solved = solve_least(board)
	elif mode == 'full':
		solved = solve_full(board)
	else:
		raise ValueError(f'Expected a mode of values \'naive\', \'least\', or \'full\', recieved \'{mode}\'')
	if not solved['board'].validate():
		print(solved['board'])
		raise RuntimeError(f'Solution mode \'{mode}\' failed')
	return solved

# INFRASTRUCTURE

def parse_boards(board_file, board_flag):
	'''
	Takes every board preceded by a line containing the flag\n
	Parameters::\n
		board_file: TextIOWrapper
		board_flag: str
	Returns::\n
		list<Board>
	'''

	boards = []
	line = board_file.readline()

	while line:
		buffer = ''
		if board_flag in line:
			for i in range(9):
				buffer += board_file.readline()

			buffer = buffer.replace(',','')
			buffer = buffer.replace('\n','')
			boards.append(buffer)

		line = board_file.readline()
	return [Board(board) for board in boards]

def main(argv = []):
	mode = 'naive'

	try:
		__infile__ = argv[1]
		__outfile__ = argv[2]
		__board_flag__ = argv[3]
	except IndexError as ex:
		raise ValueError(f'Expected 3 arguments, recieved {len(argv) - 1}')

	verbose = len(argv) > 4 and 'v' in argv[4]

	with open(__infile__, 'r') as infile:
		boards = parse_boards(infile, __board_flag__)

	start = now()
	solutions = [solve(board, mode) for board in boards]
	time = f'Solution mode: {mode}\nTotal CPU time: {now() - start}\n'

	if verbose:
		outstr = time
		for solution in solutions:
			backtracks = solution['backtracks']
			time = solution['time']
			board = solution['board']
			outstr += f'\nBacktracks: {backtracks}, CPU time: {time}\n{board}'

		print(outstr)
	else:
		outstr = ''
		for solution in solutions:
			outstr += str(solution['board'])

	with open(__outfile__, 'w') as outfile:
		outfile.write(outstr)

if __name__ == '__main__':
	main(sys.argv)