from copy import deepcopy

convert = {
	0:'_', -1:'o', 1:'x',
	'_':0, 'o':-1, 'x':1,
}

wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[6,4,2]]

transforms = {
	'x':(6, 7, 8, 3, 4, 5, 0, 1, 2),
	'y':(2, 1, 0, 5, 4, 3, 8, 7, 6),
	'cw':(6, 3, 0, 7, 4, 1, 8, 5, 2),
	'ccw':(2, 5, 8, 1, 4, 7, 0, 3, 6),
	'flip':(8, 7, 6, 5, 4, 3, 2, 1, 0),
}

class Board():

	# INFRASTRUCTURE
	def __init__(self, state = 0):
		if state:
			if type(state) == str:
				self.layout = state
				self.state = [convert[cell] for cell in state]
			elif type(state) == list:
				self.state = state
				self.layout = ''.join(convert[cell] for cell in state)
			self.turn = sum(1 for cell in self.state if cell)
		else:
			self.turn = 0
			self.layout = '_' * 9
			self.state = [0 for i in range(9)]

	def __str__(self):
		tostr = ''
		for i in range(3):
			tostr += self.layout[3*i:3*i+3] + '\n'
		return tostr

	def __repr__(self):
		return str(self)

	def copy(self):
		return deepcopy(self)

	# TRANSFORMATIONS
	def move(self, cell, value):
		if value in 'ox':
			self.layout = self.layout[:cell] + value + self.layout[cell + 1:]
			self.state[cell] = convert[value]
			self.turn += 1
		return self

	def check_end(self):
		if self.turn == 9:
			return 'DRAW'
		elif self.turn > 4:
			for win in wins:
				s = sum(self.state[cell] for cell in win)
				if s == 3:
					return 'WINX'
				elif s == -3:
					return 'WINO'
		return False

	def transform(self, method):
		mat = transforms[method]
		for i in range(9):
			self.state[i] = convert[
				 self.layout[ mat[i] ]
			]
		self.layout = ''.join(convert[cell] for cell in self.state)
		return self

	def family(self):
		full_family = [
			self.copy(),

			self.copy().transform('x'),

			self.copy().transform('cw'),
			self.copy().transform('ccw'),
			self.copy().transform('flip'),

			self.copy().transform('x').transform('cw'),
			self.copy().transform('y'),
			self.copy().transform('x').transform('ccw'),
		]

		return set(board.layout for board in full_family)

	def iso(self, other):
		return other.layout in self.family()

families = set([])
boards = set([])
counts = {
	'BOARDS':0,
	'GAMES':0,
	'DRAW':0,
	'WINX':0,
	'WINO':0,
}
def update(board):
	global boards, families
	if board.layout not in families:
		boards.add(board.layout)
		[families.add(member) for member in board.family()]

def run_variations(board):
	update(board)
	counts['BOARDS'] += 1
	end = board.check_end()
	if end:
		counts['GAMES'] += 1
		counts[end] += 1
	else:
		next_move = 'o' if board.turn % 2 else 'x'
		open_cells = [cell for cell in range(9) if not board.state[cell]]
		for cell in open_cells:
			run_variations(board.copy().move(cell, next_move))



run_variations(Board())
print(counts)
print(len(boards))