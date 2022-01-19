import os
import itertools

def load_char_mapper():
	mapper = {}
	if not os.environ['NTIM_CHAR_MAPPER']:
		return {}
	with open(os.environ['NTIM_CHAR_MAPPER'], "r") as f:
		for line in f:
			(lat, ch) = line.split()
			if ch in mapper:
				mapper[ch].append(lat)
			else:
				mapper[ch] = [lat]
	return mapper

def load_exact_mapper():
	mapper = {}
	if not os.environ['NTIM_CHAR_MAPPER']:
		return {}
	with open(os.environ['NTIM_EXACT_MAPPER'], "r") as f:
		for line in f:
			try:
				(lat, string) = line.split()
			except:
				print(f"error: {line}")
				continue
			if string in mapper:
				mapper[string].append(lat)
			else:
				mapper[string] = [lat]
	return mapper

char_mapper = load_char_mapper()
exact_mapper = load_exact_mapper()
def keyseq(string):
	result = []
	if string in exact_mapper:
		result += exact_mapper[string]
	
	lat = []
	flag = True
	for ch in string:
		if ch in char_mapper:
			lat.append(char_mapper[ch])
		else:
			flag = False
			break
	if flag:
		result += ["".join(tup) for tup in itertools.product(*lat)]
	return result
