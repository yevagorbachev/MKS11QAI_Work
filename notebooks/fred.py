from csv import reader, writer
from sys import argv

def DoIt(alist=None):

	fetch_pos_int = lambda string: int(string) if string.isdigit() else 0

	if alist and len(alist) == 3:

		# reading
		contents = []
		with open(alist[1], 'r') as infile:
			contents = [line for line in reader(infile)]

		# processing
		out = []
		for line in contents:
			out.append([
				sum([(1 if fetch_pos_int(element) else 0) for element in line]),
				sum(fetch_pos_int(element) for element in line)
			])
		print(out)

		# writing
		with open(alist[2], 'w') as outfile:
			writer(outfile).writerows(out)

	else:
		raise Exception('DoIt must be supplied a list of 3 elements')

try:
	DoIt(argv)
except Exception as ex:
	print(ex)
	raise