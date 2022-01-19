import sys
import pickle
from keyseq_generator import keyseq
from ntim import NtimData

ntim_data = NtimData()
ngrams = [{}]
lines = []
for line in sys.stdin:
	lines.append(line)

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
		for i in range(len(line) - n):
			key = line[i:i+n]
			if key in ngram:
				ngram[key][1] += 1
			else:
				ks = keyseq(key)
				if not ks and key[0] != 's':
					continue
				ngram[key] = [ks, 1]
	if n == 1:
		ntim_data.unigram_sum = sum([
			x[1] for x in ngram.values()
		])
	elif n == 2:
		ntim_data.bigram_n1 = sum([
			1 for i in ngram.values() if i[1] == 1
		])

	if n >= 2:
		ngram2 = {}
		for (key, value) in ngram.items():
			if value[1] > 1:
				ngram2[key] = value
		ngrams.append(ngram2)
	else:
		ngrams.append(ngram)

ntim_data.ngrams = ngrams

with open('ntim.pkl', 'wb') as file:
	pickle.dump(ntim_data, file)
