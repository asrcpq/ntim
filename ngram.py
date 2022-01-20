import sys
import pickle
from keyseq_generator import keyseq
from ntim_data import NtimData

def dict_filter(d: dict, min_keep):
	d2 = {}
	for (key, value) in d.items():
		if value[1] >= min_keep:
			d2[key] = value
	return d2

ntim_data = NtimData()
ngrams = [{}]
lines = []
for line in sys.stdin:
	lines.append(line)

max_items = 1_000_000
min_keep = 1
for n in range(1, 5):
	print(f"Processing {n}-gram")
	ngram = {}

	line_num = len(lines)
	for (idx, line) in enumerate(lines):
		if idx % (line_num // 10) == 0:
			print(f"{idx}/{line_num}")
		line = f"s{line.strip()}" # s is start of seq
		if len(line) <= n - 1:
			continue
		for i in range(len(line) - n + 1):
			key = line[i:i+n]
			if key in ngram:
				ngram[key][1] += 1
			else:
				ks = keyseq(key)
				ngram[key] = [ks, 1]
	if n == 1:
		ntim_data.unigram_sum = sum([
			x[1] for x in ngram.values()
		])
	elif n == 2:
		ntim_data.bigram_n1 = sum([
			1 for i in ngram.values() if i[1] == 1
		])

	ngrams.append(ngram)
	while True:
		counts = sum([len(ngram) for ngram in ngrams])
		print("dict items size:", counts)
		if counts <= max_items:
			break
		min_keep += 1
		print("min keep count:", min_keep)
		for i in range(len(ngrams)):
			ngrams[i] = dict_filter(ngrams[i], min_keep)

ntim_data.ngrams = ngrams

with open('ntim.pkl', 'wb') as file:
	pickle.dump(ntim_data, file)
