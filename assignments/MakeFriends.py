#!/usr/bin/python3

class Friend:

	def __init__(self, name, color, category):
		self.name = name
		self.color = color
		self.category = category

	def as_list(self):
		return [self.name, self.color, self.category]

class FriendGroup:
	def __init__(self):
		self.group = {}

	def add(self, name, color, category):
		fred = Friend(name, color, category)
		self.group[name] = fred

	def delete(self, name):
		try:
			del self.group[name]
			return True
		except KeyError:
			return False

	def get_cat(self, name):
		try:
			return self.group[name].category
		except KeyError:
			return None

	def change_cat(self, old_category, new_category):
		friends = self.group.items()
		for name, f_object in friends:
			if f_object.category == old_category:
				f_object.category = new_category

	def get_friend(self, name):
		try:
			return self.group[name]
		except KeyError:
			return None

	def get_names(self):
		return list(self.group.keys())

	def list_details(self):
		friends = self.group.values()
		friends = [f_object.as_list() for f_object in friends]
		friends.sort(key=lambda l:l[0])
		return friends

class myCSV:

	def split_line(line, delimiter):
		outline = []
		in_quote = False
		last = 0
		for index, char in enumerate(line):
			if char == '\"':
				in_quote = not in_quote
			else:
				if char == delimiter and not in_quote:
					outline.append(line[last:index])
					last = index + 1

		outline.append(line[last:])
		return outline

	def split_lines(lines, row_delim, line_delim):
		result = lines.split(row_delim)
		result = [myCSV.split_line(line, line_delim) for line in result]
		return result

	def combine_lines(lines, row_delim, line_delim):
		return row_delim.join(line_delim.join(str(entry) for entry in line) for line in lines)

import sys

__infile__ = sys.argv[1]
__outfile__ = sys.argv[2]
__group__ = FriendGroup()


def apply(argv):
	if argv[0] == 'add':
		return __group__.add(argv[1],argv[2],argv[3])
	elif argv[0] == 'delete':
		return __group__.delete(argv[1])
	elif argv[0] == 'get_cat':
		return __group__.get_cat(argv[1])
	elif argv[0] == 'change_cat':
		return __group__.change_cat(argv[1],argv[2])
	elif argv[0] == 'get_friend':
		return __group__.get_friend(argv[1])
	elif argv[0] == 'get_names':
		return __group__.get_names()
	elif argv[0] == 'print':
		out = __group__.list_details()
		outstr = myCSV.combine_lines(out, '\n', ',')
		with open(__outfile__, 'w') as outfile:
			outfile.write(outstr)

with open(__infile__,'r') as infile:
	input_list = myCSV.split_lines(infile.read(), '\n', ',')
	for command in input_list:
		apply(command)
