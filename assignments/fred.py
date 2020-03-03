#! /usr/bin/python3
import sys

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
	result = [split_line(line, line_delim) for line in result]
	return result

def DoIt(alist=None):

	fetch_pos_int = lambda string: int(string) if string.isdigit() else 0

	if alist and len(alist) == 3:

		# reading
		contents = []
		with open(alist[1], 'r') as infile:
			contents = infile.read()
			contents = split_lines(contents, '\n', ',')

		# processing
		out = []
		for line in contents:
			out.append([
				sum((1 if fetch_pos_int(element) else 0) for element in line),
				sum(fetch_pos_int(element) for element in line)
			])
		# print(out)

		# writing
		with open(alist[2], 'w') as outfile:
			outstr = '\n'.join(','.join(str(entry) for entry in line) for line in out)
			outfile.write(outstr)

	else:
		raise ValueError('DoIt must be supplied a list of 3 elements')

try:
	DoIt(sys.argv)
except ValueError as valex:
	print(valex)
	raise