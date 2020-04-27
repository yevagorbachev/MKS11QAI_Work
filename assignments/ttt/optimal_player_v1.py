#!/usr/bin/python3
import sys

WINS = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
turn = lambda t: 'x' if t % 2 else 'o'
Positions = (
	'Top-left','Top-center','Top-right',
	'Middle-left','Middle-center','Middle-right',
	'Bottom-left','Bottom-center','Bottom-right'
)

class BoardNode:

	def __init__(self, layout):
		self.layout = layout
		self.children = []
		self.left = layout.count('_')
		rows = [''.join(self.layout[cell] for cell in win) for win in WINS]
		if 'xxx' in rows:
			self.endState = 'x'
		elif 'ooo' in rows:
			self.endState = 'o'
		elif not self.left:
			self.endState = 'd'
		else: # if the game isn't over, calculate next games
			self.endState = None
			for cell, char in enumerate(layout):
				if char == '_':
					self.children.append((layout[:cell] + turn(self.left) + layout[cell+1:], cell))

	def __str__(self):
		tostr = ''
		for i in range(3):
			tostr += self.layout[3*i:3*i+3] + '\n'
		return tostr

	def __repr__(self):
		return f'Layout:\n{self}End state: {self.endState}\nChildren: {self.children}'


def populate_tree(tree, root):
	if root in tree:
		return
	node = BoardNode(root)
	tree[root] = node
	if not node.endState:
		for child in node.children:
			populate_tree(tree, child[0])

def make_tree(root):
	tree = {}
	populate_tree(tree, root)
	return tree

def optimize_result(tree, start):
	node = tree[start]
	if not node.endState: # game in progress
		preferred = turn(node.left) # player whose turn it is wants to win
		# sort results
		wins, draws, losses = [], [], []
		for child in node.children:
			result = optimize_result(tree, child[0])
			result = (result[0], result[1] + 1, child[1])
			if result[0] == preferred:
				wins.append(result)
			elif not wins and result[0] == 'd':
				draws.append(result)
			elif not draws and not wins:
				losses.append(result)
		# get best result
		length = lambda r:r[1]
		if wins:
			return min(wins, key=length)
		elif draws:
			return max(draws, key=length)
		else:
			return max(losses, key=length)
	else: # game finished
		return (node.endState, -1, -1)

def main():
	outfile = sys.argv[1]
	board = sys.argv[2]
	tree = make_tree(board)
	best = optimize_result(tree, board)
	player = turn(best.count('_'))

	r = 'wins' if best[0] == player else ('draws' if best[0] == 'd' else 'loses')
	result = f'{best[2]}\n{Positions[best[2]]}\n{player} {r} in {best[1]} moves'
	with open(outfile, 'w') as out:
		out.write(result)
	print(result)

main()